"""demonstration_puissance_mcs11.py — Regle 1.2 pour la carte MCS-11.

Triplet synthetique plante sur K = 2/3 a 1e-6 pres -> CS+ attendu
(Sigma >= 3,1), controles resolus a |effet| >= 2 u ; triplet log-uniforme
-> CS- attendu ; banc aveugle -> CS0.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs11.jsonl")
CIBLE = 2 / 3
ETENDUE = (0.5, 2000.0)   # MeV, declaree a la carte


def koide(masses):
    masses = np.asarray(masses, dtype=float)
    return masses.sum() / np.sqrt(masses).sum() ** 2


def mesure(masses, cible=CIBLE):
    return -np.log10(abs(koide(masses) - cible) / cible)


def triplet_libre(rng):
    return np.sort(np.exp(rng.uniform(np.log(ETENDUE[0]),
                                      np.log(ETENDUE[1]), 3)))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS11")

    # triplet plante exact : (1, 4, (6+sqrt(39))^2) resout K = 2/3
    # (verification : (1+4+y^2) = (2/3)(1+2+y)^2 pour y = 6+sqrt(39)),
    # bruite a 1e-6 relatif ; masses en MeV dans l'etendue declaree
    y = 6 + np.sqrt(39)
    plante = np.array([1.0, 4.0, y ** 2]) * np.exp(rng.normal(0, 1e-6, 3))
    m_reel = mesure(plante)

    ms_n1 = [mesure(triplet_libre(rng)) for _ in range(10000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c1 : triplet libre declare ; c2 : cible 3/4
    effet_c1 = (m_reel - mesure(triplet_libre(rng))) / u
    effet_c2 = (m_reel - mesure(plante, cible=0.75)) / u
    v = mcs.evaluer_v2("DEFAULT", {"g0": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    seuil_carte = 3.1
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-11 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"triplet libre : mu = {mu:.3f} (m_reel = {m_reel:.3f})")
    jc.ajouter({"type": "demonstration_puissance_mcs11", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS11")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
