"""mcs07_runner.py — Ouverture de la carte MCS-07 (jalon 4 v2).

Carte scellee : cartes/v2/MCS-07-economie-information.md
  sha256 pre-gel : 426ee08b718e6d693a41d5718b4c251e1a00a4296ef645b6c4872b443e4be05f
Donnees figees : donnees/mcs07_corpus_m1.json (artefacts M1/M1b du corpus
  noetic-machine-complete, empreintes GitHub consignees dans le journal).

Mesure scellee : m = -rho_Spearman(delta, tau) sur les 14 chantiers P20-P33
(restriction tau declaree par M1). delta binaire : proche = {P31, P32, P33}
(groupe frontiere M1 restreint au corpus tau ; P39 hors corpus, tau nul).

Decisions d'execution publiees (la carte est scellee ; ce qui suit
operationalise sans rien re-ajuster apres mesure) :
- g1 : denominateur alternatif tau' = succes / (V2 + 1) (convention de
  retraitement declaree ici, avant calcul).
- g2 : la mesure scellée ne depend pas de S — la deformation metrique de
  taille est INERTE sur m ; rapportee comme telle (m_g2 = m_canonique).
- g3 : le retrait de P31-P33 vide le contraste binaire (ce sont les seuls
  points proches) ; la deformation est appliquee sur le delta trois niveaux
  declare (g4), decision d'execution publiee dans le verdict.
- g6 : retrait d'un chantier tire par le PRNG public ChaCha20
  (cle = SHA-256("MCS-J4V2|" + empreinte_carte + "|" + empreinte_donnees)).

Seuil de la carte : 3,1 (regard ailleurs). Le moteur scelle mcs_score_v2
plafonne a DEFAULT = 3,0 pour les cartes v2 ; le runner applique le seuil
de la carte et consigne les deux.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np
from scipy.stats import spearmanr, kendalltau

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-07"
SEUIL_CARTE = 3.1
EMPREINTE_CARTE = "426ee08b718e6d693a41d5718b4c251e1a00a4296ef645b6c4872b443e4be05f"
DONNEES = os.path.join(RACINE, "donnees", "mcs07_corpus_m1.json")
RESULTATS = os.path.join(RACINE, "resultats", "mcs07_resultats.json")
N_NUL = 10000
N_C1 = 200


def cle_publique(empreinte_donnees: str) -> bytes:
    return hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()
    ).digest()


def mesure(delta, tau, methode="spearman"):
    if methode == "kendall":
        return -kendalltau(delta, tau).statistic
    return -spearmanr(delta, tau).statistic


def nul_n1(gen, delta, tau, methode="spearman", n=N_NUL):
    return np.array([mesure(gen.permutation(delta), tau, methode)
                     for _ in range(n)])


def main():
    with open(DONNEES, "rb") as f:
        brut = f.read()
    empreinte_donnees = hashlib.sha256(brut).hexdigest()
    d = json.loads(brut)
    chantiers = d["chantiers"]
    ids = [c["id"] for c in chantiers]
    tau = np.array([c["succes"] / c["V2"] for c in chantiers])
    tau_alt = np.array([c["succes"] / (c["V2"] + 1) for c in chantiers])  # g1
    delta = np.array([float(d["delta_binaire"].get(i, 0)) for i in ids])
    q3 = d["Q3_NF_rho1_M1"]
    delta3 = np.array([2.0 if d["delta_binaire"].get(i, 0) == 1
                       else (1.0 if (c["rho1"] is not None and c["rho1"] >= q3)
                             else 0.0)
                       for i, c in zip(ids, chantiers)])

    gen = prng.PRNGChaCha(cle_publique(empreinte_donnees))

    # configuration canonique
    m_reel = mesure(delta, tau)
    n1 = nul_n1(gen, delta, tau)
    mu, u = float(np.mean(n1)), float(np.std(n1))
    z = {"g0_canonique": mcs.z_score(m_reel, mu, u)}

    # g1 : denominateur alternatif
    m1_ = mesure(delta, tau_alt)
    n1g = nul_n1(gen, delta, tau_alt)
    z["g1_denominateur"] = mcs.z_score(m1_, float(np.mean(n1g)), float(np.std(n1g)))

    # g2 : inerte sur la mesure scellee (S n'y entre pas) — rapporte
    z["g2_metrique_taille_INERTE"] = z["g0_canonique"]

    # g3 : retrait P31-P33, delta trois niveaux (decision d'execution)
    masque = np.array([i not in ("P31", "P32", "P33") for i in ids])
    m3 = mesure(delta3[masque], tau[masque])
    n1g = nul_n1(gen, delta3[masque], tau[masque])
    z["g3_retrait_frontiere"] = mcs.z_score(m3, float(np.mean(n1g)),
                                            float(np.std(n1g)))

    # g4 : delta trois niveaux
    m4 = mesure(delta3, tau)
    n1g = nul_n1(gen, delta3, tau)
    z["g4_delta_3_niveaux"] = mcs.z_score(m4, float(np.mean(n1g)),
                                          float(np.std(n1g)))

    # g5 : Kendall
    m5 = mesure(delta, tau, "kendall")
    n1g = nul_n1(gen, delta, tau, "kendall")
    z["g5_kendall"] = mcs.z_score(m5, float(np.mean(n1g)), float(np.std(n1g)))

    # g6 : retrait d'un chantier au hasard (PRNG public)
    victime = int(gen.uniform(0, len(ids)))
    masque6 = np.arange(len(ids)) != victime
    m6 = mesure(delta[masque6], tau[masque6])
    n1g = nul_n1(gen, delta[masque6], tau[masque6])
    z["g6_retrait_" + ids[victime]] = mcs.z_score(m6, float(np.mean(n1g)),
                                                  float(np.std(n1g)))

    # controles positifs
    ms_c1 = [mesure(gen.permutation(delta), tau) for _ in range(N_C1)]
    effet_c1 = (m_reel - float(np.mean(ms_c1))) / u      # c1 : delta permutees
    m_c2 = mesure(1.0 - delta, tau)                      # c2 : proche <-> lointain
    effet_c2 = (m_reel - m_c2) / u

    v = mcs.evaluer_v2("DEFAULT", z, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()
    # seuil de la carte (3,1) applique par le runner, moteur a 3,0 consigne
    sigma_val = vd["sigma"]
    if vd["verdict"] == "CS0":
        verdict_carte = "CS0"
    elif sigma_val >= SEUIL_CARTE:
        verdict_carte = "CS+"
    elif sigma_val >= 2.0:
        verdict_carte = "CSp"
    elif sigma_val <= -2.0:
        verdict_carte = "CSi"
    else:
        verdict_carte = "CS-"

    out = {
        "carte": CARTE_ID,
        "empreinte_carte_pre_gel": EMPREINTE_CARTE,
        "empreinte_donnees": empreinte_donnees,
        "cle_prng_publique": cle_publique(empreinte_donnees).hex(),
        "m_canonique": m_reel, "mu_n1": mu, "u_n1": u,
        "z_par_g": z, "controles": {"c1": effet_c1, "c2": effet_c2},
        "verdict_moteur_seuil_3.0": vd,
        "verdict_carte_seuil_3.1": verdict_carte,
        "decisions_execution": [
            "g1 : tau' = succes/(V2+1)",
            "g2 : deformation inerte sur la mesure scellee, rapportee",
            "g3 : delta trois niveaux (delta binaire degenere apres retrait)",
        ],
    }
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": sigma_val, "verdict_carte": verdict_carte,
                      "z_par_g": z, "controles": out["controles"]},
                     indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
