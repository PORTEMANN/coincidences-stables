"""demonstration_puissance_mcs05b.py — Regle 1.2 pour la carte MCS-05b.

EEG synthetique avec ERD plante (attenuation mu contralaterale) -> CS+
attendu (Sigma >= 3,3), c2 resolu a |effet| >= 2 u ; bruit sans structure
-> CS- attendu ; pipeline aveugle simule -> CS0.
Mesure de PUISSANCE : E = (P_ipsi - P_contra)/(P_ipsi + P_contra) ;
le nul honnete est la permutation des hemispheres (IAAFT conserve le
spectre — il ne peut pas tuer une mesure de puissance ; declare a la carte).
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
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs05b.jsonl")
FS = 250.0


def puissance_mu(x, fs=FS, bande=(8.0, 12.0)):
    f = np.fft.rfftfreq(len(x), 1 / fs)
    P = np.abs(np.fft.rfft(x)) ** 2
    sel = (f >= bande[0]) & (f <= bande[1])
    return float(P[sel].mean())


def E_essai(c3, c4, classe):
    """E = (P_ipsi - P_contra)/(P_ipsi + P_contra) ; gauche -> ipsi C3."""
    p3, p4 = puissance_mu(c3), puissance_mu(c4)
    ipsi, contra = (p3, p4) if classe == 0 else (p4, p3)
    return (ipsi - contra) / (ipsi + contra)


def mesure(E):
    return float(np.mean(E))


def essai(rng, classe, n=500, erd=0.35):
    """Bruit + mu ; l'ERD plante attenue le mu contralateral."""
    t = np.arange(n) / FS
    mu = np.sin(2 * np.pi * 10 * t)
    amp3 = 1.0 - (0.0 if classe == 1 else 0.0)   # C3 = ipsi pour gauche
    amp3 = 1.0 if classe == 0 else 1.0 - erd     # classe droite : C3 contra
    amp4 = 1.0 - erd if classe == 0 else 1.0     # classe gauche : C4 contra
    c3 = amp3 * mu + rng.normal(0, 1, n)
    c4 = amp4 * mu + rng.normal(0, 1, n)
    return c3, c4


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS05B")

    n_essais = 144
    E = np.array([E_essai(*essai(rng, i % 2), i % 2) for i in range(n_essais)])
    m_reel = mesure(E)
    # N1 : permutation des hemispheres par essai (la contralateralite meurt)
    ms_n1 = []
    essais = [essai(rng, i % 2) for i in range(n_essais)]
    for _ in range(2000):
        Ef = []
        for i in range(n_essais):
            c3, c4 = essais[i]
            if rng.uniform() < 0.5:
                c3, c4 = c4, c3
            Ef.append(E_essai(c3, c4, i % 2))
        ms_n1.append(mesure(np.array(Ef)))
    mu, u = float(np.mean(ms_n1)), float(np.std(ms_n1))
    z = mcs.z_score(m_reel, mu, u)

    # c2 : injection dans du bruit pur, etiquettes factices declarees
    Ef = []
    for i in range(n_essais):
        classe = i % 2
        t = np.arange(500) / FS
        mu_ = np.sin(2 * np.pi * 10 * t)
        c3 = (1.0 if classe == 0 else 0.5) * mu_ + rng.normal(0, 1, 500)
        c4 = (0.5 if classe == 0 else 1.0) * mu_ + rng.normal(0, 1, 500)
        Ef.append(E_essai(c3, c4, classe))
    m_c2 = mesure(np.array(Ef))
    effet_c2 = abs(m_c2 - mu) / u
    v = mcs.evaluer_double_v2("MCS-02", {"g2": z}, (mu - m_reel) / u,
                              {"c2": effet_c2}, attentes={"c2": 1})
    vd = v.to_dict()

    seuil_carte = 3.3
    decision = ("SCELLABLE" if vd["sigma"] >= seuil_carte
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                else "NON SCELLABLE")
    print(f"demo MCS-05b : verdict = {vd['verdict']}, sigma = {vd['sigma']:.2f}, "
          f"puissances = {vd['puissances_controles']} -> {decision}")
    print(f"nul hemispheres : mu = {mu:.4f} (m_reel = {m_reel:.4f})")
    jc.ajouter({"type": "demonstration_puissance_mcs05b", "verdict_demo": vd,
                "decision": decision})
    ok, nb = mcs.JournalChaine.verifier(JOURNAL,
                                        genesis="GENESIS-MCS-VALID-PUISSANCE-MCS05B")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
