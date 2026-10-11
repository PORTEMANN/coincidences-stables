"""demonstration_puissance_mcs14.py — Regle 1.2 pour la carte MCS-14.

Base synthetique plantee sur la loi de rang figee (alpha = 1 exact, bruit
10 %) -> CS+ attendu (Sigma >= 3,0), controles resolus a |effet| >= 2 u ;
partition uniforme -> CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs14.jsonl")
N_GROUPES = 230
H230 = float(np.sum(1.0 / np.arange(1, N_GROUPES + 1)))


def loi_rang(n_tot, alpha=1.0):
    return n_tot / (np.arange(1, N_GROUPES + 1) ** alpha) / (
        H230 if alpha == 1.0 else np.sum(1.0 / np.arange(1, N_GROUPES + 1) ** alpha))


def mesure(effectifs, n_tot=None, alpha=1.0, renverser=False):
    n_tot = effectifs.sum() if n_tot is None else n_tot
    nz = loi_rang(n_tot, alpha)
    eff = np.sort(effectifs) if renverser else np.sort(effectifs)[::-1]
    eps = np.log10(eff + 1) - np.log10(nz + 1)
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def partition_uniforme(rng, n_tot):
    return rng.multinomial(n_tot, [1 / N_GROUPES] * N_GROUPES)


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS14")

    n_tot = 100000
    # base plantee : loi de rang exacte + 10 % de bruit relatif
    eff = loi_rang(n_tot) * (1 + 0.10 * rng.normal(0, 1, N_GROUPES))
    eff = np.maximum(np.round(eff), 0).astype(int)
    m_reel = mesure(eff)
    ms_n1 = [mesure(partition_uniforme(rng, n_tot)) for _ in range(2000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : rangs inverses ; c2 : exposant double
    effet_c1 = (m_reel - mesure(eff, renverser=True)) / u
    effet_c2 = (m_reel - mesure(eff, alpha=2.0)) / u
    v = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    seuil_carte = 3.0
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-14 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"partition uniforme : mu = {mu:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs14", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS14")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
