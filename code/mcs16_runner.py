"""mcs16_runner.py — Ouverture de la carte MCS-16 (la récolte du corpus).

Carte scellee : cartes/v2/MCS-16-ratios-masses-corpus.md
  sha256 pre-gel : fd0b290b655ddd225d91dd1f97b0b4872d94bb5a078b13ab5bbeb28f3a938ed1
Regles figees citees du bilan gele du chantier LOI-HARMONIQUE de mvcg
(PORTEMANN/mvcg, docs/CHANTIER-LOI-HARMONIQUE-BILAN.md, blob GitHub
3af2be88ec338f9b6f24523e592aa71c8ded74a2) — les six regles sont ecrites
ici AVANT tout calcul, avec leurs mots mvcg publies.

Donnees (deja acquises et empreintees au depot — reutilisation consignee) :
  - donnees/mcs04_mass_width_2024.mcd / _2022.mcd (PDG, masses)
  - donnees/mcs08_allascii_2022.txt / _2018.txt (CODATA, alpha)

Mesure scellee : m = -log10(RMS(log10(pred/mesure))) sur les six regles.
Nul N1 : 10 000 permutations des masses mesurees entre les regles.
Sigma = min sur {g1..g6} (g0 canonique hors Sigma).
Seuil de la carte : 3,2 (moteur a 3,0, consigne des deux).

Decisions d'execution publiees :
- g1 : la table PDG 2022 ne contient pas les quarks legers u/s/c ; la
  deformation porte sur les ratios dont les deux editions portent la masse
  (muon, Z, bottom) — declare ;
- la regle bottom utilise m_c^corps = 1251,029 MeV (chaine interne gelee
  du corpus — pas la valeur PDG) ;
- masses en MeV partout ; quarks MS-bar a 2 GeV (valeurs de la table PDG).
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

CARTE_ID = "MCS-16"
SEUIL_CARTE = 3.2
EMPREINTE_CARTE = "fd0b290b655ddd225d91dd1f97b0b4872d94bb5a078b13ab5bbeb28f3a938ed1"
F_PDG24 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2024.mcd")
F_PDG22 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2022.mcd")
F_CO22 = os.path.join(RACINE, "donnees", "mcs08_allascii_2022.txt")
F_CO18 = os.path.join(RACINE, "donnees", "mcs08_allascii_2018.txt")
RESULTATS = os.path.join(RACINE, "resultats", "mcs16_resultats.json")
N_NUL = 10000
M_C_CORPS = 1251.029   # valeur gelee du corpus (regle 4, chaine declaree)
NOMS = ["muon_quinte", "Z_diagonale", "strange_quarte", "bottom_G6",
        "up_G3", "charm_G5"]

VAL_RE = re.compile(
    r"^(.{60})\s*(-?[\d][\d\s.]*?\d(?:\.\.\.)?(?:\s*e[+-]?\d+)?)"
    r"\s{2,}(\(exact\)|\S.*?)\s{2,}(.*)$")


def masses_pdg(chemin):
    """Masses en MeV ; parse par tokens (les .mcd sont a colonnes fixes)."""
    cibles = {"e", "mu", "tau", "u", "d", "s", "c", "b", "t", "W", "Z",
              "H", "p", "n"}
    out = {}
    for ln in open(chemin):
        if ln.startswith("*") or not ln.strip():
            continue
        nom_ch = ln[106:].split()
        if nom_ch and nom_ch[0] in cibles:
            toks = ln.split()
            try:
                i = next(i for i, t in enumerate(toks)
                         if t[0].isdigit() and ("E" in t or "." in t))
                out[nom_ch[0]] = float(toks[i]) * 1000.0  # GeV -> MeV
            except (ValueError, StopIteration):
                continue
    return out


def alpha_codata(chemin):
    for ln in open(chemin, encoding="latin-1"):
        if ln.startswith("fine-structure constant ") or            ln.startswith("fine-structure constant	"):
            m = VAL_RE.match(ln)
            return float(m.group(2).replace("...", "").replace(" ", ""))
    for ln in open(chemin, encoding="latin-1"):
        if ln.startswith("fine-structure constant"):
            m = VAL_RE.match(ln)
            return float(m.group(2).replace("...", "").replace(" ", ""))
    raise ValueError("alpha introuvable")


def regles(m_p, m_e, alpha):
    """Les six regles figees du corpus (aucune constante recalibree)."""
    return np.array([
        m_e * (3 / 2) / alpha,            # 1 muon quinte (S+ 0,59 %)
        m_p / (alpha * np.sqrt(2)),       # 2 Z diagonale (S+ 0,30 %)
        m_p / 9,                          # 3 strange quarte (P 12,1 %)
        4 * M_C_CORPS / 2 ** (1 / 12),    # 4 bottom G6 (P 13,0 %)
        (m_p / 18) * np.sqrt(alpha) / 2,  # 5 up G3 (S+ 3,1 %)
        24 * m_p / 18,                    # 6 charm G5 (S+ 1,5 %)
    ])


def mesure(pred, obs):
    eps = np.log10(pred) - np.log10(obs)
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def nul_n1(gen, pred, obs, nb=N_NUL):
    return np.array([mesure(pred, gen.permutation(obs)) for _ in range(nb)])


def main():
    brut = {f: open(f, "rb").read() for f in (F_PDG24, F_PDG22, F_CO22, F_CO18)}
    empreintes = {os.path.basename(f_): hashlib.sha256(b).hexdigest()
                  for f_, b in brut.items()}
    empreinte_donnees = hashlib.sha256(
        json.dumps(empreintes, sort_keys=True).encode()).hexdigest()
    m24, m22 = masses_pdg(F_PDG24), masses_pdg(F_PDG22)
    a22, a18 = alpha_codata(F_CO22), alpha_codata(F_CO18)

    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    pred = regles(m24["p"], m24["e"], a22)
    obs = np.array([m24["mu"], m24["Z"], m24["s"], m24["b"], m24["u"],
                    m24["c"]])

    z, m_par = {}, {}
    ms0 = nul_n1(gen, pred, obs)
    mu0, u0 = float(ms0.mean()), float(ms0.std())
    m0 = mesure(pred, obs)
    z["g0_canonique_HORS_SIGMA"] = mcs.z_score(m0, mu0, u0)
    m_par["g0_canonique_HORS_SIGMA"] = m0

    def zconf(pred_, obs_, nom):
        m_ = mesure(pred_, obs_)
        ms = nul_n1(gen, pred_, obs_)
        z[nom] = mcs.z_score(m_, float(ms.mean()), float(ms.std()))
        m_par[nom] = m_

    # g1 : PDG 2022 (ratios dont les deux editions portent la masse)
    sel1 = [0, 1, 3]   # muon, Z, bottom — u/s/c absents de la table 2022
    pred22 = regles(m22["p"], m22["e"], a22)
    obs22 = np.array([m22["mu"], m22["Z"], m22["b"]])
    zconf(pred22[sel1], obs22, "g1_pdg2022_intersection")
    # g2 : alpha 2018
    zconf(regles(m24["p"], m24["e"], a18), obs, "g2_alpha_2018")
    # g3 : sans muon ; g4 : sans bottom ; g5 : sans strange+bottom
    zconf(pred[[1, 2, 3, 4, 5]], obs[[1, 2, 3, 4, 5]], "g3_sans_muon")
    zconf(pred[[0, 1, 2, 4, 5]], obs[[0, 1, 2, 4, 5]], "g4_sans_bottom")
    zconf(pred[[0, 1, 4, 5]], obs[[0, 1, 4, 5]], "g5_sans_zone_grise")
    # g6 : retrait d'une regle au hasard
    victime = int(gen.uniform(0, 6))
    sel6 = [i for i in range(6) if i != victime]
    zconf(pred[sel6], obs[sel6], "g6_sans_" + NOMS[victime])

    # controles positifs (unites du nul canonique)
    effet_c1 = (m0 - mesure(pred, gen.permutation(obs))) / u0
    effet_c2 = (m0 - mesure(pred * 1.05, obs)) / u0

    # diagnostic : ecart par regle (l'information honnete)
    eps = {NOMS[i]: float(np.log10(pred[i]) - np.log10(obs[i]))
           for i in range(6)}

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
           "alpha_2022": a22, "alpha_2018": a18,
           "masses_pdg2024_MeV": {k: m24[k] for k in
                                  ("e", "mu", "p", "Z", "s", "b", "u", "c")},
           "predictions_regles": dict(zip(NOMS, pred.tolist())),
           "ecarts_par_regle_dex": eps,
           "m_par_config": m_par, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.2": verdict_carte,
           "decisions_execution": [
               "g1 : intersection des editions (muon, Z, bottom)",
               "regle 4 : m_c^corps = 1251,029 MeV (chaine interne gelee)"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z, "controles": out["controles"],
                      "ecarts_dex": eps}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
