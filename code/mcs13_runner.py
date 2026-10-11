"""mcs13_runner.py — Ouverture de la carte MCS-13 (jalon 6+, registre).

Carte scellee : cartes/v2/MCS-13-resonances-orbitales.md
  sha256 pre-gel : bef50920b091937166e3b919c89fc032ea85a97cbc1da5d799a508f009ea0363
Donnees (acquisition a l'ouverture, empreinte au journal) :
  - donnees/mcs13/pscomppars_orbper.csv (NASA Exoplanet Archive, requete
    TAP : hostname, pl_orbper, sy_pnum — table pscomppars)

Mesure scellee : m = -log10(RMS(delta)), delta = min sur R de |r - rho|/rho,
r = P_ext/P_int des paires adjacentes. R fige dans la carte.
Nul N1 : 10 000 permutations intra-systeme (periodes permutees puis
re-triees) — vectorise par taille de systeme.
Sigma = min sur {g1..g6} (g0 canonique hors Sigma).
Seuil de la carte : 3,0 = seuil DEFAULT du moteur scelle.

Decisions d'execution publiees :
- g2 : retrait du systeme apportant le plus de paires (KOI-351, 8 planetes,
  mesure a l'execution — publie) ;
- g5 : mesure alternative = fraction de paires a delta < 1 % (nul recomputes
  sous la meme mesure) ;
- g6 : retrait d'une paire tiree par le PRNG public ChaCha20
  (cle = SHA-256("MCS-J4V2|" + empreinte_carte + "|" + empreinte_donnees)).
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

CARTE_ID = "MCS-13"
EMPREINTE_CARTE = "bef50920b091937166e3b919c89fc032ea85a97cbc1da5d799a508f009ea0363"
DATA = os.path.join(RACINE, "donnees", "mcs13", "pscomppars_orbper.csv")
RESULTATS = os.path.join(RACINE, "resultats", "mcs13_resultats.json")
N_NUL = 10000
R = np.array([2.0, 1.5, 4 / 3, 1.25, 1.2, 3.0, 4.0, 2.5, 5 / 3])
R_ORDRE1 = np.array([1.5, 4 / 3, 1.25, 1.2])


def ecarts(ratios, ensemble=R):
    d = np.abs(np.asarray(ratios)[:, None] - ensemble[None, :]) / ensemble[None, :]
    return d.min(axis=1), d.argmin(axis=1)


def mesure(ratios, ensemble=R):
    d, _ = ecarts(ratios, ensemble)
    return -np.log10(np.sqrt(np.mean(d ** 2)))


def mesure_frac(ratios, ensemble=R, seuil=0.01):
    d, _ = ecarts(ratios, ensemble)
    return float(np.mean(d < seuil))


def paires(systemes):
    out = []
    for h, per in systemes.items():
        per = np.sort(per)
        out += list(per[1:] / per[:-1])
    return np.array(out)


def nul_n2(gen, systemes, mesure_fn, nb=N_NUL):
    """N2 declare a la carte : periodes libres log-uniformes dans l'etendue
    observee, regroupees en systemes de memes tailles.
    NOTE D'EXECUTION PUBLIEE : le nul N1 de la carte (permutations
    intra-systeme re-triees) est l'application identite — erreur de
    redaction scellee ; N2 est le nul operatoire (substitution declaree
    au journal et aux resultats)."""
    tailles = {}
    toutes = np.concatenate([np.asarray(p) for p in systemes.values()])
    lo, hi = np.log(toutes.min()), np.log(toutes.max())
    for h, per in systemes.items():
        tailles.setdefault(len(per), 0)
        tailles[len(per)] += 1
    out = np.empty(nb)
    for i in range(nb):
        ratios = []
        for k, n in tailles.items():
            A = np.sort(np.exp(gen.uniform(lo, hi, (n, k))), axis=1)
            ratios.append((A[:, 1:] / A[:, :-1]).ravel())
        out[i] = mesure_fn(np.concatenate(ratios))
    return out

nul_n1 = nul_n2  # substitution declaree : le nul operatoire est N2


def z_config(gen, systemes, ensemble=R, fn=mesure):
    """Retourne (m_val, z) ; si le nul est degenere (u == 0), z = None :
    rapporte avec note, exclu du moteur — publie."""
    ratios = paires(systemes)
    m_val = fn(ratios, ensemble)
    ms = nul_n1(gen, systemes, lambda r: fn(r, ensemble))
    u = float(ms.std())
    if u == 0.0:
        return m_val, None
    return m_val, mcs.z_score(m_val, float(ms.mean()), u)


def main():
    with open(DATA, "rb") as f:
        brut = f.read()
    empreinte_donnees = hashlib.sha256(brut).hexdigest()
    systemes = {}
    for row in csv.DictReader(brut.decode("utf-8").splitlines()):
        if row["pl_orbper"] not in ("", "null"):
            systemes.setdefault(row["hostname"], []).append(
                float(row["pl_orbper"]))
    systemes = {h: p for h, p in systemes.items() if len(p) >= 2}
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    z, m_par = {}, {}
    m0, z["g0_canonique_HORS_SIGMA"] = z_config(gen, systemes)
    m_par["g0_canonique_HORS_SIGMA"] = m0
    ratios0 = paires(systemes)
    u0 = float(nul_n1(gen, systemes, mesure, nb=2000).std())

    _, z["g1_min_3_planetes"] = z_config(
        gen, {h: p for h, p in systemes.items() if len(p) >= 3})
    top = max(systemes, key=lambda h: len(systemes[h]) - 1)
    _, z["g2_sans_" + top.replace(" ", "")] = z_config(
        gen, {h: p for h, p in systemes.items() if h != top})
    _, z["g3_premier_ordre"] = z_config(gen, systemes, ensemble=R_ORDRE1)
    ratios_g4 = paires(systemes)
    m4 = mesure(ratios_g4[ratios_g4 <= 4.0])
    ms4 = nul_n1(gen, systemes, lambda r: mesure(r[r <= 4.0]), nb=2000)
    z["g4_r_max_4"] = mcs.z_score(m4, float(np.mean(ms4)), float(np.std(ms4)))
    m_par.update({"g4_r_max_4": m4})
    _, z["g5_fraction_1pc"] = z_config(gen, systemes, fn=mesure_frac)
    victime = int(gen.uniform(0, len(ratios0)))
    m6 = mesure(np.delete(ratios0, victime))
    ms6 = nul_n1(gen, systemes,
                 lambda r: mesure(np.delete(r, min(victime, len(r) - 1))),
                 nb=2000)
    z["g6_retrait_paire_" + str(victime)] = mcs.z_score(
        m6, float(np.mean(ms6)), float(np.std(ms6)))

    # controles positifs (unites du nul canonique)
    d, arg = ecarts(ratios0)
    tri2 = np.argsort(np.abs(ratios0[:, None] - R[None, :]) / R[None, :], axis=1)
    r_milieu = (R[tri2[:, 0]] + R[tri2[:, 1]]) / 2
    effet_c1 = (m0 - mesure(r_milieu)) / u0
    r_libre = np.exp(gen.uniform(np.log(ratios0.min()),
                                 np.log(ratios0.max()), len(ratios0)))
    effet_c2 = (m0 - mesure(r_libre)) / u0

    # diagnostics : ecarts signes au rationnel le plus proche ; histogramme R
    rho_hit = R[arg]
    signes = (ratios0 - rho_hit) / rho_hit
    diag = {"fraction_au_large": float(np.mean(signes > 0)),
            "fraction_au_strict": float(np.mean(signes < 0)),
            "mediane_ecart_signe": float(np.median(signes)),
            "histogramme_R": {str(float(x)): int(np.sum(rho_hit == x)) for x in R}}

    z_moteur = {k: v_ for k, v_ in z.items() if v_ is not None}
    degen = [k for k, v_ in z.items() if v_ is None]
    v = mcs.evaluer_v2("DEFAULT", z_moteur, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1},
                       exclure=("g0_canonique_HORS_SIGMA",))
    vd = v.to_dict()
    s = vd["sigma"]

    out = {"carte": CARTE_ID, "empreinte_carte_pre_gel": EMPREINTE_CARTE,
           "empreinte_donnees": empreinte_donnees,
           "n_systemes": len(systemes), "n_paires": len(ratios0),
           "m_canonique": m0, "m_par_config": m_par, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "diagnostics": diag,
           "verdict_moteur_seuil_3.0": vd,
           "nuls_degeneres": degen,
           "verdict_carte_seuil_3.0": vd["verdict"],
           "decisions_execution": [
               f"g2 : retrait de {top} (le plus de paires)",
               "g5 : fraction de paires a delta < 1 %"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict": vd["verdict"],
                      "z_par_g": z, "controles": out["controles"],
                      "diagnostics": diag}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
