"""demonstration_puissance_mcs23.py — Regle 1.2 pour la carte MCS-23.

Contenu synthetique plante au tarif (N_eff = 5, l'entier le plus proche de
3pi/2 dans la fenetre gelee) -> CS+ attendu (Sigma >= 3,0), controles
resolus a |effet| >= 2 u ; contenu libre -> CS- attendu ; banc aveugle ->
CS0. Nul : enumeration exacte de la fenetre Krajewski gelee (matrices
symetriques k x k, k <= 3, entrees 0..3, Sigma m_ij dans [2,24]) — pas de
tirage, distribution exacte.
Graine : 20261012 (numpy — synthetique, controle c2 seulement).
Journal chaine dedie.
"""
from __future__ import annotations

import itertools
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402

GRAINE = 20261012
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs23.jsonl")
SEUIL_CARTE = 3.0
N_REQ = 3 * np.pi / 2   # N_eff requis par la chaine gelee (declaration)


def enumerer_fenetre(mmax=3):
    """Toutes les matrices symetriques k x k (k <= 3), entrees 0..mmax,
    Sigma m_ij dans [2, 24] — enumeration exacte (fenetre gelee)."""
    sigmas = []
    for k in (1, 2, 3):
        idx = [(i, j) for i in range(k) for j in range(i, k)]
        poids = [1 if i == j else 2 for i, j in idx]
        for vals in itertools.product(range(mmax + 1), repeat=len(idx)):
            s = sum(w * v for w, v in zip(poids, vals))
            if 2 <= s <= 24:
                sigmas.append(s)
    return np.array(sigmas, dtype=float)


def mesure_sigma(s):
    return -abs(np.log10(s / N_REQ))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS23")

    nul = mesure_sigma(enumerer_fenetre())
    mu, u = float(nul.mean()), float(nul.std())
    print(f"fenetre : {len(nul)} contenus ; mu = {mu:.4f}, u = {u:.4f}")

    # contenu plante au tarif : N_eff = 5 (plus proche entier de 3pi/2)
    m_reel = mesure_sigma(5)
    zz = mcs.z_score(m_reel, mu, u)

    # c1 : contenu deplace x10 ; c2 : contenu remplace par le nul
    effet_c1 = (m_reel - mesure_sigma(50)) / u
    m_c2 = float(rng.choice(nul))
    effet_c2 = (m_reel - m_c2) / u

    vv = mcs.evaluer_v2("DEFAULT", {"g0": zz}, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()
    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-23 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"plante : m = {m_reel:.4f} (N=5) ; rang du plante dans le nul : "
          f"p = {float((nul >= m_reel).mean()):.4f}")
    jc.ajouter({"type": "demonstration_puissance_mcs23", "verdict_demo": vd,
                "decision": decision,
                "nul_fenetre": {"n": len(nul), "mu": mu, "u": u}})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS23")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
