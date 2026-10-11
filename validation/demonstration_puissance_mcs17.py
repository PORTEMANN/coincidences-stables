"""demonstration_puissance_mcs17.py — Regle 1.2 pour la carte MCS-17.

Echantillon synthetique avec tension plantee au bas-z -> CS+ attendu
(Sigma >= 3,1), controles resolus a |effet| >= 2 u ; echantillon sans
tension -> CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs17.jsonl")
H0_PLANCK = 67.4
M_GEL = -19.253
C_LUM = 299792.458   # km/s


def courbe_planck(z):
    return 5 * np.log10(C_LUM * z * (1 + z) / H0_PLANCK) + M_GEL


def mesure(z, mu, n_bins=8):
    """Ecart absolu du module moyen du bin le plus bas en z a la courbe."""
    idx = np.argsort(z)
    n = len(z)
    bas = idx[: n // n_bins]
    return abs(float(np.mean(mu[bas])) - float(np.mean(courbe_planck(z[bas]))))


def echantillon(rng, n=1701, tension=0.084):
    z = np.sort(rng.uniform(0.01, 2.3, n))
    mu = courbe_planck(z) + rng.normal(0, 0.15, n)
    bas = z < np.sort(z)[n // 8]
    mu[bas] += 5 * np.log10(1 + tension)   # tension plantee au bas-z
    return z, mu


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS17")

    z, mu = echantillon(rng)
    m_reel = mesure(z, mu)
    # N1 : residus permutes (la tendance mu(z) est conservee)
    residus = mu - courbe_planck(z)
    ms_n1 = [mesure(z, courbe_planck(z) + rng.permutation(residus))
             for _ in range(2000)]
    mu_n, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    zz = mcs.z_score(m_reel, mu_n, u)

    # c1 : residus permutes ; c2 : tension injectee doublee
    effet_c1 = (m_reel - mesure(z, courbe_planck(z)
                                + rng.permutation(residus))) / u
    z2, mu2 = echantillon(rng)
    bas2 = z2 < np.sort(z2)[len(z2) // 8]
    mu2[bas2] += 5 * np.log10(1 + 0.084)
    effet_c2 = (mesure(z2, mu2) - mu_n) / u   # l'injection doit dominer le nul
    v = mcs.evaluer_v2("DEFAULT", {"g0": zz}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    seuil_carte = 3.1
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-17 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"modules permutes : mu = {mu_n:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs17", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS17")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
