"""mcs27_runner.py — Ouverture de la carte MCS-27 (mesure jointe de forme).

Carte scelle : cartes/v2/MCS-27-mesure-jointe-forme.md
  sha256 pre-gel : 61cedbfeef7b8a358749aabc7e494d84a8cb8cbf7314016f8ad28b7735b77974
Donnees : tables PDG deja acquises (MCS-04/16/25 — empreintes
  reconsignees ; parseur de MCS-16, filiation declaree) ; contenu : le
  porteur a son vide (formes closes declarees : K = 5-2*sqrt5,
  R = phi^2 — spectre mesure T7 ; zero protege T13) ; le nul conjoint
  de forme : enumeration exhaustive (spectres_triplets.py — hache dans
  l'acte de gel de MCS-25 ; regression aux comptes mesures de la demo).

Mesure scellee : V(D) = (K, R) ; ecart = distance de Mahalanobis a
  V_mes dans l'espace (log10 K, log10 R), blanchie par la covariance du
  nul CANONIQUE (metrique fixe declaree — defaut D1 de la demo publie :
  le nul de l'ampute ne porte que 2 vecteurs distincts) ; m = -delta.
Controles d'instrument (convention MCS-25) : c1 : reference plantee sur
  V_mes puis K -> K/2 ; c2 : reference tiree du nul (PRNG public).

Seuil de la carte : 3,0 (moteur scelle a 3,0, consigne des deux).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402
import spectres_triplets as st  # noqa: E402

CARTE_ID = "MCS-27"
SEUIL_CARTE = 3.0
EMPREINTE_CARTE = "61cedbfeef7b8a358749aabc7e494d84a8cb8cbf7314016f8ad28b7735b77974"
RESULTATS = os.path.join(RACINE, "resultats", "mcs27_resultats.json")
F_PDG24 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2024.mcd")
F_PDG22 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2022.mcd")
TOL = 1e-9   # fige (filiation KO6-REAL-1.0)

# Contenus geles (formes closes declarees de la carte) :
SQ5 = np.sqrt(5.0)
V_VIDE = (5.0 - 2.0 * SQ5, (3.0 + SQ5) / 2.0)          # vide T7 (rho=√5)
# g3 : vide a Lambda = 2,5 (rho = 1,5) : spectre {0, 0,5 ; 2,5} :
K_G3 = 3.0 / (np.sqrt(0.5) + np.sqrt(2.5)) ** 2
V_G3 = (K_G3, 5.0)


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
                K[deux] = np.where(
                    distinct,
                    (a2 + b2) / (np.sqrt(a2) + np.sqrt(b2)) ** 2, 1.0)
            vs.append(np.stack([K, R], axis=1))
    return np.concatenate(vs) if vs else np.ones((1, 2))


def blanchir(V_nul, V_mes, C_metrique, espace="log"):
    """Distance de Mahalanobis sous la metrique fixe declaree (carte)."""
    if espace == "log":
        X = np.log10(V_nul)
        v = np.log10(np.asarray(V_mes, dtype=float))
    else:
        X, v = V_nul, np.asarray(V_mes, dtype=float)
    Ci = np.linalg.inv(C_metrique)
    d2 = np.sum((X - v) @ Ci * (X - v), axis=1)
    return np.sqrt(np.maximum(d2, 0.0))


def main():
    brut = {f: open(f, "rb").read() for f in (F_PDG24, F_PDG22)}
    empreintes = {os.path.basename(f_): hashlib.sha256(b).hexdigest()
                  for f_, b in brut.items()}
    constants = {"V_VIDE": list(V_VIDE), "V_G3": list(V_G3),
                 "empreintes_tables": empreintes}
    empreinte_donnees = hashlib.sha256(
        json.dumps(constants, sort_keys=True).encode()).hexdigest()
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode())
        .digest())

    m24, m22 = masses_pdg(F_PDG24), masses_pdg(F_PDG22)
    V_mes = {"g0": (koide(m24["e"], m24["mu"], m24["tau"]),
                    m24["tau"] / m24["mu"]),
             "g1": (koide(m22["e"], m22["mu"], m22["tau"]),
                    m22["tau"] / m22["mu"]),
             "g4": (koide(m24["e"], m24["mu"], m24["tau"]),
                    m24["mu"] / m24["e"])}
    print(f"canal mesure : K = {V_mes['g0'][0]:.7f} ; R = "
          f"{V_mes['g0'][1]:.4f} ; contenu : V_vide = "
          f"({V_VIDE[0]:.7f}, {V_VIDE[1]:.7f})")

    print("Nul conjoint de forme (enumeration exhaustive) :")
    V0 = vecteurs_nul_forme(5)
    V_g2 = vecteurs_nul_forme(4)
    V_g6 = vecteurs_nul_forme(5, rang_exact=False)
    print(f"  comptes : forme porteur {len(V0)} ; ampute {len(V_g2)} ; "
          f"rang <= 2 : {len(V_g6)}")

    C_log = np.cov(np.log10(V0).T)     # la metrique fixe declaree
    C_lin = np.cov(V0.T)
    d0 = blanchir(V0, V_mes["g0"], C_log)
    mu0, u0 = float((-d0).mean()), float((-d0).std())

    def mesure_contenu(Vc, Vm, nul, C_, esp="log"):
        d_nul = blanchir(nul, Vm, C_, esp)
        mu, u = float((-d_nul).mean()), float((-d_nul).std())
        m_c = -float(blanchir(np.asarray(Vc)[None, :], Vm, C_, esp)[0])
        rang = float(np.mean(d_nul <= -m_c))
        return m_c, mcs.z_score(m_c, mu, u), rang

    z_par, m_par, rangs = {}, {}, {}
    m0, z_par["g0_canonique_HORS_SIGMA"], rangs["g0"] = mesure_contenu(
        V_VIDE, V_mes["g0"], V0, C_log)
    m_par["g0"] = m0
    m1, z_par["g1_edition_2022"], rangs["g1"] = mesure_contenu(
        V_VIDE, V_mes["g1"], V0, C_log)
    m_par["g1"] = m1
    m2, z_par["g2_forme_ampute"], rangs["g2"] = mesure_contenu(
        V_VIDE, V_mes["g0"], V_g2, C_log)
    m_par["g2"] = m2
    m3, z_par["g3_vide_Lambda2.5"], rangs["g3"] = mesure_contenu(
        V_G3, V_mes["g0"], V0, C_log)
    m_par["g3"] = m3
    m4, z_par["g4_rapport_mu_e"], rangs["g4"] = mesure_contenu(
        V_VIDE, V_mes["g4"], V0, C_log)
    m_par["g4"] = m4
    m5, z_par["g5_espace_lineaire"], rangs["g5"] = mesure_contenu(
        V_VIDE, V_mes["g0"], V0, C_lin, "lin")
    m_par["g5"] = m5
    m6, z_par["g6_rang_leq_2"], rangs["g6"] = mesure_contenu(
        V_VIDE, V_mes["g0"], V_g6, C_log)
    m_par["g6"] = m6

    # controles d'instrument (convention MCS-25 — declaree)
    V_c1 = (V_mes["g0"][0] / 2.0, V_mes["g0"][1])
    m_c1 = -float(blanchir(np.asarray(V_c1)[None, :], V_mes["g0"],
                           C_log)[0])
    effet_c1 = (0.0 - m_c1) / u0
    d_sorted = np.sort(d0)
    u_draw = float(gen.uniform(0.0, 1.0))
    m_c2 = -float(d_sorted[min(int(u_draw * len(d_sorted)),
                               len(d_sorted) - 1)])
    effet_c2 = (0.0 - m_c2) / u0

    # N2 : composantes du vecteur mesure permutees entre les triplets du
    # nul (rapporte — documente) : on permute les composantes du nul
    V_perm = V0[:, ::-1]
    d_perm = blanchir(V_perm, V_mes["g0"], np.cov(np.log10(V_perm).T))
    m_perm = -d_perm
    n2_note = {"mu": float(m_perm.mean()), "u": float(m_perm.std()),
               "m_contenu_mesure_sous_n2": -float(
                   blanchir(np.asarray(V_VIDE)[None, :], V_mes["g0"],
                            np.cov(np.log10(V_perm).T))[0])}

    diag = {"ecart_porteur_blanchi": -m0,
            "composantes": {"log_K": float(np.log10(V_VIDE[0])
                                         - np.log10(V_mes["g0"][0])),
                            "log_R": float(np.log10(V_VIDE[1])
                                           - np.log10(V_mes["g0"][1]))},
            "correlation_nul_logK_logR": float(
                np.corrcoef(np.log10(V0.T)[0], np.log10(V0.T)[1])[0, 1]),
            "vecteurs_distincts_ampute": int(
                len(np.unique(np.round(np.log10(V_g2), 9), axis=0))),
            "rangs_dans_le_nul_conjoint": rangs,
            "comptes_nul": {"forme_porteur": len(V0), "ampute": len(V_g2),
                            "rang_leq_2": len(V_g6)},
            "n2_permutation_composantes": n2_note,
            "nul_canonique": [mu0, u0],
            "note": "la metrique de blanchiment est la covariance du nul "
                    "canonique (fixe, declaree) ; la degenerescence de "
                    "l'ampute (defaut D1) est mesuree"}

    v = mcs.evaluer_v2("DEFAULT", z_par, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1},
                       exclure=("g0_canonique_HORS_SIGMA",))
    vd = v.to_dict()
    s = vd["sigma"]
    if vd["verdict"] == "CS0":
        verdict_carte = "CS0"
    elif s >= SEUIL_CARTE:
        verdict_carte = "CS+"
    elif s >= 2.0:
        verdict_carte = "CSp"
    elif s <= -2.0:
        verdict_carte = "CSi"
    else:
        verdict_carte = "CS-"

    out = {"carte": CARTE_ID, "empreinte_carte_pre_gel": EMPREINTE_CARTE,
           "constantes_gelees": constants,
           "empreinte_donnees": empreinte_donnees,
           "m_par_config": m_par, "z_par_g": z_par,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "diagnostics": diag,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.0": verdict_carte,
           "decisions_execution": [
               "le nul conjoint de forme est enumere exhaustivement — "
               "jamais tire",
               "controles d'instrument sur references (convention "
               "MCS-25) ; tirage par echantillonnage inverse "
               "(convention MCS-24)",
               "la metrique de blanchiment est la covariance du nul "
               "canonique (fixe, declaree)"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z_par, "controles": out["controles"],
                      "ecart_porteur_blanchi": -m0}, indent=2,
                     default=float))
    return out


if __name__ == "__main__":
    main()
