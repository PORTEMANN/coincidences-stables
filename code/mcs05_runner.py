"""mcs05_runner.py — Ouverture de la carte MCS-05 (jalon 4 v2).

Carte scellee : cartes/v2/MCS-05-agregation-EEG-F17.md
  sha256 pre-gel : 177b86c1af4cfa2f3af64f0dd012dac25b786d98c1f636f3a19712c1d8a892be
Donnees : BCICIV-2a (BCI Competition IV, Graz), fichiers GDF d'entrainement
  A01T..A09T, telecharges de la source canonique bbci.de
  (https://www.bbci.de/competition/download/competition_iv/BCICIV_2a_gdf.zip)
  — empreintes sha256 du zip et des 9 fichiers consignees au journal.

Mesure scellee : agregation centroide (moyenne des essais par classe, zero
parametre) ; accuracy euclidienne sur split par essais 70/30 (graine publique
ChaCha20) ; classes gauche (769) / droite (770) ; fenetre 2-4 s post-cue ;
canaux C3/Cz/C4 ; 250 Hz natif ; m = moyenne des accuracies sur les 9 sujets
(un sujet = un domaine — decision d'execution publiee).

Decisions d'execution publiees (carte scellee, rien de re-ajuste) :
- aucune exclusion d'essais marques artefact (non declaree a la carte) ;
- m combine les sujets par moyenne arithmetique (la carte ne fige pas le
  mode de combinaison ; declare ici avant calcul) ;
- IAAFT vectorise, memes etapes que nulls/surrogates.py:iaaft, n_iter = 5
  (comme la demonstration de puissance hachee dans l'acte de gel) ;
- 100 repliques surrogates par configuration (100/fenetre amorti : chaque
  fenetre recoit un surrogate par replique) ;
- g4 reutilise les repliques canoniques hors A03 ; g6 reutilise les fenetres
  canoniques (seul le split change) ;
- seuil de la carte : 3,3 — applique via evaluer_double_v2(carte_id="MCS-02")
  dont le seuil gele du moteur vaut 3,3 (meme valeur, declare).

Double contrainte : (a) Sigma >= 3,3 sur {g2..g6} ; (b) z_effondrement <= -2.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np
import mne

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-05"
EMPREINTE_CARTE = "177b86c1af4cfa2f3af64f0dd012dac25b786d98c1f636f3a19712c1d8a892be"
GDF_DIR = os.environ.get("MCS05_GDF", "/tmp/bciciv")
RESULTATS = os.path.join(RACINE, "resultats", "mcs05_resultats.json")
CKPT = "/tmp/mcs05_ckpt.json"
SUJETS = ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09"]
SUJET_G4_EXCLU = "A03"   # declare a la carte (mesure P44)
N_REP = 100
N_C1 = 200
FS = 250.0

CONFIGS = {
    "g0_canonique": {"win": (500, 1000), "chans": ("EEG-C3", "EEG-Cz", "EEG-C4"),
                     "ref": None, "frac": 0.7},
    "g2_fenetre_1_3s": {"win": (250, 750), "chans": ("EEG-C3", "EEG-Cz", "EEG-C4"),
                        "ref": None, "frac": 0.7},
    "g3_C3_C4": {"win": (500, 1000), "chans": ("EEG-C3", "EEG-C4"),
                 "ref": None, "frac": 0.7},
    "g5_reference_Cz": {"win": (500, 1000), "chans": ("EEG-C3", "EEG-Cz", "EEG-C4"),
                        "ref": "EEG-Cz", "frac": 0.7},
    "g6_split_50_50": {"win": (500, 1000), "chans": ("EEG-C3", "EEG-Cz", "EEG-C4"),
                       "ref": None, "frac": 0.5},
}
CONFIGS_SURR = ["g0_canonique", "g2_fenetre_1_3s", "g3_C3_C4", "g5_reference_Cz"]


def iaaft_vec(X, gen, n_iter=5):
    """IAAFT vectorise — memes etapes que nulls/surrogates.py:iaaft."""
    amp = np.abs(np.fft.rfft(X, axis=1))
    tri = np.sort(X, axis=1)
    ph = gen.uniform(0, 2 * np.pi, size=amp.shape)
    s = np.fft.irfft(amp * np.exp(1j * ph), n=X.shape[1], axis=1)
    for _ in range(n_iter):
        S = np.fft.rfft(s, axis=1)
        s = np.fft.irfft(amp * np.exp(1j * np.angle(S)), n=X.shape[1], axis=1)
        s = np.take_along_axis(tri, np.argsort(np.argsort(s, axis=1), axis=1), axis=1)
    return s


def acc_centroide(X, y, gen, frac):
    idx = gen.permutation(np.arange(len(y)))
    n_tr = int(frac * len(y))
    tr, te = idx[:n_tr], idx[n_tr:]
    c = {k: X[tr][y[tr] == k].mean(axis=0) for k in (0, 1)}
    d = np.stack([np.linalg.norm(X[te] - c[k], axis=tuple(range(1, X.ndim)))
                  for k in (0, 1)])
    return float(np.mean(np.argmin(d, axis=0) == y[te]))


def fenetres_sujet(sujet, win, chans, ref):
    raw = mne.io.read_raw_gdf(os.path.join(GDF_DIR, sujet + "T.gdf"),
                              preload=True, verbose=False)
    ev, _ = mne.events_from_annotations(raw, verbose=False)
    codes = {7: 0, 8: 1}   # 769 gauche, 770 droite
    picks = [raw.ch_names.index(c) for c in chans]
    i_ref = raw.ch_names.index(ref) if ref else None
    data = raw.get_data()
    if i_ref is not None:
        data = data - data[i_ref]
    X, y = [], []
    for pos, _, code in ev:
        if code in codes:
            X.append(data[picks, pos + win[0]: pos + win[1]])
            y.append(codes[code])
    return np.array(X), np.array(y)


def main():
    empreintes = {}
    for s in SUJETS:
        with open(os.path.join(GDF_DIR, s + "T.gdf"), "rb") as f:
            empreintes[s + "T.gdf"] = hashlib.sha256(f.read()).hexdigest()
    empreinte_donnees = hashlib.sha256(
        json.dumps(empreintes, sort_keys=True).encode()).hexdigest()
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    ckpt = {}
    if os.path.exists(CKPT):
        ckpt = json.load(open(CKPT))

    acc_reel = {c: {} for c in CONFIGS}
    acc_surr = {c: np.zeros((N_REP, len(SUJETS))) for c in CONFIGS_SURR}

    for si, suj in enumerate(SUJETS):
        print(f"[sujet {suj}]", flush=True)
        cache = {}
        for c, cfg in CONFIGS.items():
            key = (cfg["win"], cfg["chans"], cfg["ref"])
            if key not in cache:
                cache[key] = fenetres_sujet(suj, cfg["win"], cfg["chans"], cfg["ref"])
            X, y = cache[key]
            acc_reel[c][suj] = acc_centroide(X, y, gen, cfg["frac"])
        for c in CONFIGS_SURR:
            cle = f"{c}|{suj}"
            if cle in ckpt:
                acc_surr[c][:, si] = np.array(ckpt[cle])
                continue
            cfg = CONFIGS[c]
            X, y = cache[(cfg["win"], cfg["chans"], cfg["ref"])]
            for r in range(N_REP):
                Xs = iaaft_vec(X.reshape(len(y), -1), gen).reshape(X.shape)
                acc_surr[c][r, si] = acc_centroide(Xs, y, gen, cfg["frac"])
            ckpt[cle] = acc_surr[c][:, si].tolist()
            with open(CKPT, "w") as f:
                json.dump(ckpt, f)
            print(f"  {c}: 100 repliques terminees", flush=True)

    m_par_config, mu_u = {}, {}
    for c in CONFIGS:
        m_par_config[c] = float(np.mean(list(acc_reel[c].values())))
    for c in CONFIGS_SURR:
        mu_u[c] = (float(acc_surr[c].mean()), float(acc_surr[c].mean(axis=1).std()))
    mu0, u0 = mu_u["g0_canonique"]

    z = {}
    z["g1_iaaft"] = mcs.z_score(m_par_config["g0_canonique"], mu0, u0)
    for c in ("g2_fenetre_1_3s", "g3_C3_C4", "g5_reference_Cz", "g6_split_50_50"):
        mu, u = mu_u[c] if c in mu_u else mu_u["g0_canonique"]
        z[c] = mcs.z_score(m_par_config[c], mu, u)
    # g4 : retrait du sujet le plus lisible (A03, declare a la carte)
    m_g4 = float(np.mean([v for s, v in acc_reel["g0_canonique"].items()
                          if s != SUJET_G4_EXCLU]))
    i8 = [i for i, s in enumerate(SUJETS) if s != SUJET_G4_EXCLU]
    dist_g4 = acc_surr["g0_canonique"][:, i8].mean(axis=1)
    z["g4_sans_A03"] = mcs.z_score(m_g4, float(dist_g4.mean()),
                                   float(dist_g4.std()))
    z_eff = (mu0 - m_par_config["g0_canonique"]) / u0

    # c1 : etiquettes permutees sur donnees reelles (config canonique,
    # fenetres rechargees une fois par sujet et mises en cache)
    cfg0 = CONFIGS["g0_canonique"]
    cache_c1 = {suj: fenetres_sujet(suj, cfg0["win"], cfg0["chans"], cfg0["ref"])
                for suj in SUJETS}
    ms_c1 = np.zeros(N_C1)
    for r in range(N_C1):
        vals = []
        for suj in SUJETS:
            X, y = cache_c1[suj]
            vals.append(acc_centroide(X, gen.permutation(y), gen, cfg0["frac"]))
        ms_c1[r] = np.mean(vals)
    effet_c1 = (m_par_config["g0_canonique"] - float(ms_c1.mean())) / u0
    # c2 : ERD synthetique dans bruit pur, etiquettes factices declarees
    n_f, n_pts = 96, 500
    y_fact = np.arange(n_f) % 2
    t = np.arange(n_pts) / FS
    Xn = np.stack([0.5 * np.sin(2 * np.pi * 10 * t) *
                   (1.0 if c == 0 else 0.05) +
                   gen.uniform(0, 1, n_pts) * 2 - 1
                   for c in y_fact]).reshape(n_f, 1, n_pts)
    rec = acc_centroide(Xn, y_fact, gen, 0.7)
    effet_c2 = abs(rec - 0.5) / u0

    v = mcs.evaluer_double_v2("MCS-02", z, z_eff,
                              {"c1": effet_c1, "c2": effet_c2},
                              attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    out = {"carte": CARTE_ID, "empreinte_carte_pre_gel": EMPREINTE_CARTE,
           "empreintes_gdf": empreintes, "empreinte_donnees": empreinte_donnees,
           "accuracy_reelle_par_config": m_par_config,
           "accuracy_reelle_par_sujet": {c: acc_reel[c] for c in CONFIGS},
           "mu_u_n1_par_config": mu_u,
           "z_par_g": z, "z_effondrement": z_eff,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "verdict": vd}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": vd["sigma"], "verdict": vd["verdict"],
                      "z_par_g": z, "z_effondrement": z_eff,
                      "controles": out["controles"],
                      "m_canonique": m_par_config["g0_canonique"],
                      "mu_n1": mu0, "u_n1": u0}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
