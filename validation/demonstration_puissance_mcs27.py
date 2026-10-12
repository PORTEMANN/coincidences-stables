"""demonstration_puissance_mcs27.py — Regle 1.2 pour la carte MCS-27.

DEFAUT DU BANC (v1.0/v1.1, trouve au premier run du 12/10/2026 —
publie) :
  D1  le blanchiment de Mahalanobis par la covariance de CHAQUE
      configuration diverge sur le nul de l'ampute (g2) — mesure
      structurelle publiee : les 160 matrices de la forme amputee ne
      portent que DEUX vecteurs (K, R) distincts (covariance de rang 1
      — mesuree). v1.1 (seuil de valeurs propres a 1e-12) insuffisant.
      Correction v1.2 (declaree, instrument) : la metrique de
      blanchiment est la covariance du nul CANONIQUE (la forme du
      porteur), fixe pour toutes les configurations — mesuree dans
      l'espace de la configuration ; mu et u restent mesures par
      configuration. La degenerescence de l'ampute est publiee dans
      le journal.

La mesure jointe : le vecteur de forme V = (K, R) — K statistique de
Koide des deux modes massifs (le zero protege ne contribue pas —
declare), R = sigma_max/sigma_min+ ; canal mesure : (Koide(e,mu,tau),
m_tau/m_mu) des tables PDG de la maison (parseur MCS-16, filiation
declaree). Contenu synthetique plante exactement sur le canal -> Sigma
>= 3,0 exige, controles d'instrument resolus a |effet| >= 2 u
(convention MCS-25) ; vecteur tire du nul -> CS- attendu ; banc aveugle
-> CS0.
Nul CONJOINT DE FORME : triplets verifies de la forme mesuree du
porteur a T13 (taille 5, rang(B) = 2, deux valeurs singulieres
distinctes) — enumeration exhaustive par spectres_triplets.py (hache
dans l'acte de gel de MCS-25, filiation declaree) ; la covariance de
blanchiment est celle du nul de la configuration (declaree).
Deformations mesurees a la demo : g1 (PDG 2022), g2 (forme de
l'ampute : taille 4), g4 (R = m_mu/m_e), g5 (espace lineaire), g6
(rang <= 2) ; g3 porte sur le contenu (le plante est fixe — mesuree a
l'execution).
Graine : 20261012 (numpy — tirage du nul et banc aveugle). Journal
chaine dedie.
"""
from __future__ import annotations

import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import spectres_triplets as st  # noqa: E402

GRAINE = 20261012
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs27.jsonl")
SEUIL_CARTE = 3.0
F_PDG24 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2024.mcd")
F_PDG22 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2022.mcd")
TOL = 1e-9   # fige (filiation KO6-REAL-1.0)


def masses_pdg(chemin):
    """Parseur de MCS-16 (filiation declaree), masses en MeV."""
    cibles = {"e", "mu", "tau"}
    out = {}
    for ln in open(chemin):
        if ln.startswith("*") or not ln.strip():
            continue
        nom_ch = ln[106:].split()
        if nom_ch and nom_ch[0] in cibles:
            toks = ln.split()
            try:
                i = next(i for i, t in enumerate(toks)
                         if t[0].isdigit() and ("E" in t or "." in t))
                out[nom_ch[0]] = float(toks[i]) * 1000.0  # GeV -> MeV
            except (ValueError, StopIteration):
                continue
    return out


def koide(a, b, c):
    return (a + b + c) / (np.sqrt(a) + np.sqrt(b) + np.sqrt(c)) ** 2


def vecteurs_nul_forme(taille, rang_max=2, rang_exact=True):
    """Les (K, R) des triplets verifies de la forme declaree (filiere du
    filtre de la demo MCS-26 v2 — declaree) ; rang 1 (g6) : V = (1, 1)."""
    vs = []
    for p in range(1, taille):
        for B in st.blocs_B_vect(p, taille - p):
            sv = np.linalg.svd(B, compute_uv=False)
            smax = sv[:, 0]
            nz = sv > TOL * smax[:, None]
            rang = nz.sum(axis=1)
            masque = (rang == rang_max) if rang_exact else (rang <= rang_max)
            if not masque.any():
                continue
            sv_m, rang_m = sv[masque], rang[masque]
            K = np.ones(len(sv_m))
            R = np.ones(len(sv_m))
            deux = rang_m == 2
            if deux.any():
                a2, b2 = sv_m[deux, 1], sv_m[deux, 0]
                distinct = a2 < b2 - TOL
                R[deux] = np.where(distinct, b2 / np.where(distinct, a2, 1.0),
                                   1.0)
                # Koide de la forme {0, a, b} : (a+b)/(sqrt a + sqrt b)^2
                K[deux] = np.where(
                    distinct,
                    (a2 + b2) / (np.sqrt(a2) + np.sqrt(b2)) ** 2, 1.0)
            vs.append(np.stack([K, R], axis=1))
    return np.concatenate(vs) if vs else np.ones((1, 2))


