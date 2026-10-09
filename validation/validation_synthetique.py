"""validation_synthetique.py — Jalon 2 : le banc prouve sur verite connue.

Cinq scenarios synthetiques :

  CALIB   calibration du banc (PAC plante) -> effets des controles c1, c2
  SYN-A   correspondance plantee (PAC partage entre domaines) -> attendu CS+
  SYN-B   artefact spectral (memes spectres, aucune structure de phase) -> CS-
  SYN-C   loi fausse sur donnees reelles simulees (type MCS-01)     -> CS-
  SYN-D   loi plantee (zero parametre, exacte)                       -> CS+
  SYN-E   statistique aveugle (invariante sous les sabotages)        -> CS0

Regle d'honnetete (consignee au rapport) : pour les scenarios spectraux, la
mesure synthetique est m = couplage phase-amplitude moyen (I4) entre fenetres
et domaines. C'est un substitut de validation : il exerce toute la machinerie
(Sigma = min z_g, double contrainte IAAFT, controles positifs, journal chaine).
La mesure exacte des cartes (distance de Wasserstein entre distributions de
domaines) reste gelee pour les donnees reelles du jalon 4 — elle n'est pas
testee ici et ne sera pas executee avant le gel.

Graine maitresse : 20261009 (consignee). PRNG numpy (synthetique) ; les
campagnes scellees utiliseront ChaCha20-IETF conformement au manifeste.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
sys.path.insert(0, os.path.join(RACINE, "nulls"))

import mcs_score as mcs
import surrogates as nul
import positive_controls as pc
import ash_invariants as ash

FS = 1000.0
DUREE_FENETRE = 10.0
N_FENETRES = 20
N_SURR = 20
N_DOMAINES = 3
GRAINE = 20261009
IAAFT_ITER = 5

JOURNAL = os.path.join(RACINE, "validation", "journal_synthetique.jsonl")
RAPPORT = os.path.join(RACINE, "validation", "rapport_synthetique.md")


# --------------------------------------------------------------------------
# Generateurs synthetiques
# --------------------------------------------------------------------------
def bruit_colore(n: int, pente: float, rng: np.random.Generator) -> np.ndarray:
    """Bruit de DSP ~ f^pente (pente negative)."""
    X = np.fft.rfft(rng.normal(0, 1, n))
    f = np.fft.rfftfreq(n, d=1.0 / FS)
    f[0] = f[1]
    X = X * f ** (pente / 2.0)
    x = np.fft.irfft(X, n=n)
    return x / (x.std() + 1e-12)


def fenetre_avec_pac(pente: float, profondeur: float,
                     rng: np.random.Generator) -> np.ndarray:
    """Fenetre : fond colore de pente donnee + PAC theta->gamma si profondeur>0."""
    n = int(FS * DUREE_FENETRE)
    fond = bruit_colore(n, pente, rng)
    if profondeur <= 0:
        return fond
    t = np.arange(n) / FS
    theta = np.sin(2 * np.pi * 6.0 * t
                   + np.cumsum(rng.normal(0, 0.03, n)))
    phase = np.angle(hilbert(theta))
    gamma = pc._passe_bande(rng.normal(0, 1, n), FS, 38.0, 42.0)
    paquet = (1.0 + profondeur * np.cos(phase)) * gamma
    return fond + 0.8 * theta + paquet


def hilbert(x: np.ndarray) -> np.ndarray:
    return pc._signal_analytique(x)


def dataset_spectral(plante: bool, rng: np.random.Generator) -> dict:
    """3 domaines x 20 fenetres. Si plante : PAC partage (verite connue).
    Sinon : memes spectres, phases independantes (artefact spectral pur)."""
    data = {f"D{i}": [] for i in range(N_DOMAINES)}
    for k in range(N_FENETRES):
        pente = rng.uniform(-1.6, -1.0)
        profondeur = rng.uniform(0.6, 0.9) if plante else 0.0
        for d in range(N_DOMAINES):
            data[f"D{d}"].append(fenetre_avec_pac(pente, profondeur, rng))
    return data


def m_synth(data: dict, fenetre_s: float = DUREE_FENETRE,
            fs: float = FS) -> float:
    """Mesure synthetique : I4 moyen sur fenetres et domaines."""
    vals = []
    for sig in [s for fenetres_d in data.values() for s in fenetres_d]:
        for w in ash.fenetres(sig, fs, fenetre_s):
            vals.append(ash.I4_pac(w, fs))
    return float(np.mean(vals))


def dataset_nul(data: dict, rng: np.random.Generator) -> dict:
    return {d: [nul.iaaft(s, rng, n_iter=IAAFT_ITER) for s in fenetres_d]
            for d, fenetres_d in data.items()}


# --------------------------------------------------------------------------
# Evaluation spectrale (double contrainte, carte MCS-02)
# --------------------------------------------------------------------------
def evaluation_spectrale(data: dict, rng: np.random.Generator,
                         controles: dict) -> dict:
    fs2 = FS / 2.0
    deformations = {
        # g2 : renversement temporel — nul identique par stationnarite
        "g2_renversement": (dict((d, [s[::-1].copy() for s in f])
                                 for d, f in data.items()), DUREE_FENETRE, FS),
        "g5_fenetre_4s": (data, 4.0, FS),
        "g8_500Hz": (dict((d, [s[::2].copy() for s in f])
                          for d, f in data.items()), DUREE_FENETRE, fs2),
    }
    m_data = m_synth(data)
    nuls_base = np.array([m_synth(dataset_nul(data, rng))
                          for _ in range(N_SURR)])
    mu, u = float(nuls_base.mean()), float(nuls_base.std(ddof=1) + 1e-12)
    z_par_g = {"g1_iaaft": mcs.z_score(m_data, mu, u)}
    for nom, (d_g, fen, fs_g) in deformations.items():
        m_g = m_synth(d_g, fen, fs_g)
        if nom == "g2_renversement":
            nuls_g = nuls_base  # stationnarite : meme nul, documente
        else:
            nuls_g = np.array([m_synth(dataset_nul(d_g, rng), fen, fs_g)
                               for _ in range(N_SURR)])
        z_par_g[nom] = mcs.z_score(m_g, float(nuls_g.mean()),
                                   float(nuls_g.std(ddof=1) + 1e-12))
    z_effondrement = -z_par_g["g1_iaaft"]  # mort sous IAAFT (carte section 9b)
    v = mcs.evaluer_double("MCS-02", z_par_g, z_effondrement, controles)
    return {"m": m_data, "mu_null": mu, "u_null": u,
            "z_effondrement": z_effondrement, "verdict": v.to_dict()}


# --------------------------------------------------------------------------
# Evaluation loi zero-parametre (type carte MCS-01)
# --------------------------------------------------------------------------
def loi_candidate(Z: np.ndarray) -> np.ndarray:
    """Loi plantee : y = 0.5 + 1.5 exp(-Z/25). Zero parametre libre."""
    return 0.5 + 1.5 * np.exp(-Z / 25.0)


def m_loi(y: np.ndarray, Z: np.ndarray, loi) -> float:
    rms = float(np.sqrt(np.mean((y - loi(Z)) ** 2)))
    return -np.log10(max(rms, 1e-12))


def famille_lois_lisses(Z: np.ndarray, n: int,
                        rng: np.random.Generator) -> np.ndarray:
    """Nul N3-like de la carte MCS-01 : lois lisses y = b + a exp(-Z/tau),
    a ~ U(0.5, 2.5), tau ~ U(5, 60), b ~ U(0, 1). Matrice (n, len(Z)).
    La permutation seule est un nul trop faible pour des donnees monotones :
    une mauvaise loi monotone y paraitrait 'stable'."""
    a = rng.uniform(0.5, 2.5, size=(n, 1))
    tau = rng.uniform(5.0, 60.0, size=(n, 1))
    b = rng.uniform(0.0, 1.0, size=(n, 1))
    return b + a * np.exp(-Z[None, :] / tau)


def evaluation_loi(y: np.ndarray, Z: np.ndarray, rng: np.random.Generator,
                   controles: dict) -> dict:
    def nul_famille(Zsub, ysub, n=1000):
        m_data = m_loi(ysub, Zsub, loi_candidate)
        del m_data  # le nul ne depend que de la famille, pas de la candidate
        ms = np.array([-np.log10(max(float(np.sqrt(np.mean((ysub - ly) ** 2))),
                                     1e-12))
                       for ly in famille_lois_lisses(Zsub, n, rng)])
        return float(ms.mean()), float(ms.std(ddof=1) + 1e-12)

    z_par_g = {}
    sous = {
        "g1_complet": np.ones(len(Z), bool),
        "g2_pairs": (Z % 2 == 0),
        "g3_impairs": (Z % 2 == 1),
        "g4_Zge20": (Z >= 20),
    }
    for nom, masque in sous.items():
        m_g = m_loi(y[masque], Z[masque], loi_candidate)
        mu, u = nul_famille(Z[masque], y[masque])
        z_par_g[nom] = mcs.z_score(m_g, mu, u)
    v = mcs.evaluer("MCS-01", z_par_g, controles)
    return {"z_par_g": z_par_g, "verdict": v.to_dict()}


def controles_loi(y: np.ndarray, Z: np.ndarray,
                  rng: np.random.Generator) -> dict:
    """Controles du BANC des lois, calcules sur calibration (loi vraie) :
    c1 : briser l'appariement Z<->y (doit effondrer m) ;
    c2 : tau double dans la candidate (doit degrader m)."""
    m_ref = m_loi(y, Z, loi_candidate)
    ms = np.array([m_loi(nul.permutation(y, rng), Z, loi_candidate)
                   for _ in range(500)])
    mu, u = float(ms.mean()), float(ms.std(ddof=1) + 1e-12)
    c1 = pc.effet_u(m_ref, mu, u)
    m_tau2 = m_loi(y, Z, lambda z: 0.5 + 1.5 * np.exp(-z / 50.0))
    c2 = pc.effet_u(m_ref, m_tau2, u)
    return {"c1_appariement": c1, "c2_tau_double": c2}


# --------------------------------------------------------------------------
# Scenario principal
# --------------------------------------------------------------------------
def main() -> int:
    if os.path.exists(JOURNAL):
        os.remove(JOURNAL)
    journal = mcs.JournalChaine(JOURNAL)
    rng = np.random.default_rng(GRAINE)
    resultats = []

    def consigner(scenario, attendu, res):
        obtenu = res["verdict"]["verdict"]
        conforme = (obtenu == attendu)
        journal.ajouter({
            "type": "scenario_synthetique", "scenario": scenario,
            "graine": GRAINE, "attendu": attendu, "obtenu": obtenu,
            "conforme": conforme, "detail": res["verdict"],
        })
        resultats.append((scenario, attendu, obtenu, conforme, res))
        return conforme

    # --- CALIB : controles positifs du banc spectral ----------------------
    rng_cal = np.random.default_rng(GRAINE + 1)
    calib = dataset_spectral(plante=True, rng=rng_cal)
    m_cal = m_synth(calib)
    nuls_cal = np.array([m_synth(dataset_nul(calib, rng_cal))
                         for _ in range(N_SURR)])
    mu_c = float(nuls_cal.mean())
    u_c = float(nuls_cal.std(ddof=1) + 1e-12)
    # c1 : scramble FT sur calibration (la mesure doit s'effondrer)
    ft_cal = {d: [nul.ft_surrogate(s, rng_cal) for s in f]
              for d, f in calib.items()}
    c1 = pc.effet_u(m_cal, m_synth(ft_cal), u_c)
    # c2 : injection d'un PAC connu dans du bruit (I4 doit le voir)
    sig_c2 = pc.injecter_pac(FS, DUREE_FENETRE, 0.8, rng_cal)
    i4_inj = ash.I4_pac(sig_c2, FS)
    i4_bruit = np.array([ash.I4_pac(rng_cal.normal(0, 1, int(FS * DUREE_FENETRE)), FS)
                         for _ in range(20)])
    c2 = pc.effet_u(i4_inj, float(i4_bruit.mean()),
                    float(i4_bruit.std(ddof=1) + 1e-12))
    controles_spectre = {"c1_scramble_FT": c1, "c2_injection_PAC": c2}
    journal.ajouter({"type": "calibration_banc", "graine": GRAINE + 1,
                     "m_calib": m_cal, "mu_null": mu_c, "u_null": u_c,
                     "controles": controles_spectre})

    # --- SYN-A : correspondance plantee -> CS+ ----------------------------
    res_a = evaluation_spectrale(dataset_spectral(True, np.random.default_rng(GRAINE + 10)),
                                 np.random.default_rng(GRAINE + 11),
                                 controles_spectre)
    consigner("SYN-A_correspondance_plantee", "CS+", res_a)

    # --- SYN-B : artefact spectral -> CS- ---------------------------------
    res_b = evaluation_spectrale(dataset_spectral(False, np.random.default_rng(GRAINE + 20)),
                                 np.random.default_rng(GRAINE + 21),
                                 controles_spectre)
    consigner("SYN-B_artefact_spectral", "CS-", res_b)

    # --- SYN-C / SYN-D : banc des lois (type MCS-01) ----------------------
    Z = np.arange(1.0, 93.0)
    # Controles du banc, calcules UNE FOIS sur calibration a loi vraie :
    # les controles prouvent le pouvoir de l'instrument, pas de la carte.
    y_calib_loi = loi_candidate(Z) + np.random.default_rng(GRAINE + 29
                                                           ).normal(0, 0.005, len(Z))
    ctrl_loi = controles_loi(y_calib_loi, Z, np.random.default_rng(GRAINE + 31))
    journal.ajouter({"type": "calibration_banc_lois", "graine": GRAINE + 29,
                     "controles": {k: round(float(v), 4)
                                   for k, v in ctrl_loi.items()}})

    # --- SYN-C : loi fausse (tau=12, candidate tau=25) -> CS- --------------
    rng_c = np.random.default_rng(GRAINE + 30)
    y_fausse = 0.5 + 1.5 * np.exp(-Z / 12.0) + rng_c.normal(0, 0.005, len(Z))
    res_c = evaluation_loi(y_fausse, Z, rng_c, ctrl_loi)
    consigner("SYN-C_loi_fausse", "CS-", res_c)

    # --- SYN-D : loi plantee (tau=25, exacte) -> CS+ -----------------------
    rng_d = np.random.default_rng(GRAINE + 40)
    y_vraie = loi_candidate(Z) + rng_d.normal(0, 0.005, len(Z))
    res_d = evaluation_loi(y_vraie, Z, rng_d, ctrl_loi)
    consigner("SYN-D_loi_plantee", "CS+", res_d)

    # --- SYN-E : statistique aveugle -> CS0 -------------------------------
    # m = puissance moyenne : invariante EXACTE sous surrogates FT.
    # Le controle c1 ne peut rien effondrer : le banc doit repondre CS0.
    rng_e = np.random.default_rng(GRAINE + 50)
    data_e = dataset_spectral(True, rng_e)
    m_e = float(np.mean([np.var(s) for f in data_e.values() for s in f]))
    z_aveugle = {f"g{i}": 5.0 for i in range(1, 5)}  # meme un beau Sigma...
    c1_aveugle = pc.effet_u(m_e, m_e, 0.01)  # ...ne sauve pas un banc aveugle
    v_e = mcs.evaluer("MCS-02", z_aveugle,
                      {"c1_scramble_FT": c1_aveugle, "c2_injection_PAC": c2})
    consigner("SYN-E_banc_aveugle", "CS0", {"verdict": v_e.to_dict()})

    # --- Rapport ----------------------------------------------------------
    ok_chaine, n_rec = mcs.JournalChaine.verifier(JOURNAL)
    rediger_rapport(resultats, controles_spectre, ok_chaine, n_rec)
    tout_conforme = all(c for _, _, _, c, _ in resultats) and ok_chaine
    print(f"{'scenario':<34} {'attendu':<8} {'obtenu':<8} conforme")
    for s, a, o, c, _ in resultats:
        print(f"{s:<34} {a:<8} {o:<8} {'OUI' if c else 'NON'}")
    print(f"\nchaine SHA-256 : {'integre' if ok_chaine else 'ROMPUE'} "
          f"({n_rec} enregistrements)")
    print(f"jalon 2 : {'VALIDE' if tout_conforme else 'A REVOIR'}")
    return 0 if tout_conforme else 1


def rediger_rapport(resultats, controles, ok_chaine, n_rec):
    lignes = [
        "# Rapport de validation synthetique — jalon 2",
        "",
        f"Graine maitresse : `{GRAINE}` — PRNG numpy (synthetique ; les campagnes",
        "scellees utiliseront ChaCha20-IETF, conformement au manifeste).",
        "",
        "## Resultats",
        "",
        "| Scenario | Verite connue | Attendu | Obtenu | Conforme |",
        "|----------|---------------|---------|--------|----------|",
    ]
    for s, a, o, c, res in resultats:
        lignes.append(f"| {s} | — | {a} | {o} | {'oui' if c else 'NON'} |")
    lignes += [
        "",
        "## Controles positifs du banc (calibration)",
        "",
        f"- c1 (scramble FT sur PAC plante) : effet = {controles['c1_scramble_FT']:.2f} u_null",
        f"- c2 (injection d'un PAC connu dans du bruit) : effet = {controles['c2_injection_PAC']:.2f} u_null",
        f"- seuil de pouvoir gele : >= {mcs.SEUIL_CONTROLE} u_null",
        "",
        "## Detail par scenario",
        "",
    ]
    for s, a, o, c, res in resultats:
        v = res["verdict"]
        lignes += [f"### {s}", "",
                   f"- verdict : **{v['verdict']}** — {v['motif']}",
                   f"- Sigma = {v['sigma']:.3f} (seuil {v['seuil']})",
                   f"- z par deformation : "
                   + ", ".join(f"{g} = {z:.2f}" for g, z in v["z_par_g"].items()),
                   ""]
    lignes += [
        "## Honnetete du banc",
        "",
        "1. Pour les scenarios spectraux, la mesure validee est m = couplage",
        "   phase-amplitude moyen (I4). C'est un substitut : il exerce Sigma, la",
        "   double contrainte IAAFT, les controles et le journal. La mesure",
        "   exacte de la carte MCS-02 (Wasserstein inter-domaines) reste gelee",
        "   pour le jalon 4 et n'a pas ete executee ici.",
        "2. Le nul de g2 (renversement temporel) reutilise la distribution nulle",
        "   de base : par stationnarite des surrogates, elles coincident.",
        "3. Pour les scenarios de lois (SYN-C/D), le nul est la famille de lois",
        "   lisses aleatoires (N3-like de la carte MCS-01) : une permutation seule",
        "   est trop faible pour des donnees monotones et ferait paraitre une",
        "   mauvaise loi 'stable'. La regle de marge N2 de la carte (battre le",
        "   meilleur nul ajuste hors-echantillon) reste a exercer au jalon 4.",
        "4. SYN-E demontre que le verdict CS0 prime sur Sigma : une statistique",
        "   aveugle avec Sigma = 5 est refusee. La regle 'controles muets => CS0'",
        "   est cablee dans l'operateur, pas dans l'interpretation.",
        "",
        "## Integrite",
        "",
        f"- journal chaine SHA-256 : {'integre' if ok_chaine else 'ROMPU'}, "
        f"{n_rec} enregistrements (`journal_synthetique.jsonl`).",
        "",
        "## Portee",
        "",
        "Jalon 2 valide le moteur de verdict. Il ne valide ni les donnees, ni",
        "les cartes, ni la physique. Prochain jalon : gel (SHA-256 des cartes",
        "et du code, chainage, horodatage). Aucune donnee reelle avant.",
    ]
    with open(RAPPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")


if __name__ == "__main__":
    sys.exit(main())
