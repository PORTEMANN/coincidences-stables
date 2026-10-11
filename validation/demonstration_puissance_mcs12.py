"""demonstration_puissance_mcs12.py — Regle 1.2 pour la carte MCS-12.

Observations synthetiques plantees sur les predictions a 0,02 dex pres
-> CS+ attendu (Sigma >= 3,0), controles resolus a |effet| >= 2 u ;
quadruplet d'univers aleatoire -> CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs12.jsonl")
PRED = np.array([2.5e-5, 1.0e-5, 0.247, 4.7e-10])   # D/H, 3He/H, Yp, 7Li/H
ETENDUES = [(1e-6, 1e-3), (1e-6, 1e-3), (0.05, 0.5), (1e-11, 1e-8)]


def mesure(pred, obs):
    eps = np.log10(pred) - np.log10(obs)
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def univers_aleatoire(rng):
    return np.array([np.exp(rng.uniform(np.log(a), np.log(b)))
                     for a, b in ETENDUES])


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS12")

    # observations plantees : predictions + 0,02 dex de bruit
    obs = PRED * 10 ** (0.02 * rng.normal(0, 1, 4))
    m_reel = mesure(PRED, obs)
    ms_n1 = [mesure(PRED, univers_aleatoire(rng)) for _ in range(10000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : predictions permutees ; c2 : univers aleatoire declare
    effet_c1 = (m_reel - mesure(rng.permutation(PRED), obs)) / u
    effet_c2 = (m_reel - mesure(PRED, univers_aleatoire(rng))) / u
    v = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    seuil_carte = 3.0
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-12 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"univers aleatoire : mu = {mu:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs12", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS12")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
