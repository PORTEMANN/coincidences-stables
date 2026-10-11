"""demonstration_puissance_mcs16.py — Regle 1.2 pour la carte MCS-16.

Masses synthetiques plantees sur les six regles figees a 0,5 % pres ->
CS+ attendu (Sigma >= 3,2), controles resolus a |effet| >= 2 u ;
masses libres -> CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs16.jsonl")
ALPHA = 1 / 137.035999084
M_P, M_E = 938.27208816, 0.51099895   # MeV (references declarees)
M_C_CORPS = 1251.029                  # valeur gelee du corpus (regle 4)


def regles(m_p, m_e, alpha):
    """Les six regles figees du corpus (bilan LOI-HARMONIQUE de mvcg)."""
    return np.array([
        m_e * (3 / 2) / alpha,          # 1 muon quinte
        m_p / (alpha * np.sqrt(2)),     # 2 Z diagonale
        m_p / 9,                        # 3 strange quarte
        4 * M_C_CORPS / 2 ** (1 / 12),  # 4 bottom G6 (chaine interne gelee)
        (m_p / 18) * np.sqrt(alpha) / 2,  # 5 up G3
        24 * m_p / 18,                  # 6 charm G5
    ])


def mesure(pred, obs):
    eps = np.log10(pred) - np.log10(obs)
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS16")

    pred = regles(M_P, M_E, ALPHA)
    obs = pred * (1 + 0.005 * rng.normal(0, 1, 6))   # masses plantees a 0,5 %
    m_reel = mesure(pred, obs)
    ms_n1 = [mesure(pred, rng.permutation(obs)) for _ in range(10000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : masses permutees ; c2 : constantes alterees x1,05
    effet_c1 = (m_reel - mesure(pred, rng.permutation(obs))) / u
    effet_c2 = (m_reel - mesure(pred * 1.05, obs)) / u
    v = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    seuil_carte = 3.2
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-16 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"assignation permutee : mu = {mu:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs16", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS16")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
