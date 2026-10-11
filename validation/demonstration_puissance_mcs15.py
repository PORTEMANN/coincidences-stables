"""demonstration_puissance_mcs15.py — Regle 1.2 pour la carte MCS-15.

Texte synthetique plante sur la loi figee (alpha = 1 exact, bruit 5 %,
vocabulaire 30 000) -> CS+ attendu (Sigma >= 3,0), controles resolus a
|effet| >= 2 u ; partition uniforme -> CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs15.jsonl")
K = 30000


def loi_rang(k, n_tot, alpha=1.0):
    r = np.arange(1, k + 1)
    return n_tot / (r ** alpha) / np.sum(1.0 / r ** alpha)


def mesure(effectifs, alpha=1.0, renverser=False):
    effectifs = np.asarray(effectifs, dtype=float)
    k = len(effectifs)
    n_tot = effectifs.sum()
    eff = np.sort(effectifs) if renverser else np.sort(effectifs)[::-1]
    eps = np.log10(eff + 1) - np.log10(loi_rang(k, n_tot, alpha) + 1)
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def nul_uniforme(rng, n_tot, k):
    part = rng.uniform(0, 1, k)
    return np.floor(part / part.sum() * n_tot).astype(int)


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS15")

    n_tot = 550000
    eff = loi_rang(K, n_tot) * (1 + 0.05 * rng.normal(0, 1, K))
    eff = np.maximum(np.round(eff), 0).astype(int)
    m_reel = mesure(eff)
    ms_n1 = [mesure(nul_uniforme(rng, n_tot, K)) for _ in range(2000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    effet_c1 = (m_reel - mesure(eff, renverser=True)) / u
    effet_c2 = (m_reel - mesure(nul_uniforme(rng, n_tot, K))) / u
    v = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    seuil_carte = 3.0
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-15 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"partition uniforme : mu = {mu:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs15", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS15")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
