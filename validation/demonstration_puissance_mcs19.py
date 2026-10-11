"""demonstration_puissance_mcs19.py — Regle 1.2 pour la carte MCS-19.

Triplet synthetique plante au plancher (1,05 plancher) -> CS+ attendu
(Sigma >= 3,0), controles resolus a |effet| >= 2 u ; triplet libre ->
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs19.jsonl")
PLANCHER = 0.0796   # hbar / (4 pi k_B) — KSS 2005, gele
ETENDUE = (0.05, 5.0)


def mesure(v, plancher=PLANCHER):
    e = min(v) / plancher - 1
    if e <= 0:   # violation du plancher : pire que toute approche (declare)
        return -np.log10(abs(e)) - 2
    return -np.log10(e)


def triplet_libre(rng):
    return np.exp(rng.uniform(np.log(ETENDUE[0]), np.log(ETENDUE[1]), 3))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS19")

    # triplet plante : le meilleur a 1,05 plancher
    v = np.array([0.0796 * 1.05, 0.4, 0.8]) * (1 + 0.01 * rng.normal(0, 1, 3))
    m_reel = mesure(v)
    ms_n1 = [mesure(triplet_libre(rng)) for _ in range(10000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : le meilleur remplace par 10 planchers ; c2 : plancher double
    v_c1 = v.copy(); v_c1[0] = 0.0796 * 10
    effet_c1 = (m_reel - mesure(v_c1)) / u
    effet_c2 = (m_reel - mesure(v, plancher=2 * PLANCHER)) / u
    vv = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()

    decision = ("SCELLABLE" if vd["sigma"] >= 3.0
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-19 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"triplet libre : mu = {mu:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs19", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS19")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
