"""demonstration_puissance_mcs18.py — Regle 1.2 pour la carte MCS-18.

Triplet synthetique plante unitaire a 0,1 % pres -> CS+ attendu
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs18.jsonl")
ETENDUES = [(0.95, 0.99), (0.20, 0.25), (0.003, 0.005)]


def mesure(v):
    return -np.log10(abs(v[0] ** 2 + v[1] ** 2 + v[2] ** 2 - 1))


def triplet_libre(rng):
    return np.array([rng.uniform(a, b) for a, b in ETENDUES])


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS18")

    # triplet plante : unitaire a 0,1 % pres
    v = np.array([0.9737, 0.2245, 0.00382])
    v = v * np.sqrt((1 + 0.001) / (v ** 2).sum())
    m_reel = mesure(v)
    ms_n1 = [mesure(triplet_libre(rng)) for _ in range(10000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : V_us deplace de 5 % dans le sens qui l'eloigne de 1
    v_c1 = v.copy(); v_c1[1] *= 0.95
    effet_c1 = (m_reel - mesure(v_c1)) / u
    effet_c2 = (m_reel - mesure(triplet_libre(rng))) / u
    vv = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()

    decision = ("SCELLABLE" if vd["sigma"] >= 3.0
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-18 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"triplet libre : mu = {mu:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs18", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS18")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
