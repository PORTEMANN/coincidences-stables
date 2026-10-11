"""mcs09_runner.py — Ouverture de la carte MCS-09 (jalon 4 v2).

Carte scellee : cartes/v2/MCS-09-titius-bode.md
  sha256 pre-gel : 8f8387ec24b55c2a5525700047438caf4a352718c42199951a2b95d8c063399c
  (empreinte verifiee contre scellement/GEL-MCS09.json apres erratum)
Donnees figees (acquisition a l'ouverture, empreintes au journal) :
  - donnees/mcs09/nssdc_*.html : NASA NSSDC Planetary Fact Sheets
    (pages individuelles : "Semimajor axis (AU)" ; page d'index :
    "Distance from Sun (10^6 km)")
  - donnees/mcs09/sbdb_ceres.json, sbdb_pluto.json : JPL Small-Body
    Database API (full-prec=true)

DEVIATION DECLAREE (consignee au journal) : la carte nomme la contre-source
g1 = "JPL SSD" ; les tables phys_par/Horizons de ssd.jpl.nasa.gov sont
injoignables depuis l'environnement d'execution (timeouts reseau). g1 est
operee par : SBDB (JPL, API fonctionnelle) pour Pluton, et la table d'index
NSSDC (arrondie, 10^6 km) pour les huit planetes ; Ceres garde sa valeur
SBDB aux deux configurations (source unique, declare).

Mesure scellee : m = -log10(RMS(e)), e = (a_obs - a_pred)/a_pred, loi figee
a_n = 0,4 + 0,3*2^n UA (1772, aucun parametre reajuste).
Sigma = min sur {g1..g6} (g0 canonique rapporte hors Sigma, conforme a la
carte — exclure explicite).

Seuil de la carte : 3,2. Le moteur scelle plafonne a DEFAULT 3,0 ; le
runner applique le seuil de la carte et consigne les deux.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import html as htmlmod

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-09"
SEUIL_CARTE = 3.2
EMPREINTE_CARTE = "8f8387ec24b55c2a5525700047438caf4a352718c42199951a2b95d8c063399c"
DATA = os.path.join(RACINE, "donnees", "mcs09")
RESULTATS = os.path.join(RACINE, "resultats", "mcs09_resultats.json")
N_NUL = 10000
AU_KM = 149597870.7          # UA en km (IAU 2012, exacte)
ETENDUE = (0.39, 39.8)       # declaree a la carte

CORPS = ["Mercure", "Venus", "Terre", "Mars", "Ceres",
         "Jupiter", "Saturne", "Uranus", "Neptune", "Pluton"]
A_PRED = np.array([0.4, 0.7, 1.0, 1.6, 2.8, 5.2, 10.0, 19.6, 38.8, 77.2])
PAGES = {"Mercure": "mercury", "Venus": "venus", "Terre": "earth",
         "Mars": "mars", "Jupiter": "jupiter", "Saturne": "saturn",
         "Uranus": "uranus", "Neptune": "neptune", "Pluton": "pluto"}
ORDRE_INDEX = ["mercury", "venus", "earth", "mars", "jupiter",
               "saturn", "uranus", "neptune", "pluto"]  # table d'index NSSDC


def semimajor_page(fichier):
    t = open(fichier, encoding="utf-8", errors="replace").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "|", t)
    t = htmlmod.unescape(re.sub(r"\s+", " ", t))
    m = re.search(r"Semimajor axis \(AU\)\s*\|?\s*([\d.]+)", t)
    return float(m.group(1))


def valeurs_index(fichier):
    t = open(fichier, encoding="utf-8", errors="replace").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "|", t)
    t = htmlmod.unescape(t)
    i = t.index("Distance from Sun")
    j = t.index("km)", i)
    seg = t[j:]
    nums = re.findall(r"\|\s*([\d.]+)\*?\s*(?=\|)", seg)
    vals = [float(x) for x in nums[:10]]
    return vals  # 10 valeurs incl. Lune en position 3 (0,384*)


def a_sbdb(fichier):
    d = json.load(open(fichier))
    return float([e["value"] for e in d["orbit"]["elements"]
                  if e["name"] == "a"][0])


def mesure(a_obs, a_pred):
    e = (np.asarray(a_obs, dtype=float) - a_pred) / a_pred
    return -np.log10(np.sqrt(np.mean(e ** 2)))


def seq_libre(gen, n):
    return np.sort(np.exp(gen.uniform(np.log(ETENDUE[0]),
                                      np.log(ETENDUE[1]), n)))


def z_config(gen, a_obs, a_pred):
    m_val = mesure(a_obs, a_pred)
    n = len(a_obs)
    ms = [mesure(seq_libre(gen, n), a_pred) for _ in range(N_NUL)]
    return m_val, mcs.z_score(m_val, float(np.mean(ms)), float(np.std(ms)))


def main():
    empreintes = {f: hashlib.sha256(
        open(os.path.join(DATA, f), "rb").read()).hexdigest()
        for f in sorted(os.listdir(DATA))}
    empreinte_donnees = hashlib.sha256(
        json.dumps(empreintes, sort_keys=True).encode()).hexdigest()

    # source primaire : pages individuelles NSSDC (UA) + SBDB pour Ceres
    a_prim = {c: semimajor_page(os.path.join(DATA, f"nssdc_{p}.html"))
              for c, p in PAGES.items()}
    a_prim["Ceres"] = a_sbdb(os.path.join(DATA, "sbdb_ceres.json"))
    # contre-source (g1) : index NSSDC (grossier) + SBDB pour Pluton
    idx = valeurs_index(os.path.join(DATA, "nssdc_index.html"))
    idx = [v for i, v in enumerate(idx) if i != 3]   # retrait de la Lune
    a_contre = dict(zip(ORDRE_INDEX, [v / AU_KM * 1e6 for v in idx]))
    a_contre = {c: a_contre[p] for c, p in PAGES.items()}
    a_contre["Pluton"] = a_sbdb(os.path.join(DATA, "sbdb_pluto.json"))
    a_contre["Ceres"] = a_prim["Ceres"]  # source unique, declare

    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    def sel(table, corps):
        return np.array([table[c] for c in corps]), np.array(
            [A_PRED[CORPS.index(c)] for c in corps])

    z = {}
    a0, p0 = sel(a_prim, CORPS)
    m0, z0 = z_config(gen, a0, p0)
    z["g0_canonique_HORS_SIGMA"] = z0
    ms0 = [mesure(seq_libre(gen, 10), A_PRED) for _ in range(N_NUL)]
    u0 = float(np.std(ms0))

    a1, p1 = sel(a_contre, CORPS)
    _, z["g1_contre_source"] = z_config(gen, a1, p1)
    for nom, corps in [("g2_sans_Neptune", [c for c in CORPS if c != "Neptune"]),
                       ("g3_sans_Pluton", [c for c in CORPS if c != "Pluton"]),
                       ("g4_sans_Ceres", [c for c in CORPS if c != "Ceres"]),
                       ("g5_sans_Mercure", [c for c in CORPS if c != "Mercure"])]:
        ag, pg = sel(a_prim, corps)
        _, z[nom] = z_config(gen, ag, pg)
    victime = int(gen.uniform(0, len(CORPS)))
    corps6 = [c for i, c in enumerate(CORPS) if i != victime]
    ag, pg = sel(a_prim, corps6)
    _, z["g6_retrait_" + CORPS[victime]] = z_config(gen, ag, pg)

    # controles positifs (unites du nul canonique)
    effet_c1 = (m0 - mesure(a0, A_PRED * 2)) / u0      # indices decales
    effet_c2 = (m0 - mesure(seq_libre(gen, 10), A_PRED)) / u0

    # diagnostic rapporte (hors Sigma) : cohortes historiques
    connues = CORPS[:4] + CORPS[5:7]         # Mercure..Mars, Jupiter, Saturne
    post = ["Uranus", "Ceres", "Neptune", "Pluton"]
    ac, pc = sel(a_prim, connues)
    ap_, pp = sel(a_prim, post)
    diag = {"m_cohorte_connue_1772": mesure(ac, pc),
            "m_cohorte_post_1772": mesure(ap_, pp)}

    v = mcs.evaluer_v2("DEFAULT", z, {"c1": effet_c1, "c2": effet_c2},
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
           "empreintes_fichiers": empreintes,
           "empreinte_donnees": empreinte_donnees,
           "a_primaire_UA": a_prim, "a_contre_UA": a_contre,
           "ecarts_relatifs_canoniques": {
               c: (a_prim[c] - A_PRED[i]) / A_PRED[i]
               for i, c in enumerate(CORPS)},
           "m_canonique": m0, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "diagnostic_cohortes": diag,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.2": verdict_carte,
           "deviation_declaree": ("g1 : JPL SSD (phys_par/Horizons) "
                                  "injoignable ; substitution SBDB (Pluton) "
                                  "+ index NSSDC arrondi (8 planetes)")}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict_carte": verdict_carte,
                      "z_par_g": z, "controles": out["controles"],
                      "cohortes": diag}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
