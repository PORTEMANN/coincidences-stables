"""demonstration_puissance_mcs25.py — Regle 1.2 pour la carte MCS-25 (v2).

CORRECTION PRE-GEL DECLAREE (unique, precedent MCS-20) : la v1 (table
complete des 8 fermions) est IMPUISSANTE — plafond mesure sigma = 1,46
— publiee (demonstration_puissance_mcs25_v1.py et son journal). La
correction est la regle de forme spectrale : le porteur a deux modes
massifs ; l'arene mesuree a deux rapports independants deja peses est
le canal des leptons charges {e, mu, tau} (precedent MCS-11). Les
controles sont des controles d'instrument sur contenus de reference
(declare).

Contenu synthetique plante exactement sur une entree de la table
(declare : le rapport mu/e — present dans toutes les configurations du
groupe) -> Sigma >= 3,0 exige, controles resolus a |effet| >= 2 u ;
rapport tire du nul -> CS- attendu ; banc aveugle -> CS0.
Nul REEL SPECTRAL : enumeration exhaustive des matrices verifiees de la
fenetre n in [2,6] (code/spectres_triplets.py — reimplementation
declaree de T1 ; regression tuante aux comptes publies de MCS-24).
Deformations mesurees a la demo : g1 (PDG 2022), g5 (metrique
relative), g6 (poids uniforme par taille) ; g2 (fenetre n <= 7) mesure
a l'execution (cout declare) ; g3, g4 portent sur le contenu (le plante
est fixe — mesurees a l'execution).
Graine : 20261012 (numpy — tirage du nul et banc aveugle). Journal
chaine dedie.
"""
from __future__ import annotations

import itertools
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import spectres_triplets as st  # noqa: E402

GRAINE = 20261012
JOURNAL = os.path.join(RACINE, "validation", "journal_puissance_mcs25.jsonl")
SEUIL_CARTE = 3.0
F_PDG24 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2024.mcd")
F_PDG22 = os.path.join(RACINE, "donnees", "mcs04_mass_width_2022.mcd")
FENETRE_DEMO = 6          # n in [2,6] — fenetre canonique gelee
CANAL = ("e", "mu", "tau")


def masses_pdg(chemin):
    """Parseur de MCS-16 (filiation declaree), masses en MeV."""
    cibles = {"e", "mu", "tau", "u", "d", "s", "c", "b", "t", "W", "Z",
              "H", "p", "n"}
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


def table_rapports(masses, objets):
    """Les rapports m_i/m_j > 1 de la table (lexique gele)."""
    vals = [masses[o] for o in objets]
    rs = [a / b for a, b in itertools.permutations(vals, 2) if a > b]
    return np.array(sorted(rs))


def sieges(rapports_nul, table, metrique="log"):
    """s(x) = min_R |log10(x/R)| (ou ecart relatif |x-R|/R pour g5)."""
    if metrique == "log":
        d = np.abs(np.log10(rapports_nul[:, None] / table[None, :]))
    else:
        d = np.abs(rapports_nul[:, None] - table[None, :]) / table[None, :]
    return d.min(axis=1)


def centre_plus_grand_intervalle(table):
    """Centre geometrique du plus grand intervalle logarithmique de la
    table (controle c1 — declare)."""
    lt = np.log10(table)
    i = int(np.argmax(np.diff(lt)))
    return float(10 ** ((lt[i] + lt[i + 1]) / 2))


def mu_u_poids(m_par_taille, poids_tailles):
    """(mu, u) ponderes : poids par matrice (naturel) ou uniforme par
    taille (g6)."""
    mus, vs = [], []
    for n in sorted(m_par_taille):
        mn = m_par_taille[n]
        mus.append((float(mn.mean()), float(mn.var())))
    if poids_tailles == "uniforme":
        w = np.ones(len(mus)) / len(mus)
    else:
        w = np.array([len(m_par_taille[n]) for n in sorted(m_par_taille)],
                     dtype=float)
        w /= w.sum()
    mu = float(sum(wi * mi for wi, (mi, _) in zip(w, mus)))
    var = float(sum(wi * (vi + (mi - mu) ** 2)
                    for wi, (mi, vi) in zip(w, mus)))
    return mu, float(np.sqrt(var))


