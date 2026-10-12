"""demonstration_puissance_mcs20.py — Regle 1.2 pour la carte MCS-20.

Univers synthetique plante a w = -1 exact (positions z et bruit de la
configuration reelle Pantheon+ — la puissance depend de l'echantillon,
declare) -> CS+ attendu (Sigma >= 3,1), controles resolus a |effet| >= 2 u ;
univers a w libre -> CS- attendu ; banc aveugle -> CS0.
Graine : 20261012 (numpy — synthetique). Journal chaine dedie.
"""
from __future__ import annotations

import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402

GRAINE = 20261012
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs20.jsonl")
SEUIL_CARTE = 3.1
OM_M = 0.315
H0 = 67.4
M_GEL = -19.253
C_LUM = 299792.458
N_NUL = 10000
W_LIBRE = (-1.4, -0.6)
ZGRID = np.linspace(0.0, 2.4, 262145)


def courbe_pts(zpts, w):
    """mu_th aux points zpts, integrale de Friedmann complete (trapèzes)."""
    f = 1.0 / np.sqrt(OM_M * (1 + ZGRID) ** 3
                      + (1 - OM_M) * (1 + ZGRID) ** (3 * (1 + w)))
    fint = np.concatenate(([0.0], np.cumsum(0.5 * (f[:-1] + f[1:])
                                            * np.diff(ZGRID))))
    dl = (C_LUM / H0) * (1 + zpts) * np.interp(zpts, ZGRID, fint)
    return 5 * np.log10(dl) + 25 + M_GEL


def lire_config():
    """Positions z et sigmas reels (configuration seule — declare)."""
    d = os.path.join(RACINE, "donnees", "mcs17")
    lignes = open(os.path.join(d, "pantheon_ref.dat")).read().splitlines()
    entete = lignes[0].split()
    i_z, i_mb = entete.index("zCMB"), entete.index("m_b_corr")
    z, mb = [], []
    for ln in lignes[1:]:
        p = ln.split()
        if len(p) <= max(i_z, i_mb):
            continue
        z.append(float(p[i_z]))
        mb.append(float(p[i_mb]))
    cov = np.loadtxt(os.path.join(d, "pantheon_STATONLY.cov"))
    n = int(cov[0]) if cov.ndim == 1 else len(z)
    sig = np.sqrt(np.diag(cov[1:].reshape(n, n))) if cov.ndim == 1 else None
    return np.array(z), np.array(mb), sig


def pente_bins(residus, z, n_bins=8):
    idx = np.argsort(z)
    rb, zb = [], []
    for part in np.array_split(idx, n_bins):
        rb.append(float(np.mean(residus[part])))
        zb.append(float(np.mean(z[part])))
    return np.polyfit(zb, rb, 1)[0], np.array(zb), np.array(rb)


def nul_n1(rng, zb, sig_b, nb=N_NUL):
    """Univers a w libre : derive + bruit cale sur la dispersion reelle."""
    ms = []
    for _ in range(nb):
        w = rng.uniform(*W_LIBRE)
        derive = courbe_pts(zb, w) - courbe_pts(zb, -1.0)
        rs = derive + rng.normal(0, sig_b)
        ms.append(-abs(np.polyfit(zb, rs, 1)[0]))
    return np.array(ms)


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS20")

    z, mb, sig = lire_config()
    # univers plante a w = -1 exact : residus = bruit pur
    mu_plante = courbe_pts(z, -1.0) + rng.normal(0, sig)
    residus = mu_plante - courbe_pts(z, -1.0)
    p, zb, rb = pente_bins(residus, z)
    sig_b = np.array([float(np.std(residus[np.array_split(np.argsort(z), 8)[k]],
                              ddof=1) / np.sqrt(len(np.array_split(np.argsort(z), 8)[k])))
                      for k in range(8)])
    m_reel = -abs(p)
    ms = nul_n1(rng, zb, sig_b)
    mu, u = float(ms.mean()), float(ms.std())
    zz = mcs.z_score(m_reel, mu, u)

    # c1 : derive w = -0,85 injectee ; c2 : univers a w libre du nul
    mu_sab = mu_plante + (courbe_pts(z, -0.85) - courbe_pts(z, -1.0))
    m_c1 = -abs(pente_bins(mu_sab - courbe_pts(z, -1.0), z)[0])
    effet_c1 = (m_reel - m_c1) / u
    w2 = float(rng.uniform(*W_LIBRE))
    mu_c2 = courbe_pts(z, w2) + rng.normal(0, sig)
    m_c2 = -abs(pente_bins(mu_c2 - courbe_pts(z, -1.0), z)[0])
    effet_c2 = (m_reel - m_c2) / u

    vv = mcs.evaluer_v2("DEFAULT", {"g0": zz}, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()
    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p2 >= 2.0 for p2 in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-20 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"nul w libre : mu = {mu:.4f}, u = {u:.4f} (m_plante = {m_reel:.4f})")
    jc.ajouter({"type": "demonstration_puissance_mcs20", "verdict_demo": vd,
                "decision": decision,
                "note": "positions z et bruit de la configuration reelle, "
                        "verite synthetique plantee a w = -1"})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS20")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
