"""mcs25_runner.py — Ouverture de la carte MCS-25 (siege du vide x canal
leptonique, nul reel spectral).

Carte scelle : cartes/v2/MCS-25-siege-vide-table-fermions.md
  sha256 pre-gel : e1e4e0728fa3b2849e25f906c8bf1fd0c1d68f9a417bb71a96a91be5bf40b546
Donnees : tables PDG deja acquises (MCS-04/16 — empreintes reconsignees) ;
  contenu : le porteur a son vide (r = (3+sqrt5)/2 — forme close du spectre
  mesure T7, declaree) ; le nul reel spectral : enumeration exhaustive des
  matrices verifiees de la fenetre (code/spectres_triplets.py — hache dans
  l'acte de gel ; regression tuante aux comptes publies de MCS-24).

Mesure scelle : s(x) = min_R |log10(x/R)| sur le canal {mu/e, tau/mu, tau/e}
  (regle de forme spectrale — correction pre-gel declaree unique, demo v1
  impuissante publiee) ; m = -s. Nul N1 : distribution de s(D) sur toutes
  les matrices verifiees, chaque matrice comptee une fois (exacte).
Controles d'instrument (correction declaree) : c1 : reference plantee sur
  mu/e puis deplacee au centre geometrique du plus grand intervalle de la
  table ; c2 : reference tiree du nul (PRNG public, echantillonnage inverse
  — convention MCS-24).

Seuil de la carte : 3,0 (moteur scelle a 3,0, consigne des deux).
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402
import spectres_triplets as st  # noqa: E402

CARTE_ID = "MCS-25"
SEUIL_CARTE = 3.0
EMPREINTE_CARTE = "e1e4e0728fa3b2849e25f906c8bf1fd0c1d68f9a417bb71a96a91be5bf40b546"
RESULTATS = os.path.join(RACINE, "resultats", "mcs25_resultats.json")
F_PDG24 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2024.mcd")
F_PDG22 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2022.mcd")
CANAL = ("e", "mu", "tau")

# Contenus geles (declarations de la carte) :
R_VIDE = (3 + np.sqrt(5)) / 2          # porteur au vide T7 (rho = sqrt5)
R_G3 = 5.0                             # vide deplace rho = 1,5 (declare)
R_G4 = ((np.sqrt(32) + 1) / (np.sqrt(32) - 1))   # point Lambda=6 (T12)


def masses_pdg(chemin):
    """Parseur de MCS-16 (filiation declaree), masses en MeV."""
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


def table_rapports(masses, objets):
    vals = [masses[o] for o in objets]
    rs = [a / b for a, b in itertools.permutations(vals, 2) if a > b]
    return np.array(sorted(rs))


def sieges(rapports, table, metrique="log"):
    if metrique == "log":
        d = np.abs(np.log10(rapports[:, None] / table[None, :]))
    else:
        d = np.abs(rapports[:, None] - table[None, :]) / table[None, :]
    return d.min(axis=1)


def centre_plus_grand_intervalle(table):
    lt = np.log10(table)
    i = int(np.argmax(np.diff(lt)))
    return float(10 ** ((lt[i] + lt[i + 1]) / 2))


def mu_u_poids(m_par_taille, poids):
    tailles = sorted(m_par_taille)
    stats = [(float(m_par_taille[n].mean()), float(m_par_taille[n].var()))
             for n in tailles]
    if poids == "uniforme":
        w = np.ones(len(tailles)) / len(tailles)
    else:
        w = np.array([len(m_par_taille[n]) for n in tailles], dtype=float)
        w /= w.sum()
    mu = float(sum(wi * mi for wi, (mi, _) in zip(w, stats)))
    var = float(sum(wi * (vi + (mi - mu) ** 2)
                    for wi, (mi, vi) in zip(w, stats)))
    return mu, float(np.sqrt(var))


def main():
    brut = {f: open(f, "rb").read() for f in (F_PDG24, F_PDG22)}
    empreintes = {os.path.basename(f_): hashlib.sha256(b).hexdigest()
                  for f_, b in brut.items()}
    constants = {"canal": CANAL, "R_VIDE": R_VIDE, "R_G3": R_G3,
                 "R_G4": R_G4, "fenetre": [2, 6], "fenetre_g2": [2, 7],
                 "empreintes_tables": empreintes}
    empreinte_donnees = hashlib.sha256(
        json.dumps(constants, sort_keys=True, default=list).encode()
        ).hexdigest()
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode())
        .digest())

    m24 = masses_pdg(F_PDG24)
    m22 = masses_pdg(F_PDG22)
    t24 = table_rapports(m24, CANAL)
    t22 = table_rapports(m22, CANAL)

    print("Nul reel spectral (enumeration exhaustive, chemin vectorise) :")
    sp6 = st.spectres_par_taille(6, vect=True)
    assert st.regression_comptes(sp6), "REGRESSION MCS-24 TUEE"
    sp7 = st.spectres_par_taille(7, n_min=7, vect=True)
    assert sp7[7][0] == st.COMPTES_MCS24[7], "REGRESSION MCS-24 TUEE (n=7)"
    comptes = {int(n): int(sp6[n][0]) for n in sp6}
    comptes[7] = int(sp7[7][0])
    print("  comptes par taille (regression MCS-24 PASS) :", comptes)

    def m_par_taille(sp, table, metrique):
        return {n: -sieges(sp[n][1], table, metrique) for n in sp}

    m0t = m_par_taille(sp6, t24, "log")
    mu0, u0 = mu_u_poids(m0t, "naturel")
    nul = {"g1": mu_u_poids(m_par_taille(sp6, t22, "log"), "naturel"),
           "g5": mu_u_poids(m_par_taille(sp6, t24, "rel"), "naturel"),
           "g6": mu_u_poids(m0t, "uniforme")}
    sp67 = dict(sp6); sp67[7] = sp7[7]
    nul["g2"] = mu_u_poids(m_par_taille(sp67, t24, "log"), "naturel")

    def z_conf(r, mu, u):
        m_val = -float(sieges(np.array([r]), t24)[0])
        return m_val, mcs.z_score(m_val, mu, u)

    z_par, m_par, rangs = {}, {}, {}
    m0 = -float(sieges(np.array([R_VIDE]), t24)[0])
    z_par["g0_canonique_HORS_SIGMA"] = mcs.z_score(m0, mu0, u0)
    m_par["g0"] = m0
    m_cat = np.concatenate([m0t[n] for n in sorted(m0t)])
    rangs["g0"] = float(np.mean(m_cat >= m0))
    m1 = -float(sieges(np.array([R_VIDE]), t22)[0])
    z_par["g1_edition_2022"] = mcs.z_score(m1, *nul["g1"])
    m_par["g1"] = m1
    m2 = m0
    z_par["g2_fenetre_7"] = mcs.z_score(m2, *nul["g2"])
    m_par["g2"] = m2
    m3 = -float(sieges(np.array([R_G3]), t24)[0])
    z_par["g3_vide_deplace_rho1.5"] = mcs.z_score(m3, mu0, u0)
    m_par["g3"] = m3
    m4 = -float(sieges(np.array([R_G4]), t24)[0])
    z_par["g4_point_branche_L6"] = mcs.z_score(m4, mu0, u0)
    m_par["g4"] = m4
    m5 = -float(sieges(np.array([R_VIDE]), t24, "rel")[0])
    z_par["g5_metrique_relative"] = mcs.z_score(m5, *nul["g5"])
    m_par["g5"] = m5
    z_par["g6_poids_uniforme_taille"] = mcs.z_score(m0, *nul["g6"])
    m_par["g6"] = m0

    # controles d'instrument (references — correction declaree)
    r_plante = m24["mu"] / m24["e"]
    assert abs(sieges(np.array([r_plante]), t24)[0]) < 1e-12
    r_gap = centre_plus_grand_intervalle(t24)
    m_gap = -float(sieges(np.array([r_gap]), t24)[0])
    effet_c1 = (0.0 - m_gap) / u0
    m_tries = np.sort(m_cat)
    u_draw = float(gen.uniform(0.0, 1.0))
    m_c2 = float(m_tries[min(int(u_draw * len(m_tries)), len(m_tries) - 1)])
    effet_c2 = (0.0 - m_c2) / u0

    # N2 : masses du canal permutees — exhaustif (6 permutations, declare)
    n2 = []
    for perm in itertools.permutations(CANAL):
        tp = table_rapports(m24, list(perm))
        n2.append(-float(sieges(np.array([R_VIDE]), tp)[0]))
    n2 = sorted(set(round(v, 12) for v in n2))

    # diagnostic : siege dans la table complete des fermions (demo v1)
    t_full = table_rapports(m24, ("u", "d", "s", "c", "b", "e", "mu", "tau"))
    siege_full = float(sieges(np.array([R_VIDE]), t_full)[0])

    diag = {"siege_porteur_dex": -m0,
            "rapport_le_plus_proche_canal": float(
                t24[np.argmin(np.abs(np.log10(t24 / R_VIDE)))]),
            "siege_porteur_table_complete_dex": siege_full,
            "rapport_le_plus_proche_table_complete": float(
                t_full[np.argmin(np.abs(np.log10(t_full / R_VIDE)))]),
            "rangs_dans_le_nul_reel": rangs,
            "comptes_nul_par_taille": {str(k): v for k, v in comptes.items()},
            "n2_permutations_canal_m": n2,
            "nuls_par_config": {k: list(v) for k, v in nul.items()},
            "nul_canonique": [mu0, u0],
            "note": "le canal leptonique est la correction declaree ; la "
                    "table complete est publiee en diagnostic (demo v1 "
                    "impuissante — plafond mesure 1,46)"}

    v = mcs.evaluer_v2("DEFAULT", z_par, {"c1": effet_c1, "c2": effet_c2},
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
           "constantes_gelees": constants,
           "empreinte_donnees": empreinte_donnees,
           "m_par_config": m_par, "z_par_g": z_par,
           "controles": {"c1": effet_c1, "c2": effet_c2,
                         "reference_c1_gap": r_gap},
           "diagnostics": diag,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.0": verdict_carte,
           "decisions_execution": [
               "le nul reel spectral est enumere exhaustivement (chemin "
               "vectorise declare) — jamais tire",
               "controles d'instrument sur references (correction "
               "declaree) : c1 = siege parfait deplace au plus grand "
               "intervalle ; c2 = tirage du nul par echantillonnage "
               "inverse (convention MCS-24)",
               "N2 est exhaustif (6 permutations du canal — declare)"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z_par, "controles": out["controles"],
                      "siege_porteur_dex": -m0}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
