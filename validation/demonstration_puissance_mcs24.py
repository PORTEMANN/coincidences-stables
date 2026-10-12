"""demonstration_puissance_mcs24.py — Regle 1.2 pour la carte MCS-24.

Contenu synthetique plante au plus proche entier du tarif (N_F = 5) ->
CS+ attendu (Sigma >= 3,0), controles resolus a |effet| >= 2 u ; taille
tiree du nul -> CS- attendu ; banc aveugle -> CS0.
Nul REEL : comptes de triplets nus verifies par taille, calcules par la
machine des orbites de T5/T1 (filiation declaree — reimplementation
compacte des fonctions publiees du corpus), fenetre n in [2,7] (gelee).
Graine : 20261012 (numpy — controle c2). Journal chaine dedie.
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs24.jsonl")
SEUIL_CARTE = 3.0
N_REQ = 3 * np.pi / 2     # tarif requis par la chaine gelee (declaration)
FENETRE = range(2, 8)     # n in [2,7] — gelee


# --- machine des orbites (filiation T1/T5 — reimplementation declaree)
def involutions_signees(a, b):
    n = a + b
    res = []
    for perm_a in itertools.permutations(range(a)):
        for perm_b in itertools.permutations(range(a, n)):
            sigma = perm_a + perm_b
            if any(sigma[sigma[i]] != i for i in range(n)):
                continue
            libres = [i for i in range(n) if i <= sigma[i]]
            for bits in itertools.product([1, -1], repeat=len(libres)):
                s = [0] * n
                for i, bt in zip(libres, bits):
                    s[i] = bt
                    s[sigma[i]] = bt
                res.append((sigma, s))
    return res


def compte_D_orbites(sigma, s, p, q):
    """Compte des D reels sym. hors-chiraux {0,±1}, D≠0, J0 D J0 = -D —
    orbite par orbite (T1, filiation declaree)."""
    n = p + q
    vu = set()
    k_libres = 0
    for i in range(p):
        for j in range(p, n):
            if (i, j) in vu:
                continue
            i2, j2 = sigma[i], sigma[j]
            if (i2, j2) == (i, j):
                vu.add((i, j))
                if s[i] * s[j] == -1:
                    k_libres += 1
            else:
                vu.add((i, j))
                vu.add((i2, j2))
                if s[i] * s[j] * s[i2] * s[j2] == +1:
                    k_libres += 1
    return (3 ** k_libres - 1) if k_libres else 0


def comptes_par_taille():
    """Compte des triplets nus verifies par taille n (fenetre gelee)."""
    comptes = {}
    for n in FENETRE:
        tot = 0
        for p in range(1, n):
            q = n - p
            for sigma, s in involutions_signees(p, q):
                tot += compte_D_orbites(sigma, s, p, q)
        comptes[n] = tot
        print(f"  n={n} : {tot} triplets nus verifies")
    return comptes


def mesure(n):
    return -abs(np.log10(n / N_REQ))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS24")

    print("Nul reel : comptes par taille (machine des orbites) :")
    comptes = comptes_par_taille()
    tailles = np.array(sorted(comptes))
    poids = np.array([comptes[int(n)] for n in tailles], dtype=float)
    poids /= poids.sum()
    gaps = np.array([mesure(int(n)) for n in tailles])   # m = -|delta|
    mu = float(np.sum(gaps * poids))
    u = float(np.sqrt(np.sum((gaps - mu) ** 2 * poids)))
    print(f"  nul pondere reel : mu = {mu:.4f}, u = {u:.4f}")

    # contenu plante : le plus proche entier du tarif (N_F = 5)
    m_reel = mesure(5)
    zz = mcs.z_score(m_reel, mu, u)
    # rang du plante dans le nul : fraction ponderee au moins aussi proche
    p_rang = float(np.sum(poids[gaps >= m_reel]))

    # c1 : contenu deplace x8 ; c2 : taille tiree du nul pondere
    effet_c1 = (m_reel - mesure(40)) / u
    m_c2 = float(rng.choice(gaps, p=poids))
    effet_c2 = (m_reel - m_c2) / u

    vv = mcs.evaluer_v2("DEFAULT", {"g0": zz}, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()
    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-24 : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"plante : m = {m_reel:.4f} (N=5) ; rang dans le nul reel : "
          f"p = {p_rang:.4f}")
    jc.ajouter({"type": "demonstration_puissance_mcs24", "verdict_demo": vd,
                "decision": decision,
                "nul_reel": {"fenetre": [2, 7],
                             "comptes_par_taille": {str(int(k)): int(v) for
                                                    k, v in comptes.items()},
                             "mu": mu, "u": u},
                "rang_plante": p_rang})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS24")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
