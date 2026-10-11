"""mcs15_runner.py — Ouverture de la carte MCS-15 (etalon Zipf, registre).

Carte scellee : cartes/v2/MCS-15-zipf-texte.md
  sha256 pre-gel : 8a718192f90de4f1072bb1e89e8e02934d34a3bd3f8e5d224a319d725c809f85
Donnees (acquisition a l'ouverture, empreintes au journal) :
  - donnees/mcs15/gutenberg_17489.txt (Les Miserables Tome I, FRANCAIS)
  - donnees/mcs15/gutenberg_17493.txt (Les Miserables Tome II, FRANCAIS)
  - donnees/mcs15/gutenberg_98.txt    (A Tale of Two Cities, anglais)

DEVIATION DECLAREE (consignee au journal) : les identifiants de la carte
(#135 Les Miserables, #2610 Notre-Dame de Paris) sont des TRADUCTIONS
ANGLAISES (Hapgood) — non conformes au français declare. Substitution
verifiee au contenu et consignee : l'original français des Miserables
existe en cinq tomes separes ; le canonique est le Tome I (#17489) et g1
le Tome II (#17493), même auteur comme declare a la carte.

Mesure scellee : m = -log10(RMS(eps)), eps(r) = log10(f_obs(r)+1) -
log10(f_zipf(r)+1), f_zipf(r) = f_tot / (H_k . r), k = vocabulaire.
Tokenisation declaree : suite de lettres (accents inclus), casse rabattue
en canonique (g6 : non rabattue), apostrophes coupees.
Nul N1 : 10 000 partitions uniformes (meme tokens, k cases).
Sigma = min sur {g1..g6} (g0 canonique hors Sigma).
Seuil de la carte : 3,0 = seuil DEFAULT du moteur scelle.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import Counter

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
import mcs_score_v2 as mcs  # noqa: E402
import prng_chacha as prng  # noqa: E402

CARTE_ID = "MCS-15"
EMPREINTE_CARTE = "8a718192f90de4f1072bb1e89e8e02934d34a3bd3f8e5d224a319d725c809f85"
DATA = os.path.join(RACINE, "donnees", "mcs15")
RESULTATS = os.path.join(RACINE, "resultats", "mcs15_resultats.json")
N_NUL = 10000
LETTRES = re.compile(r"[a-zàâäáéèêëíîïóôöúùûüÿçœæñ]+", re.IGNORECASE)


def tokens(texte, rabattre=True):
    if rabattre:
        texte = texte.lower()
    return LETTRES.findall(texte)


def loi_rang(k, n_tot, alpha=1.0):
    r = np.arange(1, k + 1)
    return n_tot / (r ** alpha) / np.sum(1.0 / r ** alpha)


def mesure(effectifs, alpha=1.0, renverser=False, kmax=None):
    effectifs = np.sort(np.asarray(effectifs, dtype=float))[::-1]
    if kmax:
        effectifs = effectifs[:kmax]
    k = len(effectifs)
    n_tot = effectifs.sum()
    eff = effectifs[::-1] if renverser else effectifs
    eps = np.log10(eff + 1) - np.log10(loi_rang(k, n_tot, alpha) + 1)
    return -np.log10(np.sqrt(np.mean(eps ** 2)))


def nul_n1(gen, n_tot, k, alpha=1.0, kmax=None, nb=N_NUL):
    out = np.empty(nb)
    for i in range(nb):
        part = gen.uniform(0, 1, k)
        part = np.floor(part / part.sum() * n_tot).astype(int)
        out[i] = mesure(part, alpha, kmax=kmax)
    return out


def frequences(texte, rabattre=True):
    return np.array(sorted(Counter(tokens(texte, rabattre)).values(),
                         reverse=True))


def z_config(gen, eff, alpha=1.0, kmax=None):
    m_val = mesure(eff, alpha, kmax=kmax)
    k = min(len(eff), kmax) if kmax else len(eff)
    n = np.sort(eff)[::-1][:k].sum()
    ms = nul_n1(gen, n, k, alpha, kmax)
    return m_val, mcs.z_score(m_val, float(ms.mean()), float(ms.std()))


def alpha_ajuste(eff):
    eff = np.sort(eff)[::-1]
    sel = eff > 0
    r = np.arange(1, len(eff) + 1)[sel]
    A = np.vstack([np.log10(r), np.ones(sel.sum())]).T
    pente, _ = np.linalg.lstsq(A, np.log10(eff[sel]), rcond=None)[0]
    return float(-pente)


def main():
    brut = {}
    for f in os.listdir(DATA):
        with open(os.path.join(DATA, f), "rb") as fh:
            brut[f] = fh.read()
    empreintes = {f: hashlib.sha256(b).hexdigest() for f, b in brut.items()}
    empreinte_donnees = hashlib.sha256(
        json.dumps(empreintes, sort_keys=True).encode()).hexdigest()
    t1 = brut["gutenberg_17489.txt"].decode("utf-8", errors="replace")
    t2 = brut["gutenberg_17493.txt"].decode("utf-8", errors="replace")
    t3 = brut["gutenberg_98.txt"].decode("utf-8", errors="replace")

    gen = prng.PRNGChaCha(hashlib.sha256(
        ("MCS-J4V2|" + EMPREINTE_CARTE + "|" + empreinte_donnees).encode()).digest())

    eff0 = frequences(t1)
    z, m_par = {}, {}
    m0, z["g0_canonique_HORS_SIGMA"] = z_config(gen, eff0)
    m_par["g0_canonique_HORS_SIGMA"] = m0
    u0 = float(nul_n1(gen, eff0.sum(), len(eff0), nb=2000).std())

    _, z["g1_tome_II"] = z_config(gen, frequences(t2))
    _, z["g2_dickens_anglais"] = z_config(gen, frequences(t3))
    _, z["g3_sans_top10"] = z_config(gen, np.sort(eff0)[::-1][10:])
    _, z["g4_fenetre_1000"] = z_config(gen, eff0, kmax=1000)
    _, z["g5_alpha_1.1"] = z_config(gen, eff0, alpha=1.1)
    _, z["g6_casse_non_rabattue"] = z_config(gen, frequences(t1, rabattre=False))

    # controles positifs (unites du nul canonique)
    effet_c1 = (m0 - mesure(eff0, renverser=True)) / u0
    part = gen.uniform(0, 1, len(eff0))
    part = np.floor(part / part.sum() * eff0.sum()).astype(int)
    effet_c2 = (m0 - mesure(part)) / u0

    # diagnostics
    top20 = Counter(tokens(t1)).most_common(20)
    diag = {"alpha_tome_I": alpha_ajuste(eff0),
            "alpha_tome_II": alpha_ajuste(frequences(t2)),
            "alpha_dickens": alpha_ajuste(frequences(t3)),
            "vocabulaire_tome_I": len(eff0),
            "tokens_tome_I": int(eff0.sum()),
            "top20": top20}

    v = mcs.evaluer_v2("DEFAULT", z, {"c1": effet_c1, "c2": effet_c2},
                       attentes={"c1": 1, "c2": 1},
                       exclure=("g0_canonique_HORS_SIGMA",))
    vd = v.to_dict()
    s = vd["sigma"]

    out = {"carte": CARTE_ID, "empreinte_carte_pre_gel": EMPREINTE_CARTE,
           "empreintes_fichiers": empreintes,
           "empreinte_donnees": empreinte_donnees,
           "m_par_config": m_par, "z_par_g": z,
           "controles": {"c1": effet_c1, "c2": effet_c2},
           "diagnostics": diag,
           "verdict_moteur_seuil_3.0": vd,
           "verdict_carte_seuil_3.0": vd["verdict"],
           "deviation_declaree": ("#135 et #2610 de la carte sont des "
                                  "traductions anglaises ; substitution par "
                                  "les originaux français Tome I (#17489) et "
                                  "Tome II (#17493), verifies au contenu")}
    with open(RESULTATS, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sigma": s, "verdict": vd["verdict"],
                      "z_par_g": z, "controles": out["controles"],
                      "diagnostics": {k: v_ for k, v_ in diag.items()
                                      if k != "top20"}}, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
