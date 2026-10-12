"""demonstration_puissance_mcs22.py — Regle 1.2 pour la carte MCS-22.

Triplet synthetique plante exactement unifie (alpha_s ajustee pour fermer
le gap, declare) -> CS+ attendu (Sigma >= 3,0), controles resolus a
|effet| >= 2 u ; triplet libre -> CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs22.jsonl")
SEUIL_CARTE = 3.0
MZ = 91.1880
B = np.array([41.0 / 10.0, -19.0 / 6.0, -7.0])
ETENDUES = {"A": (120.0, 140.0), "s2": (0.20, 0.27), "al": (0.09, 0.15)}


def couplages(A, s2, al):
    """y = (1/alpha1, 1/alpha2, 1/alpha3), normalisation SU(5) gelee."""
    return np.array([0.6 * (1.0 - s2) * A, s2 * A, 1.0 / al])


def gap(A, s2, al, ref=0):
    """gap au croisement t12 (ref=0) ou t13 (ref=1) — running 1-loop gele."""
    y = couplages(A, s2, al)
    i, j = (0, 1) if ref == 0 else (0, 2)
    tij = (y[i] - y[j]) / ((B[i] - B[j]) / (2 * np.pi))
    k = 2 if ref == 0 else 1
    yij = y[i] - (B[i] / (2 * np.pi)) * tij
    yk = y[k] - (B[k] / (2 * np.pi)) * tij
    return abs(yk - yij), tij, yij


def mesure(A, s2, al):
    return -gap(A, s2, al)[0]


def triplet_libre(rng):
    return (rng.uniform(*ETENDUES["A"]), rng.uniform(*ETENDUES["s2"]),
            rng.uniform(*ETENDUES["al"]))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS22")

    # triplet plante : alpha_s ajustee pour fermer le gap (declare)
    A, s2 = 127.930, 0.23129
    y = couplages(A, s2, 0.1180)
    t12 = (y[0] - y[1]) / ((B[0] - B[1]) / (2 * np.pi))
    y12 = y[0] - (B[0] / (2 * np.pi)) * t12
    y30_plante = y12 + (B[2] / (2 * np.pi)) * t12
    al_plante = 1.0 / y30_plante
    m_reel = mesure(A, s2, al_plante)

    ms = np.array([mesure(*triplet_libre(rng)) for _ in range(10000)])
    mu, u = float(ms.mean()), float(ms.std())
    zz = mcs.z_score(m_reel, mu, u)

    # c1 : alpha_s +15 % ; c2 : triplet libre du nul
    effet_c1 = (m_reel - mesure(A, s2, al_plante * 1.15)) / u
    effet_c2 = (m_reel - mesure(*triplet_libre(rng))) / u

    vv = mcs.evaluer_v2("DEFAULT", {"g0": zz}, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()
    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-22 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"plante : alpha_s = {al_plante:.4f} ; nul : mu_gap = {-mu:.3f}, "
          f"u = {u:.3f}")
    jc.ajouter({"type": "demonstration_puissance_mcs22", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS22")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
