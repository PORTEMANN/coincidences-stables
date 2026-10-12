"""demonstration_puissance_mcs26.py — Regle 1.2 pour la carte MCS-26 (v2).

CORRECTION PRE-GEL DECLAREE (unique, precedents MCS-20/25) : la v1 (nul
reel spectral complet de la fenetre) est IMPUISSANTE — sigma = 2,05,
c2 = 1,18 u — publiee (demonstration_puissance_mcs26_v1.py et son
journal). La correction est le NUL DE FORME : la correspondance est
declaree par la forme spectrale mesuree du porteur (T13 : un mode nul
protege + deux modes massifs — taille 5, rang(B) = 2, deux valeurs
singulieres distinctes) ; le nul pertinent est l'ensemble des triplets
de la fenetre ayant exactement cette forme.

Contenu synthetique plante exactement sur le canal (declare : R_nu de
la configuration canonique NuFIT 6.0 IC19) -> Sigma >= 3,0 exige,
controles d'instrument resolus a |effet| >= 2 u (convention MCS-25) ;
rapport tire du nul -> CS- attendu ; banc aveugle -> CS0.
Enumeration : code/spectres_triplets.py (hache dans l'acte de gel de
MCS-25, filiation declaree) ; le filtre de forme est declare ici :
rang(B) exactement 2 et deux valeurs singulieres non nulles distinctes
(TOL = 1e-9 fige).
Deformations mesurees a la demo : g1 (NuFIT 5.2), g2 (forme de
l'ampute : taille 4, rang 2 — T13), g5 (metrique relative), g6 (rang
<= 2) ; g3, g4 portent sur le contenu (le plante est fixe — mesurees a
l'execution).
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
TOL = 1e-9   # fige (filiation KO6-REAL-1.0)


def canal(cle):
    s = json.load(open(F_ACQ, encoding="utf-8"))["splittings"][cle]
    return s["dm31_e-3"] * 1e-3 / (s["dm21_e-5"] * 1e-5)


def mesures(q_nul, R, metrique="log"):
    if metrique == "log":
        return -np.abs(np.log10(q_nul / R))
    return -np.abs(q_nul - R) / R


def nul_de_forme(taille, rang_max=2, rang_exact=True):
    """Les q = (sigma_max/sigma_min+)^2 des triplets verifies de la forme
    declaree : taille donnee, rang(B) = 2 (ou <= 2 pour g6), deux
    valeurs singulieres non nulles DISTINCTES (le rang 1 a q = 1 —
    inclus en g6 par rang <= 2 avec q = 1)."""
    qs = []
    for p in range(1, taille):
        for B in st.blocs_B_vect(p, taille - p):
            sv = np.linalg.svd(B, compute_uv=False)
            smax = sv[:, 0]
            nz = sv > TOL * smax[:, None]
            rang = nz.sum(axis=1)
            if rang_exact:
                masque = rang == rang_max
            else:
                masque = rang <= rang_max
            if not masque.any():
                continue
            sv_m = sv[masque]
            r1 = rang[masque] == 1
            q = np.ones(len(sv_m))
            deux = ~r1
            if deux.any():
                smin2 = sv_m[deux, 1]
                smax2 = sv_m[deux, 0]
                distinct = smin2 < smax2 - TOL
                q2 = np.ones(int(deux.sum()))
                q2[distinct] = (smax2[distinct] / smin2[distinct]) ** 2
                # rang 2 mais valeurs egales : q = 1 (declare)
                q[deux] = q2
            qs.append(q)
    return np.concatenate(qs) if qs else np.array([1.0])


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS26")

    R0 = canal("v60_IC19_sans_SKatm_NO")
    R1 = canal("v52_sans_SKatm_NO")
    print(f"canal : R_nu canonique (NuFIT 6.0 IC19) = {R0:.4f} ; "
          f"g1 (5.2) = {R1:.4f}")

    print("Nul reel DE FORME (taille 5, rang 2, distinct) :")
    q0 = nul_de_forme(5)
    q_g2 = nul_de_forme(4)              # l'ampute (T13) — declare
    q_g6 = nul_de_forme(5, rang_exact=False)   # rang <= 2 — declare
    print(f"  comptes : forme porteur {len(q0)} ; forme ampute "
          f"{len(q_g2)} ; rang <= 2 : {len(q_g6)}")

    mu0, u0 = float(mesures(q0, R0).mean()), float(mesures(q0, R0).std())
    m1 = mesures(q0, R1)
    mu1, u1 = float(m1.mean()), float(m1.std())
    m2 = mesures(q_g2, R0)
    mu2, u2 = float(m2.mean()), float(m2.std())
    m5 = mesures(q0, R0, "rel")
    mu5, u5 = float(m5.mean()), float(m5.std())
    m6 = mesures(q_g6, R0)
    mu6, u6 = float(m6.mean()), float(m6.std())
    print(f"  nul canonique : mu = {mu0:.4f}, u = {u0:.4f} "
          f"(g1 : {mu1:.4f}/{u1:.4f} ; g2 : {mu2:.4f}/{u2:.4f} ; "
          f"g5 : {mu5:.4f}/{u5:.4f} ; g6 : {mu6:.4f}/{u6:.4f})")

    # contenu plante : exactement R_nu (siege parfait, m = 0)
    z_par = {"g0_canonique": mcs.z_score(0.0, mu0, u0),
             "g1_edition_5.2": mcs.z_score(0.0, mu1, u1),
             "g2_forme_ampute": mcs.z_score(0.0, mu2, u2),
             "g5_metrique_relative": mcs.z_score(0.0, mu5, u5),
             "g6_rang_leq_2": mcs.z_score(0.0, mu6, u6)}

    # controles d'instrument (convention MCS-25, declaree)
    m_c1 = mesures(np.array([R0 * 8.0]), R0)[0]
    effet_c1 = (0.0 - m_c1) / u0
    m_c2 = float(rng.choice(mesures(q0, R0)))
    effet_c2 = (0.0 - m_c2) / u0

    vv = mcs.evaluer_v2("DEFAULT", z_par, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()

    m_tire = float(rng.choice(mesures(q0, R0)))
    z_tire = mcs.z_score(m_tire, mu0, u0)
    v_aveugle = mcs.evaluer_v2("DEFAULT", {"g0": z_par["g0_canonique"]},
                               {"c1": 0.1, "c2": 0.1},
                               attentes={"c1": 1, "c2": 1}).to_dict()

    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                and abs(z_tire) < 2.0
                and v_aveugle["verdict"] == "CS0"
                else "NON SCELLABLE")
    print(f"demo MCS-26 v2 : verdict = {vd['verdict']}, sigma = "
          f"{vd['sigma']:.2f}, puissances = {vd['puissances_controles']}")
    print(f"jambe nul : z = {z_tire:+.2f} (CS- attendu) ; banc aveugle : "
          f"{v_aveugle['verdict']} (CS0 attendu) -> {decision}")
    jc.ajouter({"type": "demonstration_puissance_mcs26", "version": "v2",
                "correction_declaree": "nul de forme (taille 5, rang 2, "
                    "distinct — la forme mesuree du porteur a T13) ; v1 "
                    "impuissante publiee (sigma = 2,05)",
                "verdict_demo": vd, "decision": decision,
                "canal": {"R_nu_canonique_v60_IC19": R0,
                          "R_nu_g1_v52": R1},
                "nul_de_forme": {
                    "comptes": {"forme_porteur": len(q0),
                                "forme_ampute": len(q_g2),
                                "rang_leq_2": len(q_g6)},
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
