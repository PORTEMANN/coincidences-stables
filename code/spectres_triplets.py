"""spectres_triplets.py — Enumeration spectrale des triplets nus verifies.

Filiation T1 (machine des orbites du corpus, reimplementation declaree —
MCS-24 n'utilisait que les comptes ; la campagne E enumere les matrices).
La construction est celle de T1 (src/t1_ko6_taille_impaire.py du depot
noetic-machine-complete, filiation declaree) :
  J0 = permutations signees par blocs (p, q), sigma^2 = id, s_i*s_sigma(i) = +1 ;
  D reel symetrique hors-chiral, entrees {0,+-1}, D != 0, J0 D J0 = -D ;
  contrainte orbite par orbite sur le bloc B (H+ x H-) :
    orbite longueur 1 : libre ssi s_i*s_j = -1 ;
    orbite longueur 2 : libre ssi s_i*s_j*s_i'*s_j' = +1, et alors
    B[i',j'] = -s_i*s_j*B[i,j].
Regression tuante : les comptes par taille doivent reproduire les comptes
publies de MCS-24 (4 / 64 / 880 / 13 696 / 280 944 pour n = 2..6).
"""
from __future__ import annotations

import itertools

import numpy as np

TOL = 1e-9   # fige (filiation KO6-REAL-1.0)
COMPTES_MCS24 = {2: 4, 3: 64, 4: 880, 5: 13696, 6: 280944, 7: 8384512}


def involutions_signees(p, q):
    n = p + q
    res = []
    for perm_p in itertools.permutations(range(p)):
        for perm_q in itertools.permutations(range(p, n)):
            sigma = perm_p + perm_q
            if any(sigma[sigma[i]] != i for i in range(n)):
                continue
            libres = [i for i in range(n) if i <= sigma[i]]
            for bits in itertools.product([1, -1], repeat=len(libres)):
                s = [0] * n
                for i, bt in zip(libres, bits):
                    s[i] = bt
                    s[sigma[i]] = bt
                res.append((sigma, s))
    return res


def orbites_libres(sigma, s, p, q):
    """Orbites libres du bloc B : (representants, signe_relais)."""
    n = p + q
    vu = set()
    libres = []
    for i in range(p):
        for j in range(p, n):
            if (i, j) in vu:
                continue
            i2, j2 = sigma[i], sigma[j]
            if (i2, j2) == (i, j):
                vu.add((i, j))
                if s[i] * s[j] == -1:
                    libres.append(([(i, j)], 1.0))
            else:
                vu.add((i, j))
                vu.add((i2, j2))
                if s[i] * s[j] * s[i2] * s[j2] == +1:
                    libres.append(([(i, j), (i2, j2)], float(-s[i] * s[j])))
    return libres


def blocs_B(p, q):
    """Generateur des blocs B (p x q, entrees {0,+-1}, B != 0) de tous les
    triplets verifies de la signature (p, q)."""
    for sigma, s in involutions_signees(p, q):
        libres = orbites_libres(sigma, s, p, q)
        k = len(libres)
        if k == 0:
            continue
        for vals in itertools.product([1.0, -1.0, 0.0], repeat=k):
            if not any(vals):
                continue
            B = np.zeros((p, q))
            for (reps, rel), v in zip(libres, vals):
                B[reps[0][0], reps[0][1] - p] = v
                if len(reps) == 2:
                    B[reps[1][0], reps[1][1] - p] = rel * v
            yield B


def blocs_B_vect(p, q):
    """Version vectorisee (declaree) : rend un tableau (m, p, q) de blocs
    par involution — meme espace, meme ordre de filiation, SVD batch.
    Utilisee pour n = 7 (8,4 millions de matrices — cout declare)."""
    for sigma, s in involutions_signees(p, q):
        libres = orbites_libres(sigma, s, p, q)
        k = len(libres)
        if k == 0:
            continue
        grille = np.indices((3,) * k).reshape(k, -1).T
        vals = np.choose(grille, [1.0, -1.0, 0.0])
        vals = vals[np.any(vals != 0.0, axis=1)]
        B = np.zeros((len(vals), p, q))
        for l, (reps, rel) in enumerate(libres):
            i, j = reps[0]
            B[:, i, j - p] = vals[:, l]
            if len(reps) == 2:
                i2, j2 = reps[1]
                B[:, i2, j2 - p] = rel * vals[:, l]
        yield B


def rapports_vect(B):
    """Valeurs singulières batch -> rapports r (convention rang 1 : r=1)."""
    sv = np.linalg.svd(B, compute_uv=False)
    smax = sv[:, 0]
    masque = sv > TOL * smax[:, None]
    smin = np.where(masque, sv, np.inf).min(axis=1)
    rang1 = masque.sum(axis=1) <= 1
    r = smax / smin
    r[rang1] = 1.0
    return r


def rapport_spectral(B):
    """r = sigma_max / sigma_min+ (sigma_min+ > TOL*sigma_max) ;
    rang 1 -> r := 1 (convention declaree de la carte)."""
    sv = np.linalg.svd(B, compute_uv=False)
    smax = sv.max()
    sv = sv[sv > TOL * smax]
    if len(sv) <= 1:
        return 1.0
    return float(smax / sv.min())


def spectres_par_taille(n_max, n_min=2, vect=False):
    """{n : (compte, np.array des rapports spectraux)} — enumeration
    exhaustive ; chaque matrice compte une fois (mesure naturelle).
    vect=True : chemin vectorise (n = 7 — declare)."""
    out = {}
    for n in range(n_min, n_max + 1):
        rs = []
        for p in range(1, n):
            if vect:
                for B in blocs_B_vect(p, n - p):
                    rs.append(rapports_vect(B))
            else:
                for B in blocs_B(p, n - p):
                    rs.append(rapport_spectral(B))
        rs = np.concatenate(rs) if rs and isinstance(rs[0], np.ndarray) \
            else np.array(rs)
        out[n] = (len(rs), rs)
    return out


def regression_comptes(spectres):
    """Recoupe les comptes publies de MCS-24 (tuant)."""
    return all(spectres[n][0] == COMPTES_MCS24[n] for n in spectres)
