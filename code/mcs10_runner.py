"""mcs10_runner.py — Ouverture de la carte MCS-10 (jalon 5).

Carte scellee : cartes/v2/MCS-10-rar-sparc.md
  sha256 pre-gel : c9c9d6fdf4841ffe4e2cf37b2e447372a4ef48bad502ff58abc053aadf668089
Donnees figees (acquisition a l'ouverture, empreintes au journal) :
  - donnees/mcs10/MassModels_Lelli2016c.mrt (courbes de rotation + profils)
  - donnees/mcs10/SPARC_Lelli2016c.mrt      (table principale : D, f_D, Inc, Q)

Relation figee (publication 2016, aucun reajustement) :
  g_RAR(g) = g / (1 - exp(-sqrt(g / g-dagger))), g-dagger = 1,2e-10 m/s2.
Conventions declarees : U_disk = 0,5, U_bulge = 0,7 ; g_bar = (|Vg|Vg +
U_d|Vd|Vd + U_b|Vb|Vb) / r ; g_obs = Vobs^2 / r ; unites SI.

Mesure scellee : m = -log10(RMS(log10 g_obs - log10 g_RAR(g_bar))),
points a g_bar > 0. Nul N1 : 10 000 permutations des profils baryoniques
entre galaxies. Sigma = min sur {g1..g6} (g0 canonique hors Sigma).
Seuil de la carte : 3,1 (moteur scelle a 3,0, consigne des deux).

Decisions d'execution publiees :
- g5 : "distance de qualite etoile" = f_D dans {2, 3} (TRGB, Cepheides —
  codes publies de la base).
- g6 : retrait d'une galaxie tiree par le PRNG public ChaCha20
  (cle = SHA-256("MCS-J4V2|" + empreinte_carte + "|" + empreinte_donnees)).
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

CARTE_ID = "MCS-10"
SEUIL_CARTE = 3.1
EMPREINTE_CARTE = "c9c9d6fdf4841ffe4e2cf37b2e447372a4ef48bad502ff58abc053aadf668089"
DATA = os.path.join(RACINE, "donnees", "mcs10")
RESULTATS = os.path.join(RACINE, "resultats", "mcs10_resultats.json")
N_NUL = 10000
GDAG = 1.2e-10
UD, UB = 0.5, 0.7
KPC_M = 3.0856776e19


def g_rar(g_bar, gdag=GDAG):
    return g_bar / (1 - np.exp(-np.sqrt(np.maximum(g_bar, 1e-30) / gdag)))


def mesure(g_obs, g_bar, gdag=GDAG):
    ok = g_bar > 0
    eps = np.log10(g_obs[ok]) - np.log10(g_rar(g_bar[ok], gdag))
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def lire_modeles():
    gals = {}
    for ln in open(os.path.join(DATA, "MassModels_Lelli2016c.mrt")):
        p = ln.split()
        if len(p) < 8:
            continue
        try:
            d, r, vo, ev, vg, vd, vb = (float(x) for x in p[1:8])
        except ValueError:
            continue
        g = gals.setdefault(p[0], {"r": [], "vo": [], "vg": [], "vd": [], "vb": []})
        g["r"].append(r); g["vo"].append(vo)
        g["vg"].append(vg); g["vd"].append(vd); g["vb"].append(vb)
    for g in gals.values():
        for k in g:
            g[k] = np.array(g[k])
    return gals


def lire_table():
    # parse par tokens (les colonnes fixes du byte-by-byte sont decalees
    # dans le fichier reel) : nom T D e_D f_D Inc ... Q Ref
    tab = {}
    for ln in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        p = ln.split()
        if len(p) < 18 or not p[0][0].isalpha():
            continue
        try:
            tab[p[0]] = {"f_D": int(p[4]), "Inc": float(p[5]),
                         "Q": int(p[-2])}
        except ValueError:
            continue
    return tab


def assembler(gals, tab, noms, ud=UD, rmin=0.0):
    Go, Gb, Gg, prop = [], [], [], []
    for nom in noms:
        g = gals[nom]
        ok = g["r"] >= rmin
        r = g["r"][ok] * KPC_M
        Go.append((g["vo"][ok] * 1e3) ** 2 / r)
        Gb.append((np.abs(g["vg"][ok]) * g["vg"][ok] +
                   ud * np.abs(g["vd"][ok]) * g["vd"][ok] +
                   UB * np.abs(g["vb"][ok]) * g["vb"][ok]) * 1e6 / r)
        Gg.append((np.abs(g["vg"][ok]) * g["vg"][ok]) * 1e6 / r)
        prop += [nom] * int(ok.sum())
    return (np.concatenate(Go), np.concatenate(Gb),
            np.concatenate(Gg), np.array(prop))


def nul_n1(gen, g_obs, blocks_gbar, nb=N_NUL):
    """Permutations des profils baryoniques entre galaxies (blocs)."""
    n = len(blocks_gbar)
    out = np.empty(nb)
    for i in range(nb):
        perm = gen.permutation(np.arange(n))
        gb = np.concatenate([blocks_gbar[j] for j in perm])
        out[i] = mesure(g_obs, gb)
    return out


def main():
    empreintes = {f: hashlib.sha256(
        open(os.path.join(DATA, f), "rb").read()).hexdigest()
        for f in sorted(os.listdir(DATA))}
    empreinte_donnees = hashlib.sha256(
        json.dumps(empreintes, sort_keys=True).encode()).hexdigest()
    gals, tab = lire_modeles(), lire_table()
    noms = sorted(gals)
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    z, m_par = {}, {}

    def config(nom_cle, noms_c, ud=UD, rmin=0.0):
        go, gb, gg, prop = assembler(gals, tab, noms_c, ud, rmin)
        m_val = mesure(go, gb)
        blocks = [gb[prop == n] for n in noms_c]
        ms = nul_n1(gen, go, blocks)
        z[nom_cle] = mcs.z_score(m_val, float(ms.mean()), float(ms.std()))
        m_par[nom_cle] = m_val
        return go, gb, gg, prop, float(ms.std())

    go0, gb0, gg0, prop0, u0 = config("g0_canonique_HORS_SIGMA", noms)
    config("g1_qualite_Q1", [n for n in noms if tab.get(n, {}).get("Q") == 1])
    config("g2_upsilon_d_0.7", noms, ud=0.7)
    config("g3_inclinaison_30", [n for n in noms
                                 if tab.get(n, {}).get("Inc", 0) >= 30])
    config("g4_r_min_1kpc", noms, rmin=1.0)
    config("g5_distances_etoiles", [n for n in noms
                                    if tab.get(n, {}).get("f_D") in (2, 3)])
    victime = int(gen.uniform(0, len(noms)))
    config("g6_retrait_" + noms[victime],
           [n for i, n in enumerate(noms) if i != victime])

    # controles positifs (unites du nul canonique)
    g_c1 = np.concatenate([gen.permutation(go0[prop0 == n]) for n in noms])
    effet_c1 = (m_par["g0_canonique_HORS_SIGMA"] - mesure(g_c1, gb0)) / u0
    effet_c2 = (m_par["g0_canonique_HORS_SIGMA"]
                - mesure(go0, gb0, gdag=2 * GDAG)) / u0

    # diagnostics (hors Sigma)
    diag = {"m_gaz_seul": mesure(go0, gg0),
            "rms_intra_median_dex": float(np.median([
                np.sqrt(np.mean((np.log10(go0[prop0 == n])
                                 - np.log10(g_rar(gb0[prop0 == n]))) ** 2))
                for n in noms]))}

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
           "n_galaxies": len(noms), "n_points": len(go0),
           "m_par_config": m_par, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "diagnostics": diag,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.1": verdict_carte,
           "decisions_execution": [
               "g5 : f_D dans {2, 3} (TRGB, Cepheides)",
               "g6 : retrait PRNG public"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z, "controles": out["controles"],
                      "diagnostics": diag, "n_galaxies": len(noms),
                      "n_points": len(go0)}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
