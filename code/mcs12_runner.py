"""mcs12_runner.py — Ouverture de la carte MCS-12 (jalon 5, nucleosynthese).

Carte scellee : cartes/v2/MCS-12-bbn-elements-legers.md
  sha256 pre-gel : 90f1705d3d808674755c48fde200fae629d097ad79e4afa7b2d055bc1ad5eba4
Donnees (acquisition a l'ouverture, empreintes au journal) :
  - donnees/mcs12/rpp2024-rev-bbang-nucleosynthesis.pdf (canonique)
  - donnees/mcs12/rpp2022-rev-bbang-nucleosynthesis.pdf (g1)

DEVIATIONS DECLAREES (consignees au journal) :
- les observations 3He/H : la revue PDG refuse explicitement d'adopter une
  valeur primordiale pour 3He (paragraphe dedie) ; la valeur utilisee est la
  valeur classique de la litterature (1,1 +/- 0,2) x 1e-5 (Bania, Rood &
  Balser 2002) — deviation de provenance declaree ;
- les predictions : la revue figure les bandes mais ne les tabule pas en
  texte ; elles sont lues dans sa source citee [44] (Fields et al. 2020,
  JCAP 03, 010 — Table 3, ligne "this work", eta10 = 6,129, N_nu = 3) :
  D/H = 2,559e-5 ; 3He/H = 0,9965e-5 ; Yp = 0,2470 ; 7Li/H = 4,702e-10.

Observations (revue PDG 2024, valeurs recommandees textuelles) :
  D/H = (25,47 +/- 0,29) x 1e-6 (eq. 24.2, facteur S applique) ;
  Yp = 0,245 +/- 0,003 (eq. 24.3) ; 7Li/H = (1,6 +/- 0,3) x 1e-10 (eq. 24.4).
Edition 2022 (g1) : D/H = (25,47 +/- 0,25) x 1e-6 ; Yp et 7Li identiques.

Mesure scellee : m = -log10(RMS(log10 pred - log10 obs)) sur les elements
de la configuration. Nul N1 : 10 000 univers aleatoires log-uniformes dans
les etendues de la carte. Sigma = min sur {g1..g6} (g0 hors Sigma).
Seuil de la carte : 3,0 = seuil DEFAULT du moteur scelle.
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

CARTE_ID = "MCS-12"
EMPREINTE_CARTE = "90f1705d3d808674755c48fde200fae629d097ad79e4afa7b2d055bc1ad5eba4"
DATA = os.path.join(RACINE, "donnees", "mcs12")
RESULTATS = os.path.join(RACINE, "resultats", "mcs12_resultats.json")
N_NUL = 10000

ELEMENTS = ["D/H", "3He/H", "Yp", "7Li/H"]
PRED = np.array([2.559e-5, 0.9965e-5, 0.2470, 4.702e-10])   # Fields 2020 T3
OBS24 = np.array([2.547e-5, 1.1e-5, 0.245, 1.6e-10])        # revue 2024
SIG24 = np.array([0.029e-5, 0.2e-5, 0.003, 0.3e-10])
OBS22 = np.array([2.547e-5, 1.1e-5, 0.245, 1.6e-10])        # revue 2022
ETENDUES = [(1e-6, 1e-3), (1e-6, 1e-3), (0.05, 0.5), (1e-11, 1e-8)]


def mesure(pred, obs, sel):
    eps = np.log10(pred[sel]) - np.log10(obs[sel])
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def univers(gen, n=4):
    return np.array([np.exp(gen.uniform(np.log(a), np.log(b)))
                     for a, b in ETENDUES])


def z_config(gen, pred, obs, sel, nb=N_NUL):
    m_val = mesure(pred, obs, sel)
    ms = [mesure(pred, univers(gen), sel) for _ in range(nb)]
    return m_val, mcs.z_score(m_val, float(np.mean(ms)), float(np.std(ms)))


def main():
    empreintes = {f: hashlib.sha256(
        open(os.path.join(DATA, f), "rb").read()).hexdigest()
        for f in sorted(os.listdir(DATA))}
    empreinte_donnees = hashlib.sha256(
        json.dumps(empreintes, sort_keys=True).encode()).hexdigest()
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    tout = list(range(4))
    z, m_par = {}, {}
    m0, z["g0_canonique_HORS_SIGMA"] = z_config(gen, PRED, OBS24, tout)
    m_par["g0_canonique_HORS_SIGMA"] = m0
    ms0 = [mesure(PRED, univers(gen), tout) for _ in range(N_NUL)]
    u0 = float(np.std(ms0))

    _, z["g1_revue2022"] = z_config(gen, PRED, OBS22, tout)
    _, z["g2_sans_7Li"] = z_config(gen, PRED, OBS24, [0, 1, 2])
    _, z["g3_sans_3He"] = z_config(gen, PRED, OBS24, [0, 2, 3])
    _, z["g4_obs_plus_1sigma"] = z_config(gen, PRED, OBS24 + SIG24, tout)
    _, z["g5_obs_moins_1sigma"] = z_config(gen, PRED, OBS24 - SIG24, tout)
    victime = int(gen.uniform(0, 4))
    sel6 = [i for i in tout if i != victime]
    _, z["g6_retrait_" + ELEMENTS[victime].replace("/", "")] = z_config(
        gen, PRED, OBS24, sel6)

    # controles positifs (unites du nul canonique)
    effet_c1 = (m0 - mesure(gen.permutation(PRED), OBS24, tout)) / u0
    effet_c2 = (m0 - mesure(PRED, univers(gen), tout)) / u0

    # diagnostic : ecarts par element (dex) — la rupture 7Li est publiee
    eps = {ELEMENTS[i]: float(np.log10(PRED[i]) - np.log10(OBS24[i]))
           for i in tout}

    v = mcs.evaluer_v2("DEFAULT", z, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1},
                       exclure=("g0_canonique_HORS_SIGMA",))
    vd = v.to_dict()
    s = vd["sigma"]

    out = {"carte": CARTE_ID, "empreinte_carte_pre_gel": EMPREINTE_CARTE,
           "empreintes_fichiers": empreintes,
           "empreinte_donnees": empreinte_donnees,
           "predictions_Fields2020": dict(zip(ELEMENTS, PRED.tolist())),
           "observations_PDG2024": dict(zip(ELEMENTS, OBS24.tolist())),
           "sigmas_PDG2024": dict(zip(ELEMENTS, SIG24.tolist())),
           "observations_PDG2022": dict(zip(ELEMENTS, OBS22.tolist())),
           "ecarts_dex_canoniques": eps,
           "m_par_config": m_par, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.0": vd["verdict"],
           "deviations_declarees": [
               "3He/H observation : valeur classique (1,1e-5) — la revue "
               "n'adopte pas de valeur (deviation de provenance)",
               "predictions lues dans la source citee [44] de la revue "
               "(Fields et al. 2020, Table 3 'this work')"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict": vd["verdict"],
                      "z_par_g": z, "controles": out["controles"],
                      "ecarts_dex": eps}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
