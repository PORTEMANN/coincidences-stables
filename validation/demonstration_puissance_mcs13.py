"""demonstration_puissance_mcs13.py — Regle 1.2 pour la carte MCS-13.

Systemes synthetiques plantes sur les rapports de R a 1 % pres -> CS+
attendu (Sigma >= 3,0), controles resolus a |effet| >= 2 u ; periodes
libres ordonnees -> CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs13.jsonl")
R = np.array([2.0, 1.5, 4/3, 1.25, 1.2, 3.0, 4.0, 2.5, 5/3])  # ensemble fige


def ecarts(ratios):
    d = np.abs(ratios[:, None] - R[None, :]) / R[None, :]
    return d.min(axis=1)


def mesure(ratios):
    return -np.log10(np.sqrt(np.mean(ecarts(ratios) ** 2)))


def systemes_plantes(rng, n_sys=80):
    ratios = []
    for _ in range(n_sys):
        n_p = rng.integers(2, 6)
        p = np.exp(rng.uniform(np.log(0.5), np.log(30.0)))
        for _ in range(n_p - 1):
            rho = R[rng.integers(0, len(R))]
            ratios.append(rho * (1 + 0.01 * rng.normal()))
            p *= rho
    return np.array(ratios)


def systemes_libres(rng, n_sys=80):
    ratios = []
    for _ in range(n_sys):
        n_p = rng.integers(2, 6)
        per = np.sort(np.exp(rng.uniform(np.log(0.5), np.log(3000.0), n_p)))
        ratios += list(per[1:] / per[:-1])
    return np.array(ratios)


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS13")

    ratios = systemes_plantes(rng)
    m_reel = mesure(ratios)
    # N1 approche : rapports issus de systemes libres (ordre libre)
    ms_n1 = [mesure(systemes_libres(rng)) for _ in range(2000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : rapports deplaces au point milieu entre les deux rationnels
    # les plus proches (sabotage maximal declare)
    d = np.abs(ratios[:, None] - R[None, :]) / R[None, :]
    tri = np.argsort(d, axis=1)
    r_milieu = (R[tri[:, 0]] + R[tri[:, 1]]) / 2
    effet_c1 = (m_reel - mesure(r_milieu)) / u
    # c2 : rapports libres declares
    effet_c2 = (m_reel - mesure(systemes_libres(rng))) / u
    v = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    seuil_carte = 3.0
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-13 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"ordre libre : mu = {mu:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs13", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS13")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
