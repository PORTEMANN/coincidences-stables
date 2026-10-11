"""mcs14_runner.py — Ouverture de la carte MCS-14 (registre, cristallographie).

Carte scellee : cartes/v2/MCS-14-groupes-espace-cod.md
  sha256 pre-gel : c2202d9245cf30470d9a85d2f0fff653039511331c9834a558f51b5734ab2ff5
Donnees (acquisition a l'ouverture, empreinte au journal) :
  - donnees/mcs14/cod_comptages.csv : effectifs COD par groupe d'espace
    (result.php?space_group_number=N, 1..230 ; colonnes : groupe, total,
    annee_2000)

DEVIATIONS DECLAREES (consignees au journal) :
1. le filtre année de la COD n'existe qu'en année exacte ; g5 ("retrait
   des structures datees > 2000") est opéré comme "structures de l'année
   2000 seule" — même esprit (dépendance a l'époque), substitution declaree ;
2. la limitation de débit du serveur a laissé 45 groupes sans comptage
   annuel après epuisement des tentatives ; g5 est evalue sur les 185
   groupes avec donnée d'année acquise, exclusion publiee dans les
   resultats.

Mesure scellee : m = -log10(RMS(eps)), eps(r) = log10(N_obs(r)+1) -
log10(N_zipf(r)+1), N_zipf(r) = N_tot / (H_k . r), k = nombre de groupes
de la configuration (230 canonique ; 13 monocliniques en g1 ; 36 cubiques
en g2 — recomptes declares).
Nul N1 : 10 000 partitions multinomiales uniformes (meme total, k cases).
Sigma = min sur {g1..g6} (g0 canonique hors Sigma).
Seuil de la carte : 3,0 = seuil DEFAULT du moteur scelle.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-14"
EMPREINTE_CARTE = "c2202d9245cf30470d9a85d2f0fff653039511331c9834a558f51b5734ab2ff5"
DATA = os.path.join(RACINE, "donnees", "mcs14", "cod_comptages.csv")
RESULTATS = os.path.join(RACINE, "resultats", "mcs14_resultats.json")
N_NUL = 10000


def loi_rang(k, n_tot, alpha=1.0):
    r = np.arange(1, k + 1)
    return n_tot / (r ** alpha) / np.sum(1.0 / r ** alpha)


def mesure(effectifs, alpha=1.0, renverser=False):
    effectifs = np.asarray(effectifs, dtype=float)
    k = len(effectifs)
    n_tot = effectifs.sum()
    eff = np.sort(effectifs) if renverser else np.sort(effectifs)[::-1]
    eps = np.log10(eff + 1) - np.log10(loi_rang(k, n_tot, alpha) + 1)
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def nul_n1(gen, n_tot, k, alpha=1.0, nb=N_NUL):
    out = np.empty(nb)
    for i in range(nb):
        part = gen.uniform(0, 1, k)
        part = np.floor(part / part.sum() * n_tot).astype(int)
        out[i] = mesure(part, alpha)
    return out


def z_config(gen, effectifs, alpha=1.0, nb=N_NUL):
    effectifs = np.asarray(effectifs, dtype=int)
    m_val = mesure(effectifs, alpha)
    ms = nul_n1(gen, effectifs.sum(), len(effectifs), alpha, nb)
    return m_val, mcs.z_score(m_val, float(ms.mean()), float(ms.std()))


def alpha_ajuste(effectifs):
    eff = np.sort(effectifs)[::-1]
    sel = eff > 0
    if sel.sum() < 3:
        return None
    r = np.arange(1, len(eff) + 1)[sel]
    A = np.vstack([np.log10(r), np.ones(sel.sum())]).T
    pente, _ = np.linalg.lstsq(A, np.log10(eff[sel]), rcond=None)[0]
    return float(-pente)


def main():
    with open(DATA, "rb") as f:
        brut = f.read()
    empreinte_donnees = hashlib.sha256(brut).hexdigest()
    tot = np.zeros(230, dtype=int)
    y2k = np.zeros(230, dtype=int)
    exclus_g5 = []
    for row in csv.DictReader(brut.decode("utf-8").splitlines()):
        i = int(row["groupe"]) - 1
        tot[i] = int(row["total"])
        if row["annee_2000"] == "NA":
            exclus_g5.append(int(row["groupe"]))
            y2k[i] = -1
        else:
            y2k[i] = int(row["annee_2000"])
    y2k_sel = y2k[y2k >= 0]   # 185 groupes avec donnee d'annee (deviation)

    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    mono = tot[2:15]          # groupes 3-15 (monoclinique)
    cub = tot[194:]           # groupes 195-230 (cubique)
    z, m_par = {}, {}
    m0, z["g0_canonique_HORS_SIGMA"] = z_config(gen, tot)
    m_par["g0_canonique_HORS_SIGMA"] = m0
    u0 = float(nul_n1(gen, tot.sum(), 230, nb=2000).std())

    _, z["g1_monoclinique"] = z_config(gen, mono)
    _, z["g2_cubique"] = z_config(gen, cub)
    _, z["g3_sans_rang1"] = z_config(gen, np.sort(tot)[::-1][1:])
    _, z["g4_alpha_0.5"] = z_config(gen, tot, alpha=0.5)
    _, z["g5_annee_2000_185_groupes"] = z_config(gen, y2k_sel)
    victime = int(gen.uniform(0, 230))
    _, z["g6_retrait_groupe_" + str(victime + 1)] = z_config(
        gen, np.delete(tot, victime))

    # controles positifs (unites du nul canonique)
    effet_c1 = (m0 - mesure(tot, renverser=True)) / u0
    effet_c2 = (m0 - mesure(tot, alpha=2.0)) / u0

    # diagnostics
    ordre = np.argsort(-tot)
    diag = {"alpha_canonique": alpha_ajuste(tot),
            "alpha_monoclinique": alpha_ajuste(mono),
            "alpha_cubique": alpha_ajuste(cub),
            "tete": [{"groupe": int(g + 1), "effectif": int(tot[g])}
                     for g in ordre[:10]]}

    v = mcs.evaluer_v2("DEFAULT", z, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1},
                       exclure=("g0_canonique_HORS_SIGMA",))
    vd = v.to_dict()
    s = vd["sigma"]

    out = {"carte": CARTE_ID, "empreinte_carte_pre_gel": EMPREINTE_CARTE,
           "empreinte_donnees": empreinte_donnees,
           "n_structures_total": int(tot.sum()),
           "m_par_config": m_par, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "diagnostics": diag,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.0": vd["verdict"],
           "exclus_g5_sans_donnee_annee": exclus_g5,
           "deviations_declarees": [
               "g5 : filtre COD en annee exacte — opere sur l'annee 2000 "
               "seule (substitution)",
               "g5 : 45 groupes sans comptage annuel (limitation serveur) "
               "exclus — evalue sur 185 groupes"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict": vd["verdict"],
                      "z_par_g": z, "controles": out["controles"],
                      "diagnostics": diag}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
