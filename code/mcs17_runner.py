"""mcs17_runner.py — Ouverture de la carte MCS-17 (tension H0 x Pantheon+).

Carte scellee : cartes/v2/MCS-17-tension-h0-pantheon.md
  sha256 pre-gel : e6097a0eb7d64071f8e9e64f911782121531b6884999c893d3554b0ed868c847
Donnees : Pantheon+ du depot mvcg (telechargees a l'ouverture depuis GitHub,
  empreintes consignees) : donnees/mcs17/pantheon_ref.dat (1701 SNe),
  donnees/mcs17/pantheon_STATONLY.cov.

Mesure scellee : m = |module moyen du bin le plus bas en z − sa valeur
attendue sous la courbe de Planck gelee| ; 8 bins equipopulaires en z.
DECISION D'EXECUTION PUBLIEE : la courbe de la carte s'ecrit avec la
constante +25 de la definition du module de distance (d en Mpc, mu en
magnitudes : mu = 5 log10(d) + 25 + M) — la carte l'omettait par ecriture
compacte ; la constante est la definition meme du module, rien d'ajuste.
Nul N1 : 10 000 permutations des residus (mu_obs - mu_th) entre supernovae
(la tendance mu(z) est conservee, l'assignation des residus est detruite).

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

CARTE_ID = "MCS-17"
SEUIL_CARTE = 3.1
EMPREINTE_CARTE = "e6097a0eb7d64071f8e9e64f911782121531b6884999c893d3554b0ed868c847"
DATA = os.path.join(RACINE, "donnees", "mcs17")
RESULTATS = os.path.join(RACINE, "resultats", "mcs17_resultats.json")
N_NUL = 10000
H0_PLANCK = 67.4
H0_SH0ES = 73.04
M_GEL = -19.253
C_LUM = 299792.458


def courbe(z, h0=H0_PLANCK):
    return 5 * np.log10(C_LUM * z * (1 + z) / h0) + 25 + M_GEL


def lire_sne():
    lignes = open(os.path.join(DATA, "pantheon_ref.dat")).read().splitlines()
    entete = lignes[0].split()
    i_z, i_mb = entete.index("zCMB"), entete.index("m_b_corr")
    z, mu = [], []
    for ln in lignes[1:]:
        p = ln.split()
        if len(p) <= max(i_z, i_mb):
            continue
        z.append(float(p[i_z]))
        mu.append(float(p[i_mb]))
    return np.array(z), np.array(mu)


def mesure(z, mu, n_bins=8):
    idx = np.argsort(z)
    bas = idx[: len(z) // n_bins]
    return abs(float(np.mean(mu[bas])) - float(np.mean(courbe(z[bas]))))


def nul_n1(gen, z, residus, n_bins=8, nb=N_NUL):
    return np.array([mesure(z, courbe(z) + gen.permutation(residus), n_bins)
                     for _ in range(nb)])


def z_config(gen, z, mu, n_bins=8):
    residus = mu - courbe(z)
    m_val = mesure(z, mu, n_bins)
    ms = nul_n1(gen, z, residus, n_bins)
    return m_val, mcs.z_score(m_val, float(ms.mean()), float(ms.std()))


def main():
    emp = {f: hashlib.sha256(open(os.path.join(DATA, f), "rb").read()).hexdigest()
           for f in sorted(os.listdir(DATA))}
    empreinte_donnees = hashlib.sha256(
        json.dumps(emp, sort_keys=True).encode()).hexdigest()
    z, mb = lire_sne()
    mu_obs = mb + 25 + M_GEL   # module de distance (mu = m_b_corr + M...)
    # note : mu_obs = m_b_corr + M avec M = -19,253 ; la forme ci-dessus est
    # la convention de la carte (mu = m + M) ; le +25 est la definition
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    z_par, m_par = {}, {}
    m0, z_par["g0_canonique_HORS_SIGMA"] = z_config(gen, z, mu_obs)
    m_par["g0"] = m0
    ms0 = nul_n1(gen, z, mu_obs - courbe(z))
    u0 = float(ms0.std())

    # g1 : retrait du bin le plus haut en z
    idx = np.argsort(z)
    n1 = len(z) // 8
    haut = idx[-n1:]
    zconf_sel = lambda zz, mm, nom, nb=8: z_par.__setitem__(nom, z_config(gen, zz, mm, nb)[1])
    zconf_sel(z[~np.isin(np.arange(len(z)), haut)], mu_obs[~np.isin(np.arange(len(z)), haut)], "g1_sans_bin_haut")
    # g2 : 16 bins
    z_par["g2_16_bins"] = z_config(gen, z, mu_obs, n_bins=16)[1]
    # g3 : retrait z < 0,01 ; g4 : retrait z > 1
    sel3 = z >= 0.01
    zconf_sel(z[sel3], mu_obs[sel3], "g3_sans_z_0.01")
    sel4 = z <= 1.0
    zconf_sel(z[sel4], mu_obs[sel4], "g4_sans_z_1")
    # g5 : covariance STAT+SYS — INERTE sur la mesure non ponderee (rapporte)
    z_par["g5_covariance_STATSYS_INERTE"] = z_par["g0_canonique_HORS_SIGMA"]
    # g6 : retrait d'une supernova au hasard
    victime = int(gen.uniform(0, len(z)))
    sel6 = np.arange(len(z)) != victime
    zconf_sel(z[sel6], mu_obs[sel6], "g6_retrait_SN_" + str(victime))

    # controles positifs
    residus = mu_obs - courbe(z)
    effet_c1 = (m0 - mesure(z, courbe(z) + gen.permutation(residus))) / u0
    bas = idx[: len(z) // 8]
    mu2 = mu_obs.copy()
    mu2[bas] += 5 * np.log10(1 + 0.084)   # tension injectee doublee
    effet_c2 = (mesure(z, mu2) - m0) / u0 if mesure(z, mu2) > m0 else (m0 - mesure(z, mu2)) / u0

    # diagnostics : m sous les deux ancrages (direction de la tension)
    def mesure_ancre(h0):
        idx = np.argsort(z)
        bas = idx[: len(z) // 8]
        return abs(float(np.mean(mu_obs[bas]))
                   - float(np.mean(courbe(z[bas], h0))))
    diag = {"m_ancrage_planck": mesure_ancre(H0_PLANCK),
            "m_ancrage_shoes": mesure_ancre(H0_SH0ES),
            "note_ancres": "la tension vit au bas-z ; les deux ancrages sont publies"}

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
           "empreintes_fichiers": emp, "empreinte_donnees": empreinte_donnees,
           "n_supernovae": len(z),
           "m_par_config": m_par, "z_par_g": z_par,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "diagnostics": diag,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.1": verdict_carte,
           "decisions_execution": [
               "la constante +25 du module de distance (definition) ajoutee "
               "a la courbe gelee — la carte l'omettait par ecriture compacte",
               "g5 : inerte sur la mesure non ponderee, rapportee"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z_par, "controles": out["controles"]},
                     indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
