"""mcs08_runner.py — Ouverture de la carte MCS-08 (jalon 4 v2, calibration).

Carte scellee : cartes/v2/MCS-08-benford-codata.md
  sha256 pre-gel : ed656aa4e013bc7af8f1238314c4308cda70e4b226b9bae93f67ae485562d795
Donnees figees (acquisition a l'ouverture, empreintes au journal) :
  - donnees/mcs08_allascii_2022.txt  (NIST, CODATA 2022, "Complete Listing")
  - donnees/mcs08_allascii_2018.txt  (NIST, archive CODATA 2018, g1)

Mesure scellee : m = -L1(p_obs, p_Ben) sur les premiers chiffres
significatifs des |valeurs| ; p_Ben(d) = log_b(1+1/d), base 10 (base 12 en g4).
Nul N1 : loi plate sur le meme alphabet de chiffres et le meme effectif.

Decisions d'execution publiees (carte scellee, rien de re-ajuste) :
- g2 : le critere operatoire de "constante de definition exacte ou grandeur
  qui en decoule" est la mention "(exact)" de la colonne incertitude — les
  sept constantes de definition du SI 2019 (c, h, e, k, N_A, K_cd,
  Delta_nu_Cs) sont nommees ici comme semantique declaree de la deformation ;
  la mention "(exact)" est le critere mecanique.
- g3 : facteur exact J -> eV (1 / 1.602176634e-19) applique a toutes les
  valeurs (changement d'echelle non decimal).
- g5 : rangs pairs dans l'ordre de la table (0, 2, 4, ...).
- g6 : retrait d'une entree tiree par le PRNG public ChaCha20
  (cle = SHA-256("MCS-J4V2|" + empreinte_carte + "|" + empreinte_donnees)).

Seuil de la carte : 3,0 = seuil DEFAULT du moteur scelle (aucun ecart).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-08"
EMPREINTE_CARTE = "ed656aa4e013bc7af8f1238314c4308cda70e4b226b9bae93f67ae485562d795"
F2022 = os.path.join(RACINE, "donnees", "mcs08_allascii_2022.txt")
F2018 = os.path.join(RACINE, "donnees", "mcs08_allascii_2018.txt")
RESULTATS = os.path.join(RACINE, "resultats", "mcs08_resultats.json")
N_NUL = 10000
FACTEUR_EV = 1.0 / 1.602176634e-19

VAL_RE = re.compile(
    r"^(.{60})\s*(-?[\d][\d\s.]*?\d(?:\.\.\.)?(?:\s*e[+-]?\d+)?)"
    r"\s{2,}(\(exact\)|\S.*?)\s{2,}(.*)$")


def lire_table(chemin):
    out = []
    with open(chemin, encoding="latin-1") as f:
        for ln in f.read().splitlines():
            m = VAL_RE.match(ln)
            if not m:
                continue
            v = float(m.group(2).replace("...", "").replace(" ", ""))
            out.append({"nom": m.group(1).strip(), "valeur": v,
                        "exacte": m.group(3).strip() == "(exact)"})
    return out


def premier_chiffre(valeurs, base=10):
    v = np.abs(np.asarray(valeurs, dtype=float))
    v = v[v > 0]
    d = np.floor(v / base ** np.floor(np.log(v) / np.log(base)))
    return d.astype(int)


def p_ben(base=10):
    d = np.arange(1, base)
    return np.log(1 + 1 / d) / np.log(base)


def mesure(chiffres, base=10):
    pb = p_ben(base)
    p_obs = np.array([np.mean(chiffres == d) for d in range(1, base)])
    return -float(np.sum(np.abs(p_obs - pb)))


def nul_n1(gen, n, base=10, nb=N_NUL):
    return np.array([mesure(gen.uniform(1, base, n).astype(int), base)
                     for _ in range(nb)])


def z_config(gen, valeurs, base=10):
    ch = premier_chiffre(valeurs, base)
    m_val = mesure(ch, base)
    ms = nul_n1(gen, len(ch), base)
    return m_val, mcs.z_score(m_val, float(np.mean(ms)), float(np.std(ms)))


def main():
    b22 = open(F2022, "rb").read()
    b18 = open(F2018, "rb").read()
    emp = {"allascii_2022.txt": hashlib.sha256(b22).hexdigest(),
           "allascii_2018.txt": hashlib.sha256(b18).hexdigest()}
    empreinte_donnees = hashlib.sha256(b22 + b18).hexdigest()
    t22, t18 = lire_table(F2022), lire_table(F2018)
    vals = [e["valeur"] for e in t22]
    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    z, m_par_config = {}, {}
    m0, z["g0_canonique"] = z_config(gen, vals)
    m_par_config["g0_canonique"] = m0
    _, z["g1_codata2018"] = z_config(gen, [e["valeur"] for e in t18])
    _, z["g2_sans_exactes"] = z_config(gen, [e["valeur"] for e in t22
                                             if not e["exacte"]])
    _, z["g3_echelle_eV"] = z_config(gen, [v * FACTEUR_EV for v in vals])
    _, z["g4_base12"] = z_config(gen, vals, base=12)
    _, z["g5_rangs_pairs"] = z_config(gen, vals[::2])
    victime = int(gen.uniform(0, len(vals)))
    _, z["g6_retrait_" + str(victime)] = z_config(
        gen, [v for i, v in enumerate(vals) if i != victime])

    # nul canonique (pour les unites des controles)
    ch0 = premier_chiffre(vals)
    ms0 = nul_n1(gen, len(ch0))
    u0 = float(np.std(ms0))
    # c1 : decalage cyclique ; c2 : mantisses plates declarees
    effet_c1 = (m0 - mesure(ch0 % 9 + 1)) / u0
    effet_c2 = (m0 - mesure(gen.uniform(1, 10, len(ch0)).astype(int))) / u0

    v = mcs.evaluer_v2("DEFAULT", z, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1})
    vd = v.to_dict()

    out = {"carte": CARTE_ID, "empreinte_carte_pre_gel": EMPREINTE_CARTE,
           "empreintes_donnees": emp, "empreinte_donnees_combinee": empreinte_donnees,
           "n_entrees_2022": len(t22), "n_exactes_2022": sum(e["exacte"] for e in t22),
           "n_entrees_2018": len(t18),
           "p_obs_canonique": {str(d): float(np.mean(ch0 == d)) for d in range(1, 10)},
           "m_canonique": m0, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "verdict": vd,
           "decisions_execution": [
               "g2 : critere mecanique = mention '(exact)' de la table",
               "g3 : facteur exact J->eV applique a toutes les valeurs",
               "g5 : rangs pairs dans l'ordre de la table"]}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": vd["sigma"], "verdict": vd["verdict"],
                      "z_par_g": z, "controles": out["controles"]},
                     indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
