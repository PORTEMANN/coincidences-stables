"""demonstration_puissance_mcs10.py — Regle 1.2 pour la carte MCS-10.

Galaxies synthetiques plantees sur la relation figee (dispersion 0,13 dex
declaree) -> CS+ attendu (Sigma >= 3,1), controles resolus a |effet| >= 2 u ;
appariements libres -> CS- attendu ; banc aveugle -> CS0.
Graine : 20261011 (numpy — synthetique). Journal chaine dedie.
"""
from __future__ import annotations

import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402

GRAINE = 20261011
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs10.jsonl")
GDAG = 1.2e-10          # g-dagger gelee (publication 2016)
UD, UB = 0.5, 0.7       # conventions SPARC declarees


def g_rar(g_bar, gdag=GDAG):
    return g_bar / (1 - np.exp(-np.sqrt(np.maximum(g_bar, 1e-30) / gdag)))


def mesure(g_obs, g_bar, gdag=GDAG):
    ok = g_bar > 0
    eps = np.log10(g_obs[ok]) - np.log10(g_rar(g_bar[ok], gdag))
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def echantillon_plante(rng, n_gal=100, n_pts=20):
    """Galaxies plantees sur la relation figee, dispersion 0,13 dex."""
    G_obs, G_bar, proprietaires = [], [], []
    for i in range(n_gal):
        # masse tres variable : g_bar balaie la transition a g-dagger
        echelle = 10 ** rng.uniform(-1.5, 0.5)
        vgas = np.abs(rng.normal(40, 25, n_pts)) * echelle
        vdisk = np.abs(rng.normal(90, 40, n_pts)) * echelle
        vbul = np.abs(rng.normal(20, 15, n_pts)) * echelle
        g_bar = ((vgas ** 2 + UD * vdisk ** 2 + UB * vbul ** 2) * 3.086e16 / (
            np.arange(1, n_pts + 1) * 3.086e19)) * 2e-9   # echelle SI declaree
        g_obs = g_rar(g_bar) * 10 ** (0.13 * rng.normal(0, 1, n_pts))
        G_obs.append(g_obs); G_bar.append(g_bar)
        proprietaires.append(np.full(n_pts, i))
    return (np.concatenate(G_obs), np.concatenate(G_bar),
            np.concatenate(proprietaires))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS10")

    g_obs, g_bar, prop = echantillon_plante(rng)
    m_reel = mesure(g_obs, g_bar)
    # N1 : profils permutes entre galaxies (blocs de 20 points)
    n_gal = prop.max() + 1
    ms_n1 = []
    for _ in range(2000):
        perm = rng.permutation(n_gal)
        gb_perm = np.concatenate([g_bar[prop == perm[i]] for i in range(n_gal)])
        ms_n1.append(mesure(g_obs, gb_perm))
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : radii permutes au sein de chaque galaxie
    g_c1 = np.concatenate([rng.permutation(g_obs[prop == i]) for i in range(n_gal)])
    effet_c1 = (m_reel - mesure(g_c1, g_bar)) / u
    # c2 : echelle doublee
    effet_c2 = (m_reel - mesure(g_obs, g_bar, gdag=2 * GDAG)) / u
    v = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    seuil_carte = 3.1
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-10 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"appariement libre (nul N1) : mu = {mu:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs10", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS10")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
