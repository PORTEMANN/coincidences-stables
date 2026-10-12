"""demonstration_puissance_mcs26.py — Regle 1.2 pour la carte MCS-26.

Contenu synthetique plante exactement sur le canal (declare : R_nu de
la configuration canonique NuFIT 6.0 IC19) -> Sigma >= 3,0 exige,
controles d'instrument resolus a |effet| >= 2 u (convention MCS-25) ;
rapport tire du nul -> CS- attendu ; banc aveugle -> CS0.
Nul REEL SPECTRAL des masses^2 : q(D) = r(D)^2 sur toutes les matrices
verifiees de la fenetre n in [2,7] (code/spectres_triplets.py — hache
dans l'acte de gel de MCS-25, filiation declaree ; regression tuante
aux comptes publies de MCS-24, n = 7 compris).
Canal : acquisition declaree du 12/10/2026 (donnees/mcs26/ — valeurs
transcrites des tables NuFIT epinglees, empreintes reconsignees).
Deformations mesurees a la demo : g1 (NuFIT 5.2), g2 (fenetre n <= 6),
g5 (metrique relative), g6 (poids uniforme par taille) ; g3, g4 portent
sur le contenu (le plante est fixe — mesurees a l'execution).
Graine : 20261012 (numpy — tirage du nul et banc aveugle). Journal
chaine dedie.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import spectres_triplets as st  # noqa: E402

GRAINE = 20261012
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs26.jsonl")
SEUIL_CARTE = 3.0
F_ACQ = os.path.join(RACINE, "donnees", "mcs26", "nufit_splittings.json")
FENETRE_DEMO = 7          # n in [2,7] — fenetre canonique gelee


def canal(cle):
    s = json.load(open(F_ACQ, encoding="utf-8"))["splittings"][cle]
    return s["dm31_e-3"] * 1e-3 / (s["dm21_e-5"] * 1e-5), s


def mesures(q_nul, R, metrique="log"):
    if metrique == "log":
        return -np.abs(np.log10(q_nul / R))
    return -np.abs(q_nul - R) / R


def mu_u_poids(m_par_taille, poids):
    tailles = sorted(m_par_taille)
    stats = [(float(m_par_taille[n].mean()), float(m_par_taille[n].var()))
             for n in tailles]
    if poids == "uniforme":
        w = np.ones(len(tailles)) / len(tailles)
    else:
        w = np.array([len(m_par_taille[n]) for n in tailles], dtype=float)
        w /= w.sum()
    mu = float(sum(wi * mi for wi, (mi, _) in zip(w, stats)))
    var = float(sum(wi * (vi + (mi - mu) ** 2)
                    for wi, (mi, vi) in zip(w, stats)))
    return mu, float(np.sqrt(var))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS26")

    R0, _ = canal("v60_IC19_sans_SKatm_NO")
    R1, _ = canal("v52_sans_SKatm_NO")
    print(f"canal : R_nu canonique (NuFIT 6.0 IC19) = {R0:.4f} ; "
          f"g1 (5.2) = {R1:.4f}")

    print("Nul reel spectral des masses^2 (fenetre n <= 7, vectorise) :")
    sp7 = st.spectres_par_taille(7, vect=True)
    assert st.regression_comptes(sp7), \
        "REGRESSION TUEE : les comptes ne reproduisent pas MCS-24"
    comptes = {n: sp7[n][0] for n in sp7}
    print("  comptes par taille (regression MCS-24 PASS) :", comptes)
    q = {n: sp7[n][1] ** 2 for n in sp7}

    def m_par_taille(qq, R, metrique):
        return {n: mesures(qq[n], R, metrique) for n in qq}

    m0t = m_par_taille(q, R0, "log")
    mu0, u0 = mu_u_poids(m0t, "naturel")
    mu1, u1 = mu_u_poids(m_par_taille(q, R1, "log"), "naturel")
    mu2, u2 = mu_u_poids({n: m0t[n] for n in m0t if n <= 6}, "naturel")
    mu5, u5 = mu_u_poids(m_par_taille(q, R0, "rel"), "naturel")
    mu6, u6 = mu_u_poids(m0t, "uniforme")
    print(f"  nul canonique : mu = {mu0:.4f}, u = {u0:.4f} "
          f"(g1 : {mu1:.4f}/{u1:.4f} ; g2 : {mu2:.4f}/{u2:.4f} ; "
          f"g5 : {mu5:.4f}/{u5:.4f} ; g6 : {mu6:.4f}/{u6:.4f})")

    # contenu plante : exactement R_nu (siege parfait, m = 0)
    z_par = {"g0_canonique": mcs.z_score(0.0, mu0, u0),
             "g1_edition_5.2": mcs.z_score(0.0, mu1, u1),
             "g2_fenetre_6": mcs.z_score(0.0, mu2, u2),
             "g5_metrique_relative": mcs.z_score(0.0, mu5, u5),
             "g6_poids_uniforme_taille": mcs.z_score(0.0, mu6, u6)}

    # controles d'instrument (convention MCS-25, declaree)
    m_c1 = mesures(np.array([R0 * 8.0]), R0)[0]      # plante deplace x8
    effet_c1 = (0.0 - m_c1) / u0
    m_cat = np.concatenate([m0t[n] for n in sorted(m0t)])
    m_c2 = float(rng.choice(m_cat))
    effet_c2 = (0.0 - m_c2) / u0

    vv = mcs.evaluer_v2("DEFAULT", z_par, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()

    # jambe 2 : un rapport tire du nul -> CS- attendu
    m_tire = float(rng.choice(m_cat))
    z_tire = mcs.z_score(m_tire, mu0, u0)
    # jambe 3 : banc aveugle -> CS0 attendu
    v_aveugle = mcs.evaluer_v2("DEFAULT", {"g0": z_par["g0_canonique"]},
                               {"c1": 0.1, "c2": 0.1},
                               attentes={"c1": 1, "c2": 1}).to_dict()

    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                and abs(z_tire) < 2.0
                and v_aveugle["verdict"] == "CS0"
                else "NON SCELLABLE")
    print(f"demo MCS-26 : verdict = {vd['verdict']}, sigma = "
          f"{vd['sigma']:.2f}, puissances = {vd['puissances_controles']}")
    print(f"jambe nul : z = {z_tire:+.2f} (CS- attendu) ; banc aveugle : "
          f"{v_aveugle['verdict']} (CS0 attendu) -> {decision}")
    jc.ajouter({"type": "demonstration_puissance_mcs26",
                "verdict_demo": vd, "decision": decision,
                "canal": {"R_nu_canonique_v60_IC19": R0,
                          "R_nu_g1_v52": R1},
                "nul_reel_spectral_masses2": {
                    "fenetre": [2, FENETRE_DEMO],
                    "comptes_par_taille": {str(n): int(c)
                                           for n, c in comptes.items()},
                    "mu_canonique": mu0, "u_canonique": u0,
                    "g1": [mu1, u1], "g2": [mu2, u2],
                    "g5": [mu5, u5], "g6": [mu6, u6]},
                "jambes": {"rapport_tire_du_nul_z": z_tire,
                           "banc_aveugle": v_aveugle["verdict"]}})
    ok, nb = mcs.JournalChaine.verifier(
        JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS26")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
