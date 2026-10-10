"""demonstration_puissance_mcs08.py — Regle 1.2 pour la carte MCS-08.

Table synthetique de 300 grandeurs : mantisses tirees selon Benford exact
(verite connue plantee) -> CS+ attendu, controles resolus a |effet| >= 2 u.
Table a chiffres plats -> CS- attendu. Banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs08.jsonl")
P_BEN = np.array([np.log10(1 + 1 / d) for d in range(1, 10)])


def premier_chiffre(v):
    d = np.floor(np.abs(v) / 10 ** np.floor(np.log10(np.abs(v))))
    return d.astype(int)


def mesure(chiffres):
    p_obs = np.array([np.mean(chiffres == d) for d in range(1, 10)])
    return -float(np.sum(np.abs(p_obs - P_BEN)))   # m = -L1


def nul_n1(rng, n, nb=10000):
    return np.array([mesure(rng.integers(1, 10, size=n)) for _ in range(nb)])


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS08")

    # table plantee Benford : mantisse m = 10^u, u uniforme -> Benford exact
    n = 300
    mantisses = 10 ** rng.uniform(0, 1, size=n)
    chiffres = premier_chiffre(mantisses)
    m_reel = mesure(chiffres)
    ms_n1 = nul_n1(rng, n)
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : decalage cyclique ; c2 : mantisses uniformes (chiffres plats)
    effet_c1 = (m_reel - mesure(chiffres % 9 + 1)) / u
    effet_c2 = (m_reel - mesure(rng.integers(1, 10, size=n))) / u
    v = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    # fausse table (chiffres plats) : CS- attendu
    m_plat = mesure(rng.integers(1, 10, size=n))
    z_plat = mcs.z_score(m_plat, mu, u)

    print(f"demo MCS-08 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']}")
    print(f"table plate : z = {z_plat:.2f} (CS- attendu)")
    jc.ajouter({"type": "demonstration_puissance_mcs08", "verdict_demo": vd,
                "z_table_plate": z_plat,
                "decision": "SCELLABLE" if vd["verdict"] == "CS+" else "NON SCELLABLE"})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS08")
    print(f"chaine : {ok} ({nb} records)")
    return vd


if __name__ == "__main__":
    main()
