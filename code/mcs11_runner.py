"""mcs11_runner.py — Ouverture de la carte MCS-11 (jalon 5, particules).

Carte scellee : cartes/v2/MCS-11-koide-leptons.md
  sha256 pre-gel : 7eaad89022d57ab342590196dc79c9ac880792c7879c07ea50e1e29fd2efbe21
Donnees (deja acquises et empreintees au depot — reutilisation consignee) :
  - donnees/mcs04_mass_width_2024.mcd  (PDG 2024, canonique)
  - donnees/mcs04_mass_width_2022.mcd  (PDG 2022, g1)
  - donnees/mcs08_allascii_2022.txt    (CODATA 2022, g2 — rapports de masse)
  - donnees/mcs08_allascii_2018.txt    (CODATA 2018, g3 — rapports de masse)

Formule figee (publication 1982, aucun parametre) :
  K = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = 2/3.
Mesure scellee : m = -log10(|K - 2/3| / (2/3)). K est sans dimension :
g6 (unites) est INERTE par construction, rapportee.
Nul N1 : 10 000 triplets tries log-uniformes dans [0,5 ; 2000] MeV.
Sigma = min sur {g1..g6} (g0 canonique hors Sigma).
Seuil de la carte : 3,1 (moteur scelle a 3,0, consigne des deux).

Decisions d'execution publiees :
- g2/g3 : la formule etant sans dimension, les configurations CODATA sont
  evaluees sur les rapports de masse publies (muon-electron, tau-electron) —
  masses = (1 ; r_mu/e ; r_tau/e) ;
- g4/g5 : bornes +1 sigma / -1 sigma publiees de la table PDG 2024 ;
- la fragilite n = 3 est rappelee dans la lecture quelle que soit l'issue.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-11"
SEUIL_CARTE = 3.1
EMPREINTE_CARTE = "7eaad89022d57ab342590196dc79c9ac880792c7879c07ea50e1e29fd2efbe21"
F_PDG24 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2024.mcd")
F_PDG22 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2022.mcd")
F_CO22 = os.path.join(RACINE, "donnees", "mcs08_allascii_2022.txt")
F_CO18 = os.path.join(RACINE, "donnees", "mcs08_allascii_2018.txt")
RESULTATS = os.path.join(RACINE, "resultats", "mcs11_resultats.json")
N_NUL = 10000
CIBLE = 2 / 3
ETENDUE = (0.5, 2000.0)
PANEL = [1 / 3, 1 / 2, 2 / 3, 3 / 4, 4 / 5, (5 ** 0.5 - 1) / 2]


def koide(masses):
    masses = np.asarray(masses, dtype=float)
    return masses.sum() / np.sqrt(masses).sum() ** 2


def mesure(masses, cible=CIBLE):
    return -np.log10(abs(koide(masses) - cible) / cible)


def triplet_libre(gen):
    return np.sort(np.exp(gen.uniform(np.log(ETENDUE[0]),
                                      np.log(ETENDUE[1]), 3)))


def nul_n1(gen, nb=N_NUL):
    return np.array([mesure(triplet_libre(gen)) for _ in range(nb)])


def leptons_pdg(chemin):
    out = {}
    for ln in open(chemin):
        if ln.startswith("*") or not ln.strip():
            continue
        nom_ch = ln[106:].split()
        if nom_ch and nom_ch[0] in ("e", "mu", "tau") and nom_ch[1] == "-":
            toks = ln.split()
            i = next(i for i, t in enumerate(toks)
                     if t[0].isdigit() and ("E" in t or "." in t))
            out[nom_ch[0]] = (float(toks[i]), abs(float(toks[i + 1])),
                              abs(float(toks[i + 2])))
    return np.array([out["e"], out["mu"], out["tau"]])


VAL_RE = re.compile(
    r"^(.{60})\s*(-?[\d][\d\s.]*?\d(?:\.\.\.)?(?:\s*e[+-]?\d+)?)"
    r"\s{2,}(\(exact\)|\S.*?)\s{2,}(.*)$")


def rapports_codata(chemin):
    out = {}
    for ln in open(chemin, encoding="latin-1"):
        for cle in ("muon-electron mass ratio", "tau-electron mass ratio"):
            if ln.startswith(cle):
                m = VAL_RE.match(ln)
                out[cle] = float(m.group(2).replace("...", "").replace(" ", ""))
    return np.array([1.0, out["muon-electron mass ratio"],
                     out["tau-electron mass ratio"]])


def main():
    brut = {f: open(f, "rb").read() for f in
            (F_PDG24, F_PDG22, F_CO22, F_CO18)}
    empreintes = {os.path.basename(f): hashlib.sha256(b).hexdigest()
                  for f, b in brut.items()}
    empreinte_donnees = hashlib.sha256(
        json.dumps(empreintes, sort_keys=True).encode()).hexdigest()
    m24 = leptons_pdg(F_PDG24)
    m22 = leptons_pdg(F_PDG22)
    r22 = rapports_codata(F_CO22)
    r18 = rapports_codata(F_CO18)

    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    z, m_par = {}, {}
    ms0 = nul_n1(gen)
    mu0, u0 = float(ms0.mean()), float(ms0.std())
    m0 = mesure(m24[:, 0])
    m_par["g0_canonique_HORS_SIGMA"] = m0
    z["g0_canonique_HORS_SIGMA"] = mcs.z_score(m0, mu0, u0)

    m_par["g1_pdg2022"] = mesure(m22[:, 0])
    z["g1_pdg2022"] = mcs.z_score(m_par["g1_pdg2022"], mu0, u0)
    m_par["g2_codata2022"] = mesure(r22)
    z["g2_codata2022"] = mcs.z_score(m_par["g2_codata2022"], mu0, u0)
    m_par["g3_codata2018"] = mesure(r18)
    z["g3_codata2018"] = mcs.z_score(m_par["g3_codata2018"], mu0, u0)
    m_par["g4_plus_1sigma"] = mesure(m24[:, 0] + m24[:, 1])
    z["g4_plus_1sigma"] = mcs.z_score(m_par["g4_plus_1sigma"], mu0, u0)
    m_par["g5_moins_1sigma"] = mesure(m24[:, 0] - m24[:, 2])
    z["g5_moins_1sigma"] = mcs.z_score(m_par["g5_moins_1sigma"], mu0, u0)
    # g6 : unites atomiques (m_e = 1) — K sans dimension, INERTE, rapporte
    m_par["g6_unites_atomiques_INERTE"] = mesure(m24[:, 0] / m24[0, 0])
    z["g6_unites_atomiques_INERTE"] = mcs.z_score(
        m_par["g6_unites_atomiques_INERTE"], mu0, u0)

    # controles positifs (unites du nul canonique)
    effet_c1 = (m0 - mesure(triplet_libre(gen))) / u0     # triplet libre
    effet_c2 = (m0 - mesure(m24[:, 0], cible=0.75)) / u0  # cible 3/4

    # diagnostic : panel de rationnels (hors Sigma)
    panel = {str(c): mesure(m24[:, 0], cible=c) for c in PANEL}

    v = mcs.evaluer_v2("DEFAULT", z, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1},
                       exclure=("g0_canonique_HORS_SIGMA",))
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
           "empreintes_fichiers": empreintes,
           "empreinte_donnees": empreinte_donnees,
           "masses_pdg2024_GeV": {"e": m24[0, 0], "mu": m24[1, 0],
                                  "tau": m24[2, 0]},
           "K_canonique": float(koide(m24[:, 0])),
           "ecart_relatif_canonique": float(abs(koide(m24[:, 0]) - CIBLE) / CIBLE),
           "m_par_config": m_par, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "diagnostic_panel_rationnels": panel,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.1": verdict_carte,
           "decisions_execution": [
               "g2/g3 : rapports de masse CODATA (K sans dimension)",
               "g4/g5 : bornes +/-1 sigma publiees PDG 2024"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "K": float(koide(m24[:, 0])),
                      "z_par_g": z, "controles": out["controles"],
                      "panel": panel}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
