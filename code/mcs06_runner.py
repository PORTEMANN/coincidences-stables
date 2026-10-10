"""mcs06_runner.py — Ouverture de la carte MCS-06 (jalon 4 v2).

Carte scellee : cartes/v2/MCS-06-loi-bifurcations.md
  sha256 pre-gel : 46f1c95083d8472b64779b6b7202a3fb15cc4c2ffb27737b1aba507657370ee8
Donnees figees : donnees/mcs06_bifurcations.json (20 bifurcations : 14
  physiques + 6 conventionnelles ; 5 D cites du corpus, 15 D mesures a
  l'execution par batterie figee de 5 tests, justifications incluses).

Mesure scellee : m = -rho_Spearman(D, Z_eff) sur les bifurcations PHYSIQUES
seules ; l'axe conventionnel n'entre pas dans m (controle c3 : |rho_conv|
rapporte).

Decisions d'execution publiees (carte scellee, rien de re-ajuste) :
- g1 : gamma = Z^2/137^2 applique a Z_eff ; Spearman est invariant par
  transformation monotone croissante -> deformation INERTE sur m, rapportee.
- g2 : retrait des 5 verdicts du corpus -> il reste les 15 bifurcations
  mesurees a l'execution (10 physiques). L'arriere-plan "(7 nouvelles)" du
  tableau des deformations est un reste de redaction ; l'ensemble fige de la
  section 4 (15 nouvelles) fait foi.
- g4 : le seuil rho (-0,7 -> -0,6) ne figure pas dans la mesure scellee
  (m = -rho_phys, continu) -> deformation INERTE, rapportee.
- g5 : batterie reduite aux tests 1-3 pour les 15 points mesures a
  l'execution ; les 5 D du corpus sont cites publies et non decomposables.
- g6 : permutation des etiquettes de type (PRNG public ChaCha20). ATTENTION,
  publie : g6 est par construction un tirage du nul N1 (types permutes) ;
  son z sous N1 est donc ~N(0,1) quelle que soit la realite de la loi —
  la carte inclut ce tirage dans le minimum Sigma (section 8).

Seuil de la carte : 3,1. Moteur scelle a DEFAULT 3,0 ; le runner applique
le seuil de la carte et consigne les deux.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np
from scipy.stats import spearmanr

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-06"
SEUIL_CARTE = 3.1
EMPREINTE_CARTE = "46f1c95083d8472b64779b6b7202a3fb15cc4c2ffb27737b1aba507657370ee8"
DONNEES = os.path.join(RACINE, "donnees", "mcs06_bifurcations.json")
RESULTATS = os.path.join(RACINE, "resultats", "mcs06_resultats.json")
N_NUL = 10000
N_C1 = 200
CORPUS = {"P-He", "P-CrCu-3d", "P-CrCu-4d", "P-CrCu-5d", "C-LaLr"}

# issues des 5 tests declares dans donnees/mcs06_bifurcations.json
# (1 = prediction derivee confirmee / propriete convergente dominante)
TESTS = {"P-N-tete15": [1, 1, 1, 1, 1], "P-O-tete16": [1, 1, 1, 1, 1],
         "P-Ne-inertie": [1, 1, 1, 1, 1], "P-Si-covalence": [1, 1, 1, 1, 1],
         "P-Ge-covalence": [1, 1, 1, 1, 1], "P-La-tete-f": [0, 0, 1, 1, 0],
         "P-Hg-homologue": [1, 0, 0, 0, 0], "P-Au-homologue": [1, 0, 0, 0, 0],
         "P-Pb-paire-inerte": [1, 0, 0, 0, 1],
         "P-U-tete-actinide": [0, 0, 0, 0, 0],
         "C-H-placement": [1, 0, 0, 1, 0], "C-ligne-metalloide": [1, 1, 0, 1, 0],
         "C-Zn-transition": [1, 1, 1, 1, 0], "C-Po-metal": [1, 0, 0, 0, 0],
         "C-At-halogene": [1, 1, 0, 1, 0]}


def mesure(Z, D, types):
    ph = types == 1
    return -spearmanr(Z[ph], D[ph]).statistic   # m = -rho_phys


def nul_n1(gen, Z, D, types, n=N_NUL):
    """N1 : etiquettes de type permutees (memes effectifs 14/6)."""
    return np.array([mesure(Z, D, gen.permutation(types)) for _ in range(n)])


def z_sous_n1(gen, Z, D, types):
    m_val = mesure(Z, D, types)
    ms = nul_n1(gen, Z, D, types)
    return m_val, mcs.z_score(m_val, float(np.mean(ms)), float(np.std(ms))), ms


def main():
    with open(DONNEES, "rb") as f:
        brut = f.read()
    empreinte_donnees = hashlib.sha256(brut).hexdigest()
    d = json.loads(brut)["bifurcations"]
    ids = np.array([b["id"] for b in d])
    Z = np.array([b["Z"] for b in d], dtype=float)
    D = np.array([b["D"] for b in d], dtype=float)
    types = np.array([1 if b["type"] == "physique" else 0 for b in d])
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    z = {}
    m_reel, z0, n1 = z_sous_n1(gen, Z, D, types)
    mu, u = float(np.mean(n1)), float(np.std(n1))
    z["g0_canonique"] = z0

    # g1 : correction relativiste sur Z (inerte sur Spearman — rapportee)
    gamma = (Z / 137.0) ** 2
    z["g1_Z_relativiste_INERTE"] = z_sous_n1(gen, Z * (1 + gamma), D, types)[1]

    # g2 : retrait des 5 verdicts du corpus (15 nouvelles seules)
    masque = np.array([i not in CORPUS for i in ids])
    z["g2_sans_corpus"] = z_sous_n1(gen, Z[masque], D[masque], types[masque])[1]

    # g3 : retrait de He
    masque = ids != "P-He"
    z["g3_sans_He"] = z_sous_n1(gen, Z[masque], D[masque], types[masque])[1]

    # g4 : seuil rho absent de la mesure scellee — inerte, rapporte
    z["g4_seuil_rho_INERTE"] = z0

    # g5 : batterie reduite aux tests 1-3 (points mesures a l'execution)
    D3 = D.copy()
    for i, bid in enumerate(ids):
        if bid in TESTS:
            D3[i] = float(np.mean(TESTS[bid][:3]))
    z["g5_batterie_3_tests"] = z_sous_n1(gen, Z, D3, types)[1]

    # g6 : permutation des types (PRNG public) — tirage du nul N1, publie
    types6 = gen.permutation(types)
    m6, z6, _ = z_sous_n1(gen, Z, D, types6)
    z["g6_types_permutés"] = z6

    # controles positifs (unites du nul canonique N1)
    ph = types == 1
    ms_c1 = []
    for _ in range(N_C1):
        Dp = D.copy()
        Dp[ph] = gen.permutation(D[ph])
        ms_c1.append(mesure(Z, Dp, types))
    effet_c1 = (m_reel - float(np.mean(ms_c1))) / u
    D_rev = D.copy()
    D_rev[ph] = D[ph][np.argsort(np.argsort(-Z[ph]))]  # rangs retournes (c2)
    effet_c2 = (m_reel - mesure(Z, D_rev, types)) / u
    rho_conv = float(abs(spearmanr(Z[types == 0], D[types == 0]).statistic))

    v = mcs.evaluer_v2("DEFAULT", z, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()
    s = vd["sigma"]
    if vd["verdict"] == "CS0":
        verdict_carte = "CS0"
    elif s >= SEUIL_CARTE:
        verdict_carte = "CS+"
    elif s >= 2.0:
        verdict_carte = "CSp"
    elif s <= -2.0:
        verdict_carte = "CSi"
    else:
        verdict_carte = "CS-"

    out = {"carte": CARTE_ID, "empreinte_carte_pre_gel": EMPREINTE_CARTE,
           "empreinte_donnees": empreinte_donnees,
           "m_canonique": m_reel, "mu_n1": mu, "u_n1": u,
           "z_par_g": z, "controles": {"c1": effet_c1, "c2": effet_c2},
           "c3_rho_conv_abs": rho_conv,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.1": verdict_carte,
           "decisions_execution": [
               "g1 inerte (Spearman invariant monotone), rapportee",
               "g2 : 15 nouvelles seules (parenthese '7' = reste de redaction)",
               "g4 inerte (pas de seuil dans m continu), rapportee",
               "g6 : tirage du nul N1 inclus dans Sigma par la carte scellee"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z, "controles": out["controles"],
                      "c3_rho_conv": rho_conv}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
