"""mcs02_runner.py — Execution unique MCS-02 (jalon 4).

Carte : MCS-02-ASH-signaux.md (SHA256_CARTE 0aa840f23ca4516ae5f76342be950694d0dcd4c204e02ea7ad0c8b1f08fa167a).
Hache et consigne au journal JALON-4 AVANT execution.

Donnees : MANIFESTE-ACQUISITION-MCS02.json (fenetres tirees, offsets publies,
empreintes). Le runner re-verifie l'empreinte_donnees avant tout calcul.

PRNG (doctrine jalon 4) : cle = SHA-256("MCS-J4|" + empreinte_carte + "|" +
empreinte_donnees), ChaCha20-IETF, nonce nulle.
Ordre des tirages (publie) :
  1. N1 (IAAFT, 100 generations x 240 fenetres) pour les configurations dans
     l'ordre [g1_iaaft (base), g2, g3, g4, g5, g6, g7, g8] ;
  2. N2 (100 generations de signaux a DSP moyenne de domaine, phase aleatoire) ;
  3. N3 (100 permutations des etiquettes de domaine) ;
  4. c1 (1 permutation d'etiquettes) ; 5. c2 (60 signaux PAC geles injectes) ;
  6. c3 (60 metronomes 1 Hz + bruit).

Conventions declarees :
  - m = -(moyenne des 6 distances euclidiennes entre moyennes de domaines dans
    l'espace I standardise) ; standardisation (moyenne/ecart-type par invariant)
    calculee UNE FOIS sur les 240 fenetres reelles de la configuration de base
    et reappliquee a toutes les configurations et tous les nuls (comparabilite) ;
  - d_W entre moyennes ponctuelles = euclidienne (lecture litterale du lexique :
    'd_W(moyennes de domaines)') ;
  - z_g = (m_g - mu_N1,g)/u_g ; z_par_g contient g1_iaaft..g8 ; Sigma = min sur
    {g2..g8} (le moteur gele exclut g1_iaaft) ;
  - z_effondrement = (mu_N1,base - m_base)/u_N1,base : <= -2 exige (double
    contrainte carte section 9) ;
  - g5 : 4 premieres secondes de chaque fenetre tiree (aucun nouveau tirage) ;
  - g6 : espace (I1, I2, I3) (I4 retire) ; g7 : les fenetres du sujet i sont
    remplacees par celles du sujet (i+1) mod 20 (memes indices) ;
  - c2 : x_EEG + injecter_pac(1000, 10, profondeur=1.0, rng) (generateur gele,
    theta 6 Hz x gamma 40 Hz) ; effet = (I4_c2 - I4_EEG)/sigma_I4 ;
  - c3 : metronome = impulsions gaussiennes 1 Hz (sigma_p = 2 ms, amplitude 1)
    + bruit gaussien sigma = 0,01 ; effet = |I3_c3 - I3_ECG|/sigma_I3.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys

import numpy as np
from scipy.signal import resample_poly

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
sys.path.insert(0, os.path.join(RACINE, "nulls"))
from mcs_score import evaluer_double  # noqa: E402
from prng_chacha import PRNGChaCha  # noqa: E402
from ash_invariants import vecteur_invariants  # noqa: E402
from surrogates import iaaft  # noqa: E402
from positive_controls import injecter_pac  # noqa: E402

EMPREINTE_CARTE = "0aa840f23ca4516ae5f76342be950694d0dcd4c204e02ea7ad0c8b1f08fa167a"
D = os.path.join(RACINE, "donnees")
DOMAINES = ("EEG", "ECG", "ALLEN", "CWRU")
N_GEN = 100


def sha256_fichier(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def to_fs(x, fs_in, fs_out):
    if fs_in == fs_out:
        return np.asarray(x, dtype=float)
    g = math.gcd(int(fs_in), int(fs_out))
    return resample_poly(np.asarray(x, dtype=float), fs_out // g, fs_in // g)


def charger_fenetres(man, canal_eeg="Cz", hp="1HP", fs_out=1000):
    """Retourne {domaine: [60 fenetres a fs_out Hz]}."""
    out = {"EEG": [], "ECG": [], "ALLEN": [], "CWRU": []}
    for sub, info in sorted(man["eeg_fenetres"].items()):
        n_ch, n_s = info["n_ch"], info["n_samples"]
        raw = np.fromfile(f"{D}/eeg/{sub}.fdt", dtype="<f4").reshape(n_s, n_ch)
        col = info["idx"][canal_eeg]
        for w in info["fenetres"]:
            x = raw[w * 5000:(w + 1) * 5000, col]
            out["EEG"].append(to_fs(x, 500, fs_out))
    for f in man["ecg_fenetres"]:
        x = np.load(f"{D}/{f['fichier']}")
        out["ECG"].append(to_fs(x, 128, fs_out))
    for f in man["allen_fenetres"]:
        x = np.load(f"{D}/{f['fichier']}")
        out["ALLEN"].append(to_fs(x, f["fs"], fs_out))
    for f in man[f"cwru_{hp}"]["fenetres"]:
        x = np.load(f"{D}/{f['fichier']}")
        out["CWRU"].append(to_fs(x, 12000, fs_out))
    assert all(len(v) == 60 for v in out.values())
    return out


def matrice_I(fenetres_par_domaine, fs, duree=None):
    vecs, etiquettes = [], []
    for dom in DOMAINES:
        for x in fenetres_par_domaine[dom]:
            if duree is not None:
                x = x[:int(duree * fs)]
            vecs.append(vecteur_invariants(x, fs))
            etiquettes.append(dom)
    return np.array(vecs), etiquettes


def m_mesure(vecs_std, etiquettes, n_inv=4):
    moy = {}
    for dom in DOMAINES:
        idx = [i for i, e in enumerate(etiquettes) if e == dom]
        moy[dom] = vecs_std[idx, :n_inv].mean(axis=0)
    paires = [(a, b) for i, a in enumerate(DOMAINES) for b in DOMAINES[i + 1:]]
    d = np.mean([np.linalg.norm(moy[a] - moy[b]) for a, b in paires])
    return -float(d)


def main():
    man = json.load(open(f"{D}/MANIFESTE-ACQUISITION-MCS02.json", encoding="utf-8"))
    assert man["empreinte_carte"] == EMPREINTE_CARTE
    # re-verification de l'empreinte donnees (liage)
    emp = {k: sha256_fichier(os.path.join(D, k)) for k in sorted(man["empreintes_fichiers"])}
    canon = "\n".join(f"{k}:{emp[k]}" for k in sorted(emp))
    emp_donnees = hashlib.sha256(canon.encode()).hexdigest()
    assert emp_donnees == man["empreinte_donnees"], "empreinte donnees : divergence"

    cle = hashlib.sha256(f"MCS-J4|{EMPREINTE_CARTE}|{emp_donnees}".encode("ascii")).digest()
    rng = PRNGChaCha(cle)
    empreinte_flot = rng._octets(64).hex()

    # --- configuration de base + standardisation de reference ---------------
    fen_base = charger_fenetres(man)
    vecs_base, etiq_base = matrice_I(fen_base, 1000)
    mu_I, sd_I = vecs_base.mean(axis=0), vecs_base.std(axis=0)
    std_base = (vecs_base - mu_I) / sd_I
    m_base = m_mesure(std_base, etiq_base)
    print(f"[base] m = {m_base:+.4f}")

    CONFIGS = {
        "g1_iaaft": lambda: (vecs_base, etiq_base, 1000),
        "g2_renversement": lambda: (*matrice_I({d: [x[::-1] for x in fen_base[d]] for d in DOMAINES}, 1000), 1000),
        "g3_eeg_O1": lambda: (*matrice_I(charger_fenetres(man, canal_eeg="O1"), 1000), 1000),
        "g4_cwru_3HP": lambda: (*matrice_I(charger_fenetres(man, hp="3HP"), 1000), 1000),
        "g5_fenetres_4s": lambda: (*matrice_I(fen_base, 1000, duree=4.0), 1000),
        "g6_sans_I4": lambda: (vecs_base, etiq_base, 1000),
        "g7_sujets_tournes": lambda: (rotation_sujets(vecs_base), etiq_base, 1000),
        "g8_500Hz": lambda: (*matrice_I(charger_fenetres(man, fs_out=500), 500), 500),
    }

    def rotation_sujets(vecs):
        eeg = vecs[:60].reshape(20, 3, 4)
        eeg = np.roll(eeg, 1, axis=0)  # sujet i <- fenetres du sujet i-1
        return np.vstack([eeg.reshape(60, 4), vecs[60:]])

    fenetres_config = {"g1_iaaft": fen_base,
                       "g2_renversement": {d: [x[::-1] for x in fen_base[d]] for d in DOMAINES},
                       "g3_eeg_O1": charger_fenetres(man, canal_eeg="O1"),
                       "g4_cwru_3HP": charger_fenetres(man, hp="3HP"),
                       "g5_fenetres_4s": {d: [x[:4000] for x in fen_base[d]] for d in DOMAINES},
                       "g6_sans_I4": fen_base,
                       "g7_sujets_tournes": fen_base,
                       "g8_500Hz": charger_fenetres(man, fs_out=500)}
    fs_config = {"g8_500Hz": 500}

    z_par_g, detail = {}, {}
    fs_b = 1000
    for nom in ["g1_iaaft", "g2_renversement", "g3_eeg_O1", "g4_cwru_3HP",
                "g5_fenetres_4s", "g6_sans_I4", "g7_sujets_tournes", "g8_500Hz"]:
        vecs, etiq, fs = CONFIGS[nom]()
        if nom == "g7_sujets_tournes":
            vecs_std = (vecs - mu_I) / sd_I
        else:
            vecs_std = (vecs - mu_I) / sd_I
        n_inv = 3 if nom == "g6_sans_I4" else 4
        m_reel = m_mesure(vecs_std, etiq, n_inv)
        # N1 : 100 generations IAAFT
        fen = fenetres_config[nom]
        fsc = fs_config.get(nom, 1000)
        duree_c = 4.0 if nom == "g5_fenetres_4s" else None
        ms = np.empty(N_GEN)
        for g in range(N_GEN):
            vg, eg = [], []
            for dom in DOMAINES:
                for x in fen[dom]:
                    xs = iaaft(x, rng)
                    if duree_c is not None:
                        xs = xs[:int(duree_c * fsc)]
                    vg.append(vecteur_invariants(xs, fsc))
                    eg.append(dom)
            vg = (np.array(vg) - mu_I) / sd_I
            if nom == "g7_sujets_tournes":
                vg = rotation_sujets(vg * sd_I + mu_I)
                vg = (vg - mu_I) / sd_I
            ms[g] = m_mesure(vg, eg, n_inv)
        mu, u = float(np.mean(ms)), float(np.std(ms))
        z = (m_reel - mu) / u
        z_par_g[nom] = z
        detail[nom] = {"m": m_reel, "mu_null": mu, "u_null": u, "z": z}
        print(f"[{nom:18s}] m={m_reel:+7.4f}  mu={mu:+7.4f}  u={u:.4f}  z={z:+8.3f}")

    z_effondrement = (detail["g1_iaaft"]["mu_null"] - m_base) / detail["g1_iaaft"]["u_null"]

    # --- N2 : bruit de meme DSP moyenne de domaine ----------------------------
    specs = {}
    for dom in DOMAINES:
        X = np.array([np.abs(np.fft.rfft(x)) for x in fen_base[dom]])
        specs[dom] = X.mean(axis=0)
    ms_n2 = np.empty(N_GEN)
    for g in range(N_GEN):
        vg, eg = [], []
        for dom in DOMAINES:
            for _ in range(60):
                ph = rng.uniform(0.0, 2 * np.pi, size=len(specs[dom]))
                ph[0] = 0.0
                ph[-1] = 0.0  # composante de Nyquist reelle (n pair)
                xs = np.fft.irfft(specs[dom] * np.exp(1j * ph), n=10000)
                vg.append(vecteur_invariants(xs, 1000))
                eg.append(dom)
        ms_n2[g] = m_mesure((np.array(vg) - mu_I) / sd_I, eg)
    # --- N3 : permutations d'etiquettes ---------------------------------------
    ms_n3 = np.empty(N_GEN)
    etiq_arr = np.array(etiq_base)
    for g in range(N_GEN):
        ms_n3[g] = m_mesure(std_base, list(rng.permutation(etiq_arr)))
    # --- c1 : une permutation d'etiquettes ------------------------------------
    m_c1 = m_mesure(std_base, list(rng.permutation(etiq_arr)))
    effet_c1 = (m_base - m_c1) / detail["g1_iaaft"]["u_null"]
    # --- c2 : injection PAC dans l'EEG ----------------------------------------
    # Controle fort (carte section 7 : 'sinon I4 est aveugle') : injection a
    # amplitude 10x l'ecart-type de la fenetre (le couplage doit dominer la
    # bande ; une injection non mise a l'echelle serait indetectable sur des
    # signaux en microvolts — declare).
    i4_c2 = []
    for x in fen_base["EEG"]:
        xp = injecter_pac(1000, 10.0, 1.0, rng)
        alpha = 10.0 * float(np.std(x)) / float(np.std(xp))
        i4_c2.append(vecteur_invariants(x + alpha * xp, 1000)[3])
    i4_eeg = vecs_base[:60, 3].mean()
    sigma_i4 = vecs_base[:, 3].std()
    effet_c2 = (float(np.mean(i4_c2)) - float(i4_eeg)) / float(sigma_i4)
    # --- c3 : metronome 1 Hz + bruit ------------------------------------------
    t = np.arange(10000) / 1000.0
    i3_c3 = []
    for _ in range(60):
        phase = rng.uniform(0, 1)
        xm = np.exp(-((t - phase) % 1.0 - 0.002) ** 2 / (2 * 0.002 ** 2)) + 0.01 * rng.normal(0, 1, len(t))
        i3_c3.append(vecteur_invariants(xm, 1000)[2])
    i3_ecg = vecs_base[60:120, 2].mean()
    sigma_i3 = vecs_base[:, 2].std()
    effet_c3 = abs(float(np.mean(i3_c3)) - float(i3_ecg)) / float(sigma_i3)

    controles = {"c1": effet_c1, "c2": effet_c2}
    v = evaluer_double("MCS-02", z_par_g, z_effondrement, controles, g_surrogate="g1_iaaft")

    res = {
        "carte": "MCS-02",
        "empreinte_carte": EMPREINTE_CARTE,
        "empreinte_donnees": emp_donnees,
        "prng": {"algorithme": "ChaCha20-IETF, nonce nulle", "cle_publique_hex": cle.hex(),
                 "empreinte_flot_64o": empreinte_flot, "octets_consumes": rng.tirages,
                 "ordre_tirages": "N1 (8 configs) puis N2, N3, c1, c2, c3"},
        "configurations": detail,
        "z_effondrement": z_effondrement,
        "N2_dsp_moyenne": {"m_moyenne": float(np.mean(ms_n2)), "u": float(np.std(ms_n2))},
        "N3_melange": {"m_moyenne": float(np.mean(ms_n3)), "u": float(np.std(ms_n3)),
                       "quantile_m_base": float(np.mean(ms_n3 <= m_base))},
        "controles": {"c1": {"m_melange": m_c1, "effet_u": effet_c1},
                      "c2": {"I4_injecte": float(np.mean(i4_c2)), "I4_base": float(i4_eeg),
                             "effet_u": effet_c2},
                      "c3": {"I3_metronome": float(np.mean(i3_c3)), "I3_ecg": float(i3_ecg),
                             "effet_u": effet_c3}},
        "verdict": v.to_dict(),
    }
    return res


if __name__ == "__main__":
    res = main()
    os.makedirs(os.path.join(RACINE, "resultats"), exist_ok=True)
    sortie = os.path.join(RACINE, "resultats", "mcs02_resultats.json")
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("\n=== VERDICT MCS-02 ===")
    print(json.dumps(res["verdict"], ensure_ascii=False, indent=2))
    print("sha256(resultats) =", hashlib.sha256(open(sortie, "rb").read()).hexdigest())
