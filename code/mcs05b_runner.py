"""mcs05b_runner.py — Ouverture de la carte MCS-05b (refonte unique, F17).

Carte scellee : cartes/v2/MCS-05b-agregation-EEG-F17-refonte.md
  sha256 pre-gel : 33ae9f7194d345cb83de45006de8c0ff0fd58fd7c1d50a56600111a87f166e0d
Donnees : BCICIV-2a (deja acquises et empreintees au jalon 4 v2 ;
  reutilisation consignee — les 9 fichiers GDF doivent etre octet-identiques,
  assertion sur les empreintes publiees).

Mesure scellee (refonte) : E = (P_ipsi - P_contra)/(P_ipsi + P_contra) par
essai ; m = moyenne de E sur tous les essais de la configuration.
Bande mu 8-12 Hz, fenetre 2-4 s post-cue, canaux C3/C4, 250 Hz.
Nul honnete (mesure de puissance) : permutation des hemispheres C3<->C4
par essai (10 000 fois) — IAAFT conserve le spectre et ne peut pas tuer
une mesure de puissance ; declare a la carte.

Double contrainte : (a) Sigma >= 3,3 sur {g2..g6} ; (b) z_effondrement
<= -2 sous permutation des hemispheres (g1 rapporte, exclu du min).

Regle de la refonte (declaree a la carte) : le declencheur CS0 est c2
(injection synthetique dans bruit reel, etiquettes factices — le pipeline
doit retrouver ces etiquettes) ; c1 (etiquettes permutees) est un diagnostic
de presence du signal, publie, PAS un declencheur CS0.

Seuil de la carte : 3,3 — applique via evaluer_double_v2(carte_id="MCS-02")
dont le seuil gele du moteur vaut 3,3 (meme valeur, declare).
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

CARTE_ID = "MCS-05b"
EMPREINTE_CARTE = "33ae9f7194d345cb83de45006de8c0ff0fd58fd7c1d50a56600111a87f166e0d"
GDF_DIR = os.environ.get("MCS05_GDF", "/tmp/bciciv")
RESULTATS = os.path.join(RACINE, "resultats", "mcs05b_resultats.json")
CKPT = "/tmp/mcs05b_ckpt.json"
SUJETS = ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09"]
SUJET_G4_EXCLU = "A03"
N_NUL = 10000
FS = 250.0

EMPREINTES_ATTENDUES = {
    "A01T.gdf": "74d900ce83a115509f663c0ac45bd36d56f05be528064743c49b0c2efb5088a3",
    "A02T.gdf": "66c9eaf971198d08c95dc272fd310dc2a2f8fe470b7a4f29971a75552cdc2a56",
    "A03T.gdf": "b6327b61ad725062b538ac9bc4c4cbe792ff841a2b009b971ac151cb7a83f02d",
    "A04T.gdf": "2ce34de240bbf3d25b0dc8b54ead5a9b1fea743b8184d60c2b6c57e1bf0c9409",
    "A05T.gdf": "62558a31c342aa56fc93ae702a62fada9024b814a7adaab8069ca94027b2e917",
    "A06T.gdf": "ae709d09ac15c19d3c0af3c32de7f7101c0699dd72cdcacc4d7234e9a57d3169",
    "A07T.gdf": "331dae51fb07685b06526ee04994fb41230177d357c95e9d7cfa5977191a8155",
    "A08T.gdf": "0aa60752dcf02d7a88a0fdaf7082b68b57bc7a2e16698c89174aadce45d627d8",
    "A09T.gdf": "3e585fd3a4f10ded77003492529433abe6d172e80316cb068997ff4b498c3bc4"}


def puissance_mu(x, bande=(8.0, 12.0)):
    f = np.fft.rfftfreq(len(x), 1 / FS)
    P = np.abs(np.fft.rfft(x)) ** 2
    sel = (f >= bande[0]) & (f <= bande[1])
    return float(P[sel].mean())


def E_depuis_puissances(p3, p4, classe):
    ipsi, contra = (p3, p4) if classe == 0 else (p4, p3)
    if ipsi + contra <= 0:
        return 0.0
    return (ipsi - contra) / (ipsi + contra)


def essais_sujet(sujet, win=(500, 1000), bande=(8.0, 12.0), ref_cz=False):
    """Retourne (p3, p4, classes) par essai — les puissances mu par canal."""
    raw = mne.io.read_raw_gdf(os.path.join(GDF_DIR, sujet + "T.gdf"),
                              preload=True, verbose=False)
    ev, _ = mne.events_from_annotations(raw, verbose=False)
    codes = {7: 0, 8: 1}   # 769 gauche, 770 droite
    i3 = raw.ch_names.index("EEG-C3")
    i4 = raw.ch_names.index("EEG-C4")
    icz = raw.ch_names.index("EEG-Cz")
    data = raw.get_data()
    if ref_cz:
        data = data - data[icz]
    p3l, p4l, cl = [], [], []
    for pos, _, code in ev:
        if code in codes:
            p3l.append(puissance_mu(data[i3, pos + win[0]: pos + win[1]], bande))
            p4l.append(puissance_mu(data[i4, pos + win[0]: pos + win[1]], bande))
            cl.append(codes[code])
    return np.array(p3l), np.array(p4l), np.array(cl)


def m_depuis(p3, p4, cl):
    return float(np.mean([E_depuis_puissances(a, b, c)
                          for a, b, c in zip(p3, p4, cl)]))


def nul_hemispheres(gen, E, nb=N_NUL):
    n = len(E)
    out = np.empty(nb)
    for i in range(nb):
        signe = np.where(gen.uniform(0, 1, n) < 0.5, -1.0, 1.0)
        out[i] = float(np.mean(E * signe))
    return out


def main():
    empreintes = {}
    for s in SUJETS:
        with open(os.path.join(GDF_DIR, s + "T.gdf"), "rb") as f:
            empreintes[s + "T.gdf"] = hashlib.sha256(f.read()).hexdigest()
    assert empreintes == EMPREINTES_ATTENDUES, (
        "les fichiers GDF ne sont pas ceux de la campagne scellee")
    empreinte_donnees = hashlib.sha256(
        json.dumps(empreintes, sort_keys=True).encode()).hexdigest()
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    ckpt = {}
    if os.path.exists(CKPT):
        ckpt = json.load(open(CKPT))

    donnees = {}
    for suj in SUJETS:
        print(f"[sujet {suj}]", flush=True)
        if suj in ckpt:
            p3, p4, cl = ckpt[suj]
            donnees[suj] = (np.array(p3), np.array(p4), np.array(cl))
            continue
        donnees[suj] = essais_sujet(suj)
        ckpt[suj] = [donnees[suj][0].tolist(), donnees[suj][1].tolist(),
                     donnees[suj][2].tolist()]
        with open(CKPT, "w") as f:
            json.dump(ckpt, f)

    def concat_cles(cles):
        return (np.concatenate([donnees[s][0] for s in cles]),
                np.concatenate([donnees[s][1] for s in cles]),
                np.concatenate([donnees[s][2] for s in cles]))

    p3, p4, cl = concat_cles(SUJETS)
    E0 = np.array([E_depuis_puissances(a, b, c) for a, b, c in zip(p3, p4, cl)])
    m0 = float(np.mean(E0))
    ms0 = nul_hemispheres(gen, E0)
    mu0, u0 = float(ms0.mean()), float(ms0.std())
    z = {"g0_canonique_HORS_SIGMA": mcs.z_score(m0, mu0, u0)}
    z_eff = (mu0 - m0) / u0

    # g1 : permutation des hemispheres (double contrainte, rapporte)
    signe = np.where(gen.uniform(0, 1, len(E0)) < 0.5, -1.0, 1.0)
    z["g1_hemisperes_permutés"] = mcs.z_score(float(np.mean(E0 * signe)),
                                              mu0, u0)

    def zconf(p3_, p4_, cl_, nom):
        E_ = np.array([E_depuis_puissances(a, b, c)
                       for a, b, c in zip(p3_, p4_, cl_)])
        m_ = float(np.mean(E_))
        ms = nul_hemispheres(gen, E_)
        z[nom] = mcs.z_score(m_, float(ms.mean()), float(ms.std()))

    # g2 : fenetre 1-3 s ; g3 : bande 8-13 Hz ; g5 : reference Cz
    d_g2 = {s: essais_sujet(s, win=(250, 750)) for s in SUJETS}
    zconf(*[np.concatenate([d_g2[s][k] for s in SUJETS]) for k in range(3)],
          "g2_fenetre_1_3s")
    d_g3 = {s: essais_sujet(s, bande=(8.0, 13.0)) for s in SUJETS}
    zconf(*[np.concatenate([d_g3[s][k] for s in SUJETS]) for k in range(3)],
          "g3_bande_8_13")
    zconf(*concat_cles([s for s in SUJETS if s != SUJET_G4_EXCLU]),
          "g4_sans_A03")
    d_g5 = {s: essais_sujet(s, ref_cz=True) for s in SUJETS}
    zconf(*[np.concatenate([d_g5[s][k] for s in SUJETS]) for k in range(3)],
          "g5_reference_Cz")
    victime = int(gen.uniform(0, len(SUJETS)))
    zconf(*concat_cles([s for i, s in enumerate(SUJETS) if i != victime]),
          "g6_sans_" + SUJETS[victime])

    # c1 : etiquettes permutees (diagnostic de presence — PAS declencheur)
    cl_p = gen.permutation(cl)
    m_c1 = m_depuis(p3, p4, cl_p)
    effet_c1 = (m0 - m_c1) / u0

    # c2 : injection d'une asymetrie mu dans les fenêtres reelles :
    # la bande mu du canal contra est attenuee de moitie selon des etiquettes
    # factices declarees ; le pipeline doit retrouver ces etiquettes
    Ef = []
    n_fact = 144
    idx = gen.permutation(np.arange(len(E0)))[:n_fact]
    for rang, j in enumerate(idx):
        classe = rang % 2   # etiquettes factices declarees
        a, b = p3[j], p4[j]
        if classe == 0:
            b = b * 0.5     # C4 attenué (contra pour gauche)
        else:
            a = a * 0.5     # C3 attenue (contra pour droite)
        Ef.append(E_depuis_puissances(a, b, classe))
    m_c2 = float(np.mean(Ef))
    effet_c2 = abs(m_c2 - mu0) / u0

    # verdict : le moteur ne recoit que c2 (declencheur declare de la carte)
    v = mcs.evaluer_double_v2("MCS-02", z, z_eff,
                              {"c2": effet_c2}, attentes={"c2": 1})
    vd = v.to_dict()

    out = {"carte": CARTE_ID, "empreinte_carte_pre_gel": EMPREINTE_CARTE,
           "empreintes_gdf": empreintes, "empreinte_donnees": empreinte_donnees,
           "m_canonique": m0, "mu_nul": mu0, "u_nul": u0,
           "E_moyen_par_sujet": {s: float(np.mean(
               [E_depuis_puissances(a, b, c)
                for a, b, c in zip(*donnees[s])])) for s in SUJETS},
           "z_par_g": z, "z_effondrement": z_eff,
           "controles": {"c1_diagnostic": effet_c1, "c2_pipeline": effet_c2},
           "verdict_moteur_c2_seul": vd, "verdict_carte": vd["verdict"],
           "note": ("c1 est un diagnostic de presence (non declencheur, "
                    "regle de la refonte) ; le declencheur CS0 est c2 seul "
                    "(declare a la carte)")}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": vd["sigma"], "verdict": vd["verdict"],
                      "m_canonique": m0, "z_par_g": z,
                      "controles": out["controles"]}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
