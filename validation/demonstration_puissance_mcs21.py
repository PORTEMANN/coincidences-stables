"""demonstration_puissance_mcs21.py — Regle 1.2 pour la carte MCS-21.

Jeu synthetique plante avec une tension de 3,5 sigma entre deux familles
(erreurs symetrisees des cinq mesures gelees) -> CS+ attendu
(Sigma >= 3,1), controles resolus a |effet| >= 2 u ; jeu concordant ->
CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs21.jsonl")
SEUIL_CARTE = 3.1
# erreurs symetrisees des cinq mesures gelees (CMB x2, lentilles x3)
SIG = np.array([0.016, 0.028, 0.0225, 0.024, 0.0325])
FAM = np.array([0, 0, 1, 1, 1])   # 0 = CMB, 1 = lentilles


def tension(v, sig=SIG, fam=FAM):
    w = 1.0 / sig ** 2
    mu, s = {}, {}
    for f in (0, 1):
        sel = fam == f
        mu[f] = float((w[sel] * v[sel]).sum() / w[sel].sum())
        s[f] = float(np.sqrt(1.0 / w[sel].sum()))
    return abs(mu[0] - mu[1]) / np.sqrt(s[0] ** 2 + s[1] ** 2)


def tension_vect(tir, sig=SIG, fam=FAM):
    """Tension vectorisee sur des lignes de tirages (nb, 5)."""
    w = 1.0 / sig ** 2
    out = np.empty(len(tir))
    for f in (0, 1):
        sel = fam == f
        mu = (tir[:, sel] * w[sel]).sum(axis=1) / w[sel].sum()
        s = np.sqrt(1.0 / w[sel].sum())
        if f == 0:
            mu0, s0 = mu, s
        else:
            mu1, s1 = mu, s
    out = np.abs(mu0 - mu1) / np.sqrt(s0 ** 2 + s1 ** 2)
    return out


def nul_n1(rng, v, nb=10000):
    w = 1.0 / SIG ** 2
    mup = float((w * v).sum() / w.sum())
    tir = rng.normal(mup, SIG, size=(nb, len(v)))
    return tension_vect(tir)


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS21")

    # jeu plante : deux familles separees de 3,5 sigma combines
    sep = 3.5 * np.sqrt(0.01389 ** 2 + 0.01465 ** 2)
    v = np.array([0.8005 + sep / 2, 0.8005 + sep / 2,
                  0.8005 - sep / 2, 0.8005 - sep / 2, 0.8005 - sep / 2])
    m_reel = tension(v)
    ms = nul_n1(rng, v)
    mu, u = float(ms.mean()), float(ms.std())
    zz = mcs.z_score(m_reel, mu, u)

    # c1 : tension supprimee (lentilles alignees sur la famille CMB)
    v_c1 = v.copy()
    w1 = 1.0 / SIG[FAM == 1] ** 2
    v_c1[FAM == 1] = (w1 * 0 + 1) * v_c1[FAM == 0].mean()
    effet_c1 = (m_reel - tension(v_c1)) / u
    # c2 : ecarts doubles dans le sens observe (tension doublee)
    w_all = 1.0 / SIG ** 2
    mup = float((w_all * v).sum() / w_all.sum())
    v_c2 = mup + 2.0 * (v - mup)
    effet_c2 = (tension(v_c2) - m_reel) / u

    vv = mcs.evaluer_v2("DEFAULT", {"g0": zz}, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()
    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-21 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"nul concordance : mu = {mu:.3f}, u = {u:.3f} (T plantee = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs21", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS21")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
