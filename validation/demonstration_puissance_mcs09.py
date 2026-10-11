"""demonstration_puissance_mcs09.py — Regle 1.2 pour la carte MCS-09.

Systeme solaire synthetique plante sur la loi figee a 1 % pres -> CS+
attendu (Sigma >= 3,2), controles resolus a |effet| >= 2 u ; sequence
croissante sans loi -> CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs09.jsonl")
A_PRED = np.array([0.4, 0.7, 1.0, 1.6, 2.8, 5.2, 10.0, 19.6, 38.8, 77.2])
ETENDUE = (0.39, 39.8)   # declare a la carte


def mesure(a_obs, a_pred):
    e = (np.asarray(a_obs) - a_pred) / a_pred
    return -np.log10(np.sqrt(np.mean(e ** 2)))


def sequence_libre(rng, n=10):
    return np.sort(np.exp(rng.uniform(np.log(ETENDUE[0]), np.log(ETENDUE[1]), n)))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS09")

    # systeme plante : loi figee + 1 % de bruit
    a_reel = A_PRED * (1 + 0.01 * rng.normal(0, 1, 10))
    m_reel = mesure(a_reel, A_PRED)
    ms_n1 = [mesure(sequence_libre(rng), A_PRED) for _ in range(10000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : indices decales (predictions doublees) ; c2 : sequence libre declaree
    effet_c1 = (m_reel - mesure(a_reel, A_PRED * 2)) / u
    effet_c2 = (m_reel - mesure(sequence_libre(rng), A_PRED)) / u
    v = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    # fausse loi : sequence croissante sans structure -> CS- attendu
    m_libre = mesure(sequence_libre(rng), A_PRED)
    z_libre = mcs.z_score(m_libre, mu, u)

    seuil_carte = 3.2
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-09 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"sequence libre : z = {z_libre:.2f} (CS- attendu)")
    jc.ajouter({"type": "demonstration_puissance_mcs09", "verdict_demo": vd,
                "z_sequence_libre": z_libre, "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS09")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
