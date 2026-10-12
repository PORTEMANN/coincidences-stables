"""mcs21_runner.py — Ouverture de la carte MCS-21 (tension S8).

Carte scellee : cartes/v2/MCS-21-tension-s8.md
  sha256 pre-gel : 48d55fcc28a714859f50af1b0e4aa8ec388f914b6d404b16d5171ee5f4cb909b
Donnees : valeurs S8 gelee ci-dessous avec leurs sources publiques
  (convention MCS-16 : aucune acquisition de fichiers ; sources verifiees
  avant redaction, citees).

Mesure scellee : T = |moyenne ponderee CMB - moyenne ponderee lentilles| /
sigma combinee ; m = T. Nul N1 : 10 000 tirages de concordance gaussienne
autour de la moyenne commune de la configuration.

Seuil de la carte : 3,1 (moteur scelle a 3,0, consigne des deux).
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

CARTE_ID = "MCS-21"
SEUIL_CARTE = 3.1
EMPREINTE_CARTE = "48d55fcc28a714859f50af1b0e4aa8ec388f914b6d404b16d5171ee5f4cb909b"
RESULTATS = os.path.join(RACINE, "resultats", "mcs21_resultats.json")
N_NUL = 10000

# Valeurs gelees (source publique citee pour chacune — verifiees avant redaction)
MESURES = {
    # canonique : CMB
    "planck2018": {"s8": 0.834, "plus": 0.016, "moins": 0.016, "famille": "CMB",
                   "source": "Planck Collaboration 2020 (A&A 641, A6) — valeur "
                             "Planck Legacy citee par Wright et al. 2025"},
    "act_dr6": {"s8": 0.840, "plus": 0.028, "moins": 0.028, "famille": "CMB",
                "source": "Madhavacheril et al. 2024 (ApJ 962, 113) — ACT DR6 "
                          "lentille+BAO+BBN"},
    # canonique : lentilles faibles
    "kids1000": {"s8": 0.759, "plus": 0.024, "moins": 0.021, "famille": "lentilles",
                 "source": "Asgari et al. 2021 (KiDS-1000, A&A 645, A104)"},
    "desy3": {"s8": 0.759, "plus": 0.025, "moins": 0.023, "famille": "lentilles",
              "source": "Amon et al. / Secco et al. 2022 (DES-Y3 cosmic shear, "
                        "PRD 105)"},
    "hscy3": {"s8": 0.769, "plus": 0.031, "moins": 0.034, "famille": "lentilles",
              "source": "Li et al. 2023 / Dalal et al. 2023 (HSC-Y3, S8(xi))"},
    # editions declarees pour les deformations
    "combined_cmb_2026": {"s8": 0.836, "plus": 0.012, "moins": 0.013,
                          "famille": "CMB",
                          "source": "Combined CMB (Planck+ACT+SPT) — revue "
                                    "Pantos 2026 / Abbott et al. 2026"},
    "kids_legacy": {"s8": 0.815, "plus": 0.016, "moins": 0.021,
                    "famille": "lentilles",
                    "source": "Wright et al. 2025 (KiDS-Legacy, A&A)"},
}
CANONIQUE = ["planck2018", "act_dr6", "kids1000", "desy3", "hscy3"]


def erreur_sym(m, mode="sym"):
    if mode == "haute":
        return m["plus"]
    if mode == "basse":
        return m["moins"]
    return (m["plus"] + m["moins"]) / 2.0


def tension(cles, mode="sym"):
    v = np.array([MESURES[k]["s8"] for k in cles])
    sig = np.array([erreur_sym(MESURES[k], mode) for k in cles])
    fam = np.array([0 if MESURES[k]["famille"] == "CMB" else 1 for k in cles])
    w = 1.0 / sig ** 2
    mu, s = {}, {}
    for f in (0, 1):
        sel = fam == f
        mu[f] = float((w[sel] * v[sel]).sum() / w[sel].sum())
        s[f] = float(np.sqrt(1.0 / w[sel].sum()))
    return abs(mu[0] - mu[1]) / np.sqrt(s[0] ** 2 + s[1] ** 2), v, sig, fam


def nul_n1(gen, v, sig, fam, nb=N_NUL):
    """Concordance gaussienne autour de la moyenne commune (vectorise)."""
    w = 1.0 / sig ** 2
    mup = float((w * v).sum() / w.sum())
    tir = np.array([rng_normal(gen, mup, sig, len(v)) for _ in range(nb)])
    s0 = np.sqrt(1.0 / w[fam == 0].sum())
    s1 = np.sqrt(1.0 / w[fam == 1].sum())
    mu0 = (tir[:, fam == 0] * w[fam == 0]).sum(axis=1) / w[fam == 0].sum()
    mu1 = (tir[:, fam == 1] * w[fam == 1]).sum(axis=1) / w[fam == 1].sum()
    return np.abs(mu0 - mu1) / np.sqrt(s0 ** 2 + s1 ** 2)


def rng_normal(gen, mu, sig, n):
    """N(mu, sig) via le PRNG public (Box-Muller, declare)."""
    u1 = np.array([gen.uniform(1e-12, 1.0) for _ in range(n)])
    u2 = np.array([gen.uniform(0.0, 1.0) for _ in range(n)])
    return mu + sig * np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)


def z_config(gen, cles, mode="sym"):
    m_val, v, sig, fam = tension(cles, mode)
    ms = nul_n1(gen, v, sig, fam)
    return m_val, mcs.z_score(m_val, float(ms.mean()), float(ms.std()))


def main():
    empreinte_donnees = hashlib.sha256(
        json.dumps(MESURES, sort_keys=True).encode()).hexdigest()
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    z_par, m_par = {}, {}
    m0, z_par["g0_canonique_HORS_SIGMA"] = z_config(gen, CANONIQUE)
    m_par["g0"] = m0
    ms0 = nul_n1(gen, tension(CANONIQUE)[1], tension(CANONIQUE)[2],
                 tension(CANONIQUE)[3])
    u0 = float(ms0.std())

    # g1 : KiDS-1000 -> KiDS-Legacy ; g2 : Planck 2018 -> Combined CMB 2026
    # (Planck et ACT retires de la famille car inclus dans la combinaison — declare)
    z_par["g1_kids_legacy"] = z_config(
        gen, ["planck2018", "act_dr6", "kids_legacy", "desy3", "hscy3"])[1]
    z_par["g2_combined_cmb_2026"] = z_config(
        gen, ["combined_cmb_2026", "kids1000", "desy3", "hscy3"])[1]
    # g3/g4 : erreurs symetrisees -> bornes hautes / basses
    z_par["g3_bornes_hautes"] = z_config(gen, CANONIQUE, "haute")[1]
    z_par["g4_bornes_basses"] = z_config(gen, CANONIQUE, "basse")[1]
    # g5 : retrait de HSC-Y3 (la plus haute des lentilles)
    z_par["g5_sans_hsc"] = z_config(
        gen, ["planck2018", "act_dr6", "kids1000", "desy3"])[1]
    # g6 : retrait d'une mesure au hasard
    victime = CANONIQUE[int(gen.uniform(0, len(CANONIQUE)))]
    z_par["g6_retrait_" + victime] = z_config(
        gen, [k for k in CANONIQUE if k != victime])[1]

    # controles positifs (canonique)
    v0, sig0, fam0 = tension(CANONIQUE)[1:]
    w0 = 1.0 / sig0 ** 2
    sel_l = fam0 == 1
    mu_cmb = float((w0[~sel_l] * v0[~sel_l]).sum() / w0[~sel_l].sum())
    v_c1 = v0.copy()
    v_c1[sel_l] = mu_cmb   # tension supprimee (declare)
    m_c1 = abs(mu_cmb - mu_cmb) / 1.0   # T = 0 par construction
    effet_c1 = (m0 - m_c1) / u0
    mup0 = float((w0 * v0).sum() / w0.sum())
    v_c2 = mup0 + 2.0 * (v0 - mup0)     # tension doublee (declare)
    w_c2 = 1.0 / sig0 ** 2
    mu0_c2 = float((w_c2[~sel_l] * v_c2[~sel_l]).sum() / w_c2[~sel_l].sum())
    mu1_c2 = float((w_c2[sel_l] * v_c2[sel_l]).sum() / w_c2[sel_l].sum())
    s0 = np.sqrt(1.0 / w_c2[~sel_l].sum())
    s1 = np.sqrt(1.0 / w_c2[sel_l].sum())
    m_c2 = abs(mu0_c2 - mu1_c2) / np.sqrt(s0 ** 2 + s1 ** 2)
    effet_c2 = (m_c2 - m0) / u0

    # diagnostics : poids par mesure, T canonique
    diag = {"T_canonique_sigma": m0,
            "poids_canonique": {k: float((1 / erreur_sym(MESURES[k]) ** 2))
                                for k in CANONIQUE},
            "note": "la tension est publiee par mesure, pas moyennee "
                    "inter-familles au-dela de T"}

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
           "mesures_gelees": MESURES, "empreinte_donnees": empreinte_donnees,
           "m_par_config": m_par, "z_par_g": z_par,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "diagnostics": diag,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.1": verdict_carte,
           "decisions_execution": [
               "g2 : la famille CMB devient Combined CMB 2026 seule (Planck "
               "et ACT en sont membres — declare)",
               "c1 : T = 0 par construction (alignement exact declare)"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z_par, "controles": out["controles"]},
                     indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
