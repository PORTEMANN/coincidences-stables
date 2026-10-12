"""mcs24_runner.py — Ouverture de la carte MCS-24 (tarif BH x porteur repare).

Carte scellee : cartes/v2/MCS-24-tarif-bh-porteur-repare.md
  sha256 pre-gel : 5ab3ca699aa49ca21047726b656a47e1c586d2c94c48c48eb61de194085bb1db
Donnees : contenu repare du corpus (porteur PORTEUR-KO6-A3b-DIM5 : N_F = 5,
  mesure et publie aux verdicts T5/T6/T7 ; C4 : N_F = 4 — declares) ;
  constantes CODATA deja acquises (MCS-08/16) ; le nul reel : comptes de
  triplets nus verifies par taille, calcules par la machine des orbites
  (filiation T1/T5 du corpus — reimplementation declaree).

Mesure scellee : m = -|log10(N_eff / N_req)| ; N_req = (3pi/2)·(M_P/Lambda)^2
(chaine gelee de MCS-23 : 1/G_ind = (2/3pi)·N_eff·f2·Lambda^2 ; f2 = 1 ;
Lambda = M_P non reduite, canonique). Nul N1 : distribution de m sur les
triplets nus verifies de la fenetre (n in [2,7]), ponderee par les comptes
mesures — exacte, calculee, pas tiree.

Seuil de la carte : 3,0 (moteur scelle a 3,0, consigne des deux).
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-24"
SEUIL_CARTE = 3.0
EMPREINTE_CARTE = "5ab3ca699aa49ca21047726b656a47e1c586d2c94c48c48eb61de194085bb1db"
RESULTATS = os.path.join(RACINE, "resultats", "mcs24_resultats.json")

# Constantes gelees (declarations de la carte) :
G_2022 = 6.67430e-11      # CODATA 2022 (deja acquise, MCS-08/16)
G_2018 = 6.67408e-11      # CODATA 2018 (edition declaree pour g2)
M_P = 1.2209e19           # Planck non reduite, GeV (convention gelee)
F2_GEL = 1.0              # moment de la fonction test (gele)
N_REQ_BASE = 3 * np.pi / 2
CONTENU_PORTEUR = 5       # N_F du porteur repare (mesure T5/T6/T7)
CONTENU_C4 = 4            # triplet verifie C4 du corpus (erratum declare)


# --- machine des orbites (filiation T1/T5 du corpus — declaree)
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


def comptes_par_taille(n_max):
    comptes = {}
    for n in range(2, n_max + 1):
        tot = 0
        for p in range(1, n):
            q = n - p
            for sigma, s in involutions_signees(p, q):
                tot += compte_D_orbites(sigma, s, p, q)
        comptes[n] = tot
    return comptes


def n_req(G, Lambda):
    """N_req = (3pi/2)·(M_P(G)/Lambda)^2 avec M_P² = hbar·c/G (gele)."""
    m_p = M_P * np.sqrt(G_2022 / G)
    return N_REQ_BASE * (m_p / Lambda) ** 2


def mesure(n, nreq):
    return -abs(np.log10(n / nreq))


def nul_reel(comptes, nreq, pond="comptes"):
    tailles = np.array(sorted(comptes), dtype=float)
    if pond == "comptes":
        w = np.array([comptes[int(t)] for t in tailles], dtype=float)
    else:
        w = np.ones(len(tailles))
    w /= w.sum()
    gaps = np.array([mesure(t, nreq) for t in tailles])
    mu = float(np.sum(gaps * w))
    u = float(np.sqrt(np.sum((gaps - mu) ** 2 * w)))
    return mu, u, gaps, w


def z_config(comptes, nreq, n_content, pond="comptes"):
    mu, u, gaps, w = nul_reel(comptes, nreq, pond)
    m_val = mesure(n_content, nreq)
    p_rang = float(np.sum(w[gaps >= m_val]))
    return m_val, mcs.z_score(m_val, mu, u), p_rang


def main():
    constants = {"G_2022": G_2022, "G_2018": G_2018, "M_P": M_P,
                 "f2": F2_GEL, "N_REQ_BASE": N_REQ_BASE,
                 "contenu_porteur": CONTENU_PORTEUR, "contenu_C4": CONTENU_C4}
    empreinte_donnees = hashlib.sha256(
        json.dumps(constants, sort_keys=True).encode()).hexdigest()
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    print("Calcul du nul reel (fenetre n <= 7, machine des orbites) :")
    comptes7 = comptes_par_taille(7)
    comptes8 = None

    z_par, m_par, rangs = {}, {}, {}
    nreq0 = n_req(G_2022, M_P)
    m0, z_par["g0_canonique_HORS_SIGMA"], rangs["g0"] = z_config(
        comptes7, nreq0, CONTENU_PORTEUR)
    m_par["g0"] = m0
    mu0, u0, gaps0, w0 = nul_reel(comptes7, nreq0)

    # g1 : coupure reduite ; g2 : G edition 2018 ; g3 : fenetre n <= 8 ;
    # g4 : contenu C4 ; g5 : porteur ampute du noeud C ; g6 : nul uniforme
    m_par["g1"], z_par["g1_coupure_reduite"], rangs["g1"] = z_config(
        comptes7, n_req(G_2022, M_P / np.sqrt(8 * np.pi)), CONTENU_PORTEUR)
    m_par["g2"], z_par["g2_CODATA_2018"], rangs["g2"] = z_config(
        comptes7, n_req(G_2018, M_P), CONTENU_PORTEUR)
    comptes8 = comptes_par_taille(8)
    m_par["g3"], z_par["g3_fenetre_8"], rangs["g3"] = z_config(
        comptes8, nreq0, CONTENU_PORTEUR)
    m_par["g4"], z_par["g4_contenu_C4"], rangs["g4"] = z_config(
        comptes7, nreq0, CONTENU_C4)
    m_par["g5"], z_par["g5_porteur_ampute_noeud_C"], rangs["g5"] = z_config(
        comptes7, nreq0, CONTENU_PORTEUR - 1)
    m_par["g6"], z_par["g6_nul_uniforme_par_taille"], rangs["g6"] = z_config(
        comptes7, nreq0, CONTENU_PORTEUR, pond="uniforme")

    # controles positifs (canonique) : c1 : contenu deplace x8 ;
    # c2 : taille tiree du nul pondere par echantillonnage inverse
    # (uniforme + poids cumules — declare ; le PRNG public n'a pas de
    # methode choice : la convention est publiee ici)
    effet_c1 = (m0 - mesure(40, nreq0)) / u0
    tailles0 = np.array(sorted(comptes7), dtype=float)
    u_draw = float(gen.uniform(0.0, 1.0))
    idx = min(int(np.searchsorted(np.cumsum(w0), u_draw)), len(tailles0) - 1)
    m_c2 = float(mesure(tailles0[idx], nreq0))
    effet_c2 = (m0 - m_c2) / u0

    diag = {"delta_canonique_dex": -m0, "N_req_canonique": nreq0,
            "comptes_nul_par_taille": {str(int(k)): int(v)
                                       for k, v in comptes7.items()},
            "rangs_dans_le_nul_reel": {k: round(v, 6)
                                       for k, v in rangs.items()},
            "note": "la proximite du porteur vit au cadran non reduit ; "
                    "g1 mesure la dependance a la convention de Planck"}

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
               "le nul reel est calcule (machine des orbites, filiation "
               "T1/T5 declaree) — jamais tire",
               "g5 : le porteur ampute de son noeud C a N_F = 4 "
               "(declare)"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z_par, "controles": out["controles"]},
                     indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
