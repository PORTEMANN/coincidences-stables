"""demonstrations_puissance_v2.py — Règle 1.2 du manifeste v2.0.

Avant le gel de chaque carte v2, sa statistique doit demontrer sa puissance
sur donnees SYNTHETIQUES a verite connue : resoudre chacun de ses controles
a |effet| >= 2 u, et donner le verdict attendu sur le scenario plante.

Une carte dont la demonstration echoue N'EST PAS scellee (la regle 1.2 fait
son office : la carte dort jusqu'a une statistique plus puissante).

Graine : 20261010 (numpy — synthetique). ChaCha20 reserve aux campagnes
scellees. Journal chaine dedie (GENESIS-MCS-VALID-PUISSANCE-V2).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.stats import spearmanr

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
sys.path.insert(0, os.path.join(RACINE, "nulls"))

import mcs_score_v2 as mcs  # noqa: E402
import surrogates as nul  # noqa: E402
import positive_controls as pc  # noqa: E402
import ash_invariants as ash  # noqa: E402

GRAINE = 20261010
FS = 1000.0
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_v2.jsonl")


# ---------------------------------------------------------------- MCS-04 ----
def demo_mcs04(rng):
    """Loi harmonique : zoo synthetique plante sur le reseau vs hors reseau."""
    noms = [f"p{i}" for i in range(14)]
    m_p = 938.272

    def mesure(masses, delta=2 ** (1 / 12), m_ref=m_p):
        # residu au reseau de pas delta : n(m ; delta) = log2(m/m_ref)/log2(delta)
        ld = np.log2(delta)
        r = [np.log2(m / m_ref) / ld for m in masses]
        r = [x - round(x) for x in r]
        return -np.log10(np.sqrt(np.mean(np.array(r) ** 2)))

    # zoo plante : masses = m_p * delta^n * (1 + 0,1 % bruit)
    n_p = rng.integers(-60, 60, size=14)
    masses_p = m_p * (2 ** (1 / 12)) ** n_p * (1 + 0.001 * rng.normal(0, 1, 14))
    m_reel = mesure(masses_p)
    # nul N1 : reseaux aleatoires
    ms_n1 = [mesure(masses_p, delta=rng.uniform(2 ** (1 / 13), 2 ** (1 / 11)))
             for _ in range(2000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)
    # controles
    masses_dec = masses_p * (2 ** (1 / 24))       # c1 : reseau decale
    effet_c1 = (m_reel - mesure(masses_dec)) / u
    masses_bruit = m_p * np.exp(rng.uniform(np.log(0.5), np.log(95000), 14))  # c2
    effet_c2 = (m_reel - mesure(masses_bruit)) / u
    v = mcs.evaluer_v2("DEFAULT", {"g1": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    # zoo hors reseau (verite connue : pas de loi) — evalue sous N2 (zoos
    # aleatoires, meme reseau delta) : le nul pertinent pour une fausse loi
    masses_hors = m_p * np.exp(rng.uniform(np.log(0.5), np.log(95000), 14))
    m_hors = mesure(masses_hors)
    ms_n2 = [mesure(m_p * np.exp(rng.uniform(np.log(0.5), np.log(95000), 14)))
             for _ in range(2000)]
    u_n2 = float(np.std(ms_n2))
    z_hors = (m_hors - float(np.mean(ms_n2))) / max(u_n2, 1e-9)
    return v.to_dict(), z_hors, {"z_plante": z, "effet_c1": effet_c1,
                                 "effet_c2": effet_c2, "m_reel": m_reel}


# ---------------------------------------------------------------- MCS-05 ----
def demo_mcs05(rng):
    """Agregation EEG : essais synthetiques avec ERD plante par classe."""
    n = 2000  # 8 s a 250 Hz
    n_essais, n_surr = 96, 40

    def signal(classe, rng):
        t = np.arange(n) / 250.0
        mu_amp = 1.0 if classe == 0 else 0.05   # ERD plante fort
        x = 0.5 * np.sin(2 * np.pi * 10 * t) * mu_amp + rng.normal(0, 1, n)
        return x

    def signal_fact(classe, rng):
        # bruit pur + ERD injecte selon l'etiquette factice (verite connue)
        t = np.arange(n) / 250.0
        mu_amp = 1.0 if classe == 0 else 0.05
        return 0.5 * np.sin(2 * np.pi * 10 * t) * mu_amp + rng.normal(0, 1, n)

    def accuracy_centroide(X, y, rng):
        idx = rng.permutation(len(y))
        tr, te = idx[: int(0.7 * len(y))], idx[int(0.7 * len(y)):]
        c = {k: X[tr][y[tr] == k].mean(axis=0) for k in (0, 1)}
        pred = [np.argmin([np.linalg.norm(x - c[k]) for k in (0, 1)]) for x in X[te]]
        return float(np.mean(np.array(pred) == y[te]))

    X = np.array([signal(i % 2, rng) for i in range(n_essais)])
    y = np.arange(n_essais) % 2
    m_reel = accuracy_centroide(X, y, rng)
    ms_n1 = []
    for _ in range(n_surr):
        Xs = np.array([nul.iaaft(x, rng, n_iter=5) for x in X])
        ms_n1.append(accuracy_centroide(Xs, y, rng))
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)
    # c1 : etiquettes permutees
    ms_c1 = [accuracy_centroide(X, rng.permutation(y), rng) for _ in range(20)]
    effet_c1 = (m_reel - float(np.mean(ms_c1))) / u
    # c2 : verite connue injectee dans du BRUIT PUR (aucun signal plante) :
    # un ERD module par des etiquettes factices declarees ; le pipeline doit
    # retrouver ces etiquettes-la (recuperation >> hasard 0,5)
    y_fact = rng.permutation(y)
    Xn = np.array([signal_fact(y_fact[i], rng) for i in range(n_essais)])
    rec = accuracy_centroide(Xn, y_fact, rng)
    effet_c2 = abs(rec - 0.5) / u  # 0,5 = hasard ; la recuperation doit dominer
    z_eff = (mu - m_reel) / u
    v = mcs.evaluer_double_v2("MCS-02", {"g1_iaaft": z, "g2": z}, z_eff,
                              {"c1": effet_c1, "c2": effet_c2},
                              attentes={"c1": 1, "c2": 1})
    return v.to_dict(), {"z": z, "effet_c1": effet_c1, "effet_c2": effet_c2,
                         "m_reel": m_reel, "mu": mu}


# ---------------------------------------------------------------- MCS-06 ----
def demo_mcs06(rng):
    """Bifurcations : 20 questions synthetiques (14 physiques plantees
    decroissantes, 6 conventionnelles libres) ; mesure sur l'axe physique."""
    n_ph, n_co = 14, 6
    types = np.array([1] * n_ph + [0] * n_co)
    Z = np.array([2, 4, 6, 10, 14, 18, 24, 30, 36, 42, 50, 56, 68, 79,
                  5, 12, 33, 47, 60, 75], dtype=float)
    D = np.array([np.clip(5.0 - 0.055 * z + 0.15 * rng.normal(), 0, 5) if t == 1
                  else float(rng.integers(1, 5)) for z, t in zip(Z, types)])

    def mesure(D, types):
        ph = D[types == 1]
        return -spearmanr(ph, Z[types == 1]).statistic   # m = -rho_phys

    m_reel = mesure(D, types)
    # N1 : D permutees au sein des physiques (la mesure ne porte que sur elles)
    ms_n1 = [-spearmanr(rng.permutation(D[types == 1]), Z[types == 1]).statistic
             for _ in range(10000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)
    effet_c1 = (m_reel - float(np.mean(ms_n1))) / u        # c1 : D permutees
    D_rev = D.copy(); D_rev[types == 1] = D[types == 1][::-1]
    effet_c2 = (m_reel - mesure(D_rev, types)) / u         # c2 : rangs retournes
    rho_conv = abs(spearmanr(D[types == 0], Z[types == 0]).statistic)  # c3 : rapporte
    v = mcs.evaluer_v2("DEFAULT", {"g1": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    return v.to_dict(), {"z": z, "effet_c1": effet_c1, "effet_c2": effet_c2,
                         "m_reel": m_reel, "n": n_ph + n_co,
                         "c3_rho_conv": rho_conv}


# ---------------------------------------------------------------- MCS-07 ----
def demo_mcs07(rng):
    """Economie de l'information : chantiers synthetiques avec relation plantee."""
    n = 23
    delta = np.array([0] * 8 + [1] * 15, dtype=float)  # 0 = loin, 1 = proche
    tau = np.array([1.0 - 0.4 * d + 0.05 * rng.normal() for d in delta])

    def mesure(tau, delta):
        return -spearmanr(delta, tau).statistic

    m_reel = mesure(tau, delta)
    ms_n1 = [mesure(tau, rng.permutation(delta)) for _ in range(2000)]
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)
    effet_c1 = (m_reel - float(np.mean([mesure(tau, rng.permutation(delta))
                                        for _ in range(50)]))) / u
    # c2 (carte MCS-07) : etiquettes delta inversees (proche <-> lointain)
    effet_c2 = (m_reel - mesure(tau, 1.0 - delta)) / u
    v = mcs.evaluer_v2("DEFAULT", {"g1": z}, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": -1})
    return v.to_dict(), {"z": z, "effet_c1": effet_c1, "effet_c2": effet_c2,
                         "m_reel": m_reel}


def main():
    rng = np.random.default_rng(GRAINE)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-V2")
    out = {}

    demos = {
        "MCS-04": demo_mcs04,
        "MCS-05": demo_mcs05,
        "MCS-06": demo_mcs06,
        "MCS-07": demo_mcs07,
    }
    seuils = {"MCS-04": 3.1, "MCS-05": 3.3, "MCS-06": 3.1, "MCS-07": 3.1}
    for carte, fn in demos.items():
        res = fn(rng)
        verdict = res[0]
        detail = res[1] if carte == "MCS-04" else res[1]
        puissances = verdict.get("puissances_controles", {})
        passe_puissance = all(p >= 2.0 for p in puissances.values())
        passe_sigma = verdict["sigma"] >= seuils[carte] or verdict["verdict"] == "CS+"
        decision = "SCELLABLE" if (passe_puissance and passe_sigma) else "NON SCELLABLE"
        out[carte] = {"verdict_demo": verdict, "passe_puissance": passe_puissance,
                      "passe_sigma": passe_sigma, "decision": decision,
                      "detail": detail}
        jc.ajouter({"type": "demonstration_puissance_v2", "carte": carte,
                    "decision": decision, "verdict_demo": verdict})
        print(f"{carte}: verdict demo = {verdict['verdict']}, "
              f"puissances = {puissances}, sigma = {verdict['sigma']:.2f} -> {decision}")

    ok, n = mcs.JournalChaine.verifier(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-V2")
    print(f"\nchaine : {ok} ({n} records)")
    return out


if __name__ == "__main__":
    main()
