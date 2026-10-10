"""mcs04_runner.py — Ouverture de la carte MCS-04 (jalon 4 v2).

Carte scellee : cartes/v2/MCS-04-loi-harmonique.md
  sha256 pre-gel : 3cda0e155f11451263ee8ec1f7f1a9cd84c617e6a0e4eedc6a15b91b445b10b9
Donnees figees : tables PDG "mass_width" (provenance publique, empreintes
  sha256 consignees au journal) :
  - donnees/mcs04_mass_width_2024.mcd  (edition 2024, generee 31-05-2024)
  - donnees/mcs04_mass_width_2022.mcd  (edition 2022, deformation g3)

Zoo gele (14 particules, lues dans la table 2024 a l'execution) :
  leptons e/mu/tau, quarks u/d/s/c/b/t, bosons W/Z/H, proton, neutron.
Mesure scellee : m = -log10(RMS(r)), r(m) = n(m) - round(n(m)),
  n(m) = 12*log2(m/m_p), ancre m_p (proton PDG 2024).

Decisions d'execution publiees :
- g3 : la table 2022 ne contient pas les quarks legers u/d/s/c ; la
  deformation porte sur l'intersection des deux editions (10 particules).
- g5 : les deux pas delta' = 2^(1/11) et 2^(1/13) sont evalues ; z_g5 = min
  des deux (pire cas, maillon le plus faible).
- g6 : retrait d'une particule tiree par le PRNG public ChaCha20
  (cle = SHA-256("MCS-J4V2|" + empreinte_carte + "|" + empreinte_donnees)).

Seuil de la carte : 3,1 (regard ailleurs). Moteur scelle a DEFAULT 3,0 ;
le runner applique le seuil de la carte et consigne les deux.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-04"
SEUIL_CARTE = 3.1
EMPREINTE_CARTE = "3cda0e155f11451263ee8ec1f7f1a9cd84c617e6a0e4eedc6a15b91b445b10b9"
F2024 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2024.mcd")
F2022 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2022.mcd")
RESULTATS = os.path.join(RACINE, "resultats", "mcs04_resultats.json")
N_NUL = 10000
DELTA = 2 ** (1 / 12)

ZOO = [("e", "-"), ("mu", "-"), ("tau", "-"),
       ("u", "+2/3"), ("d", "-1/3"), ("s", "-1/3"),
       ("c", "+2/3"), ("b", "-1/3"), ("t", "+2/3"),
       ("W", "+"), ("Z", "0"), ("H", "0"),
       ("p", "+"), ("n", "0")]
QUARKS = {"u", "d", "s", "c", "b", "t"}
BOSONS = {"W", "Z", "H"}


def lire_table(chemin):
    out = {}
    for ln in open(chemin):
        if ln.startswith("*") or not ln.strip():
            continue
        try:
            masse = float(ln[32:52].split()[0])
        except (ValueError, IndexError):
            continue
        nom_ch = ln[106:].split()
        if nom_ch:
            out[(nom_ch[0], nom_ch[1] if len(nom_ch) > 1 else "")] = masse
    return out


def mesure(masses, m_ref, delta=DELTA):
    ld = np.log2(delta)
    r = np.array([np.log2(m / m_ref) / ld for m in masses])
    r = r - np.round(r)
    return -np.log10(np.sqrt(np.mean(r ** 2)))


def z_sous_n1(gen, masses, m_ref, delta=DELTA, n=N_NUL):
    m_val = mesure(masses, m_ref, delta)
    ms = [mesure(masses, m_ref, float(gen.uniform(2 ** (1 / 13), 2 ** (1 / 11))))
          for _ in range(n)]
    mu, u = float(np.mean(ms)), float(np.std(ms))
    return m_val, mcs.z_score(m_val, mu, u), mu, u


def main():
    with open(F2024, "rb") as f:
        b24 = f.read()
    with open(F2022, "rb") as f:
        b22 = f.read()
    emp24, emp22 = hashlib.sha256(b24).hexdigest(), hashlib.sha256(b22).hexdigest()
    empreinte_donnees = hashlib.sha256(b24 + b22).hexdigest()
    t24, t22 = lire_table(F2024), lire_table(F2022)

    noms = [n for n, _ in ZOO]
    masses = {n: t24[(n, c)] for n, c in ZOO}
    m_p = masses["p"]
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    z = {}
    # canonique
    m_reel, z0, mu, u = z_sous_n1(gen, [masses[n] for n in noms], m_p)
    z["g0_canonique"] = z0
    # g1 : ancre m_p -> m_e
    _, z["g1_ancre_m_e"], _, _ = z_sous_n1(gen, [masses[n] for n in noms],
                                         masses["e"])
    # g2 : retrait des quarks
    sel = [n for n in noms if n not in QUARKS]
    _, z["g2_sans_quarks"], _, _ = z_sous_n1(gen, [masses[n] for n in sel], m_p)
    # g3 : PDG 2022 (intersection declaree : les deux editions)
    sel3 = [n for n in noms if (n, dict(ZOO)[n]) in t22]
    _, z["g3_pdg2022"], _, _ = z_sous_n1(
        gen, [t22[(n, dict(ZOO)[n])] for n in sel3], t22[("p", "+")])
    # g4 : retrait des bosons
    sel4 = [n for n in noms if n not in BOSONS]
    _, z["g4_sans_bosons"], _, _ = z_sous_n1(gen, [masses[n] for n in sel4], m_p)
    # g5 : pas du reseau (pire des deux)
    _, z5a, _, _ = z_sous_n1(gen, [masses[n] for n in noms], m_p, 2 ** (1 / 11))
    _, z5b, _, _ = z_sous_n1(gen, [masses[n] for n in noms], m_p, 2 ** (1 / 13))
    z["g5_pas_reseau_min"] = min(z5a, z5b)
    # g6 : retrait d'une particule au hasard (PRNG public)
    victime = int(gen.uniform(0, len(noms)))
    sel6 = [n for i, n in enumerate(noms) if i != victime]
    _, z["g6_retrait_" + noms[victime]], _, _ = z_sous_n1(
        gen, [masses[n] for n in sel6], m_p)

    # controles positifs (unites du nul canonique N1)
    masses_dec = [m * 2 ** (1 / 24) for m in (masses[n] for n in noms)]  # c1
    effet_c1 = (m_reel - mesure(masses_dec, m_p)) / u
    masses_bruit = list(m_p * np.exp(gen.uniform(np.log(0.0005 / m_p),
                                                 np.log(173.0 / m_p), len(noms))))
    effet_c2 = (m_reel - mesure(masses_bruit, m_p)) / u                  # c2

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
           "empreintes_donnees": {"mass_width_2024.mcd": emp24,
                                  "mass_width_2022.mcd": emp22,
                                  "combinee": empreinte_donnees},
           "zoo_2024_GeV": masses, "m_canonique": m_reel,
           "mu_n1": mu, "u_n1": u, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.1": verdict_carte,
           "decisions_execution": [
               "g3 : intersection des editions 2024/2022 (10 particules, "
               "quarks legers absents de la table 2022)",
               "g5 : z = min des deux pas delta' (maillon le plus faible)"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z,
                      "controles": out["controles"]}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