def blanchir(V_nul, V_mes, espace="log", C_metrique=None):
    """Distance de Mahalanobis a V_mes sous la metrique fixe declaree
    (v1.2 — defaut D1 publie) : la covariance du nul CANONIQUE, mesuree
    dans l'espace de la configuration ; mu et u restent mesures par
    configuration."""
    if espace == "log":
        X = np.log10(V_nul)
        v = np.log10(V_mes)
    else:
        X, v = V_nul, V_mes
    mu = X.mean(axis=0)
    Ci = np.linalg.inv(C_metrique)
    d2 = np.sum((X - v) @ Ci * (X - v), axis=1)
    d_nul = np.sqrt(np.maximum(d2, 0.0))
    return d_nul, mu, C_metrique


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS27")

    m24, m22 = masses_pdg(F_PDG24), masses_pdg(F_PDG22)
    V_mes = {"g0": (koide(m24["e"], m24["mu"], m24["tau"]),
                    m24["tau"] / m24["mu"]),
             "g1": (koide(m22["e"], m22["mu"], m22["tau"]),
                    m22["tau"] / m22["mu"]),
             "g4": (koide(m24["e"], m24["mu"], m24["tau"]),
                    m24["mu"] / m24["e"])}
    print(f"canal mesure : K = {V_mes['g0'][0]:.7f} (Koide, MCS-11) ; "
          f"R = {V_mes['g0'][1]:.4f} (tau/mu)")

    print("Nul conjoint de forme (enumeration exhaustive) :")
    V0 = vecteurs_nul_forme(5)
    V_g2 = vecteurs_nul_forme(4)
    V_g6 = vecteurs_nul_forme(5, rang_exact=False)
    print(f"  comptes : forme porteur {len(V0)} ; forme ampute "
          f"{len(V_g2)} ; rang <= 2 : {len(V_g6)}")
    X_g2 = np.log10(V_g2)
    distincts_g2 = len(np.unique(np.round(X_g2, 9), axis=0))
    print(f"  mesure D1 publiee : la forme amputee ne porte que "
          f"{distincts_g2} vecteurs (K, R) distincts sur {len(V_g2)} "
          f"matrices — covariance de rang 1")

    d0, mu_vec, C = blanchir(V0, V_mes["g0"],
                             C_metrique=np.cov(np.log10(V0).T))
    mu0, u0 = float((-d0).mean()), float((-d0).std())
    C_lin = np.cov(V0.T)     # la metrique canonique en espace lineaire
    confs = {"g1_edition_2022": (V0, V_mes["g1"], "log", C),
             "g2_forme_ampute": (V_g2, V_mes["g0"], "log", C),
             "g4_rapport_mu_e": (V0, V_mes["g4"], "log", C),
             "g5_espace_lineaire": (V0, V_mes["g0"], "lin", C_lin),
             "g6_rang_leq_2": (V_g6, V_mes["g0"], "log", C)}
    z_par = {"g0_canonique": mcs.z_score(0.0, mu0, u0)}
    print(f"  nul canonique : mu = {mu0:.4f}, u = {u0:.4f} ; metrique "
          f"(covariance canonique, log) : [{C[0,0]:.4f} {C[0,1]:.4f} ; "
          f"{C[1,0]:.4f} {C[1,1]:.4f}]")
    for nom, (V_, v_, esp_, C_) in confs.items():
        d_, _, _ = blanchir(V_, v_, esp_, C_metrique=C_)
        mu_, u_ = float((-d_).mean()), float((-d_).std())
        z_par[nom] = mcs.z_score(0.0, mu_, u_)
        print(f"  {nom} : mu = {mu_:.4f}, u = {u_:.4f}, "
              f"z_plante = {z_par[nom]:.3f}")

    # controles d'instrument (convention MCS-25, declaree)
    V_c1 = np.array([[V_mes["g0"][0] / 2.0, V_mes["g0"][1]]])
    d_c1, _, _ = blanchir(np.concatenate([V0, V_c1]), V_mes["g0"],
                          C_metrique=C)
    effet_c1 = (0.0 - (-float(d_c1[-1]))) / u0
    m_cat = -d0
    m_c2 = float(rng.choice(m_cat))
    effet_c2 = (0.0 - m_c2) / u0

    vv = mcs.evaluer_v2("DEFAULT", z_par, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()

    m_tire = float(rng.choice(m_cat))
    z_tire = mcs.z_score(m_tire, mu0, u0)
    v_aveugle = mcs.evaluer_v2("DEFAULT", {"g0": z_par["g0_canonique"]},
                               {"c1": 0.1, "c2": 0.1},
                               attentes={"c1": 1, "c2": 1}).to_dict()

    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                and abs(z_tire) < 2.0
                and v_aveugle["verdict"] == "CS0"
                else "NON SCELLABLE")
    print(f"demo MCS-27 : verdict = {vd['verdict']}, sigma = "
          f"{vd['sigma']:.2f}, puissances = {vd['puissances_controles']}")
    print(f"jambe nul : z = {z_tire:+.2f} (CS- attendu) ; banc aveugle : "
          f"{v_aveugle['verdict']} (CS0 attendu) -> {decision}")
    jc.ajouter({"type": "demonstration_puissance_mcs27",
                "verdict_demo": vd, "decision": decision,
                "canal_mesure": {"K_Koide": V_mes["g0"][0],
                                 "R_tau_mu": V_mes["g0"][1]},
                "nul_conjoint_forme": {
                    "comptes": {"forme_porteur": len(V0),
                                "forme_ampute": len(V_g2),
                                "rang_leq_2": len(V_g6)},
                    "mu_canonique": mu0, "u_canonique": u0,
                    "covariance_metrique_canonique": C.tolist(),
                    "defaut_D1_publie": {"vecteurs_distincts_ampute":
                                         distincts_g2}},
                "jambes": {"vecteur_tire_du_nul_z": z_tire,
                           "banc_aveugle": v_aveugle["verdict"]}})
    ok, nb = mcs.JournalChaine.verifier(
        JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS27")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