def main():
    rng = np.random.default_rng(GRAINE)
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    jc = mcs.JournalChaine(JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS25")

    print("Nul reel spectral : enumeration des matrices (fenetre n <= 6) :")
    spectres = st.spectres_par_taille(FENETRE_DEMO)
    assert st.regression_comptes(spectres), \
        "REGRESSION TUEE : les comptes ne reproduisent pas MCS-24"
    comptes = {n: spectres[n][0] for n in spectres}
    print("  comptes par taille (regression MCS-24 PASS) :", comptes)

    m24 = masses_pdg(F_PDG24)
    m22 = masses_pdg(F_PDG22)
    t24 = table_rapports(m24, CANAL)
    t22 = table_rapports(m22, CANAL)
    print(f"  canal leptonique : {len(t24)} rapports ; centre du plus "
          f"grand intervalle : {centre_plus_grand_intervalle(t24):.3f}")

    # sieges par taille (m = -s) pour chaque configuration de table/metrique
    def m_par_taille(table, metrique):
        return {n: -sieges(spectres[n][1], table, metrique)
                for n in spectres}

    m0t = m_par_taille(t24, "log")
    mu0, u0 = mu_u_poids(m0t, "naturel")
    mu1, u1 = mu_u_poids(m_par_taille(t22, "log"), "naturel")
    mu5, u5 = mu_u_poids(m_par_taille(t24, "rel"), "naturel")
    mu6, u6 = mu_u_poids(m0t, "uniforme")
    print(f"  nul canonique : mu = {mu0:.4f}, u = {u0:.4f} "
          f"(g1 : {mu1:.4f}/{u1:.4f} ; g5 : {mu5:.4f}/{u5:.4f} ; "
          f"g6 : {mu6:.4f}/{u6:.4f})")

    # contenu plante : exactement mu/e (present partout — declare)
    r_plante = m24["mu"] / m24["e"]
    assert abs(sieges(np.array([r_plante]), t24)[0]) < 1e-12
    z_par = {"g0_canonique": mcs.z_score(0.0, mu0, u0),
             "g1_edition_2022": mcs.z_score(0.0, mu1, u1),
             "g5_metrique_relative": mcs.z_score(0.0, mu5, u5),
             "g6_poids_uniforme_taille": mcs.z_score(0.0, mu6, u6)}

    # controles d'instrument (contenus de reference — correction declaree)
    r_c1 = centre_plus_grand_intervalle(t24)
    m_c1 = -float(sieges(np.array([r_c1]), t24)[0])
    effet_c1 = (0.0 - m_c1) / u0          # siege parfait -> gap : degrade
    m_c2 = float(rng.choice(np.concatenate([m0t[n] for n in m0t])))
    effet_c2 = (0.0 - m_c2) / u0          # tire du nul contraste au parfait

    vv = mcs.evaluer_v2("DEFAULT", z_par, {"c1": effet_c1, "c2": effet_c2},
                        attentes={"c1": 1, "c2": 1})
    vd = vv.to_dict()

    # jambe 2 : un rapport tire du nul -> CS- attendu
    m_tire = float(rng.choice(np.concatenate([m0t[n] for n in m0t])))
    z_tire = mcs.z_score(m_tire, mu0, u0)
    # jambe 3 : banc aveugle (controles muets simules) -> CS0 attendu
    v_aveugle = mcs.evaluer_v2("DEFAULT", {"g0": z_par["g0_canonique"]},
                               {"c1": 0.1, "c2": 0.1},
                               attentes={"c1": 1, "c2": 1}).to_dict()

    decision = ("SCELLABLE" if vd["sigma"] >= SEUIL_CARTE
                and all(p >= 2.0 for p in vd["puissances_controles"].values())
                and abs(z_tire) < 2.0
                and v_aveugle["verdict"] == "CS0"
                else "NON SCELLABLE")
    print(f"demo MCS-25 v2 : verdict = {vd['verdict']}, sigma = "
          f"{vd['sigma']:.2f}, puissances = {vd['puissances_controles']}")
    print(f"jambe nul : z = {z_tire:+.2f} (CS- attendu) ; banc aveugle : "
          f"{v_aveugle['verdict']} (CS0 attendu) -> {decision}")
    jc.ajouter({"type": "demonstration_puissance_mcs25", "version": "v2",
                "correction_declaree": "canal leptonique charge (regle de "
                    "forme spectrale) + controles d'instrument ; v1 "
                    "impuissante publiee (plafond mesure 1,46)",
                "verdict_demo": vd, "decision": decision,
                "nul_reel_spectral": {
                    "fenetre": [2, FENETRE_DEMO],
                    "comptes_par_taille": {str(n): int(c)
                                           for n, c in comptes.items()},
                    "mu_canonique": mu0, "u_canonique": u0,
                    "g1": [mu1, u1], "g5": [mu5, u5], "g6": [mu6, u6]},
                "jambes": {"rapport_tire_du_nul_z": z_tire,
                           "banc_aveugle": v_aveugle["verdict"]}})
    ok, nb = mcs.JournalChaine.verifier(
        JOURNAL, genesis="GENESIS-MCS-VALID-PUISSANCE-MCS25")
    print(f"chaine : {ok} ({nb} records)")


if __name__ == "__main__":
    main()
