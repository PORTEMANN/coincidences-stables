"""demonstration_puissance_mcs20.py — Regle 1.2 pour la carte MCS-20 (v2).

Mesure corrigee (une fois, avant gel, declaree dans la carte) : m = -Delta,
Delta = chi2(w=-1) - chi2(w_best) sur la grille gelee ; bruit diagonal cale
sur la covariance reelle. La demo v1 (pente OLS, impuissante) est conservee
a cote (demonstration_puissance_mcs20_v1.py).
Implementation : les 81 courbes theoriques de la grille sont pre-calculees
une fois par configuration (elles ne dependent pas du tirage — meme
convention numerique que la carte).

Univers synthetique plante a w = -1 exact (positions z et sigmas de la
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
W_GRID = np.linspace(W_LIBRE[0], W_LIBRE[1], 81)
ZGRID = np.linspace(0.0, 2.4, 262145)


def courbe_pts(zpts, w, om=OM_M):
    """mu_th aux points zpts, integrale de Friedmann complete (trapezes)."""
    f = 1.0 / np.sqrt(om * (1 + ZGRID) ** 3
                      + (1 - om) * (1 + ZGRID) ** (3 * (1 + w)))
    fint = np.concatenate(([0.0], np.cumsum(0.5 * (f[:-1] + f[1:])
                                            * np.diff(ZGRID))))
    dl = (C_LUM / H0) * (1 + zpts) * np.interp(zpts, ZGRID, fint)
    return 5 * np.log10(dl) + 25 + M_GEL


def grille_theorie(z, om=OM_M, grid=W_GRID):
    """TH[k] = mu_th(z ; grid[k]) — pre-calcule une fois par configuration."""
    return np.array([courbe_pts(z, float(w), om) for w in grid])


def mesure(mu, TH, sig, i_m1):
    """m = -(chi2(-1) - chi2(w_best)) ; i_m1 = indice de w = -1."""
    c_all = np.sum(((mu - TH) / sig) ** 2, axis=1)
    return -(c_all[i_m1] - float(c_all.min()))


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
    n = int(cov[0])
    sig = np.sqrt(np.diag(cov[1:].reshape(n, n)))
    return np.array(z), np.array(mb), sig


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS20")

    z, mb, sig = lire_config()
    TH = grille_theorie(z)
    i_m1 = int(np.argmin(np.abs(W_GRID + 1.0)))

    # univers plante a w = -1 exact
    mu_plante = TH[i_m1] + rng.normal(0, sig)
    m_reel = mesure(mu_plante, TH, sig, i_m1)

    # nul : univers a w libre (cout de w = -1 quand le monde a w != -1)
    ms = np.empty(N_NUL)
    for k in range(N_NUL):
        w = rng.uniform(*W_LIBRE)
        mu_s = courbe_pts(z, w) + rng.normal(0, sig)
        ms[k] = mesure(mu_s, TH, sig, i_m1)
    mu, u = float(ms.mean()), float(ms.std())
    zz = mcs.z_score(m_reel, mu, u)

    # c1 : derive w = -0,85 injectee ; c2 : univers a w libre du nul
    mu_sab = mu_plante + (courbe_pts(z, -0.85) - TH[i_m1])
    effet_c1 = (m_reel - mesure(mu_sab, TH, sig, i_m1)) / u
    w2 = float(rng.uniform(*W_LIBRE))
    mu_c2 = courbe_pts(z, w2) + rng.normal(0, sig)
    effet_c2 = (m_reel - mesure(mu_c2, TH, sig, i_m1)) / u

    vv = mcs.evaluer_v2("DEFAULT", {"g0": zz}, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()
    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-20 v2 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"nul w libre : mu_Delta = {-mu:.3f}, u = {u:.3f} "
          f"(Delta_plante = {-m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs20", "version": 2,
                "verdict_demo": vd, "decision": decision,
                "note": "mesure corrigee Delta-chi2 (v1 pente OLS impuissante, "
                        "conservee) ; verite synthetique plantee a w = -1"})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS20")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
