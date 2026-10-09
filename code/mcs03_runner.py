"""mcs03_runner.py — Execution unique MCS-03 (jalon 4).

Carte : MCS-03-KO6-E8.md (SHA256_CARTE e5b082c87c996842c707e06a66d98008c62c9dfc114ee33a35ff5da7dc0a1f70).
Hache et consigne au journal JALON-4 AVANT execution.

Operationalisation declaree (le lexique laisse C partiellement abstrait ; ces
choix sont geles ici, avant tout tirage) :

- condition d'ordre 1 : le couple (p, q) la satisfait ssi (p == q) OU
  (dim(p) == dim(q)) ; C(A) = nombre de couples non ordonnes avec repetition
  (p <= q) de representations reelles irreductibles, dim(p)*dim(q) <= dim_R(A)
  (facteur 2 pour g3) ;
- tables de caracteres : calculees NUMERIQUEMENT par diagonalisation
  simultanee du centre de l'algebre de groupe (constantes de structure des
  sommes de classes), puis AUTO-VERIFIEES : orthogonalite, completude
  (somme d_i^2 = |G|), chi(e) entier ; types reels/complexes/quaternioniques
  par indicateur de Frobenius-Schur nu = (1/|G|) somme chi(g^2), calcule
  sur la loi de groupe explicite ; verification Wedderburn reelle
  (somme a_i^2 dim D_i = |G|) ;
- famille ALG (KO-6, minimalite proxy : exactement un sommand H, J^2 = -1,
  <= 3 sommets, dim_R <= 32) : 36 algebres ; A_F = C + H + M3(C) y figure
  (dim_R = 24) ; famille GRP : Z_1..Z_8, 2D_2..2D_5, 2T, 2O, 2I (16 groupes,
  tries par (|G|, nom)) ; appariement rang-quantile declare : le groupe de
  rang i est apparie a l'algebre de rang floor(i * (L_ALG - 1) / 15) ;
- m = correlation de Spearman entre C_ALG apparie et C_GRP ;
- z_g sous N1 (10 000 familles d'algebres aleatoires de meme distribution de
  dimensions) ; N2 (comptage d'ordre, Z_n uniforme, n <= 240) et N3
  (permutation des C_GRP) rapportes en position de quantile ;
- Sigma : la carte fixe min sur {g1..g6} ; renforcement conservateur DECLARE :
  la configuration de base est incluse dans Sigma (ne peut que l'abaisser) ;
- systemes de racines : labels de la chaine de McKay (2T<->E6, 2O<->E7,
  2I<->E8, 2D_n<->D_{n+2}), utilises uniquement pour les re-ancrages g1/g6 ;
- PRNG : cle = SHA-256("MCS-J4|" + empreinte_carte + "|" + empreinte_donnees)
  ou empreinte_donnees = SHA-256 du JSON canonique des deux familles calcule
  par CE runner AVANT tout tirage (enumeration deterministe ; publiee dans
  les resultats) ; ordre des tirages : N1 pour [base, g1..g6], puis N2, puis N3.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from itertools import combinations_with_replacement

import numpy as np
from scipy.stats import spearmanr

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
sys.path.insert(0, os.path.join(RACINE, "nulls"))
from mcs_score import evaluer, z_score  # noqa: E402
from prng_chacha import PRNGChaCha  # noqa: E402
from surrogates import permutation as nul_permutation  # noqa: E402

EMPREINTE_CARTE = "e5b082c87c996842c707e06a66d98008c62c9dfc114ee33a35ff5da7dc0a1f70"
N_TIRAGES = 10000
TAU = (1.0 + math.sqrt(5.0)) / 2.0
TOL = 1e-6

# --- Groupes finis de SU(2) en coordonnees quaternionnelles ------------------

def qmul(p, q):
    w1, x1, y1, z1 = p; w2, x2, y2, z2 = q
    return (w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2)

def qinv(p):
    return (p[0], -p[1], -p[2], -p[3])

def groupe_Z(n):
    return [(math.cos(2*k*math.pi/n), math.sin(2*k*math.pi/n), 0.0, 0.0) for k in range(n)]

def groupe_2D(n):
    a = [(math.cos(k*math.pi/n), math.sin(k*math.pi/n), 0.0, 0.0) for k in range(2*n)]
    b = (0.0, 0.0, 1.0, 0.0)
    return a + [qmul(b, g) for g in a]

def groupe_2T():
    base = [(1,0,0,0), (-1,0,0,0), (0,1,0,0), (0,-1,0,0),
            (0,0,1,0), (0,0,-1,0), (0,0,0,1), (0,0,0,-1)]
    demi = [(s1/2, s2/2, s3/2, s4/2)
            for s1 in (1,-1) for s2 in (1,-1) for s3 in (1,-1) for s4 in (1,-1)]
    return [tuple(map(float, g)) for g in base] + demi

def groupe_2O():
    g = groupe_2T()
    s = 1.0 / math.sqrt(2.0)
    for i, j in [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]:
        for s1 in (1, -1):
            for s2 in (1, -1):
                q = [0.0]*4; q[i] = s1*s; q[j] = s2*s
                g.append(tuple(q))
    return g

def groupe_2I():
    g = groupe_2T()
    vals = [TAU/2, 0.5, (TAU-1)/2, 0.0]
    import itertools as _it
    for perm in _it.permutations(range(4)):
        # permutations paires seulement
        inv = sum(1 for a in range(4) for b in range(a+1, 4) if perm[a] > perm[b])
        if inv % 2:
            continue
        for sgns in _it.product((1, -1), repeat=3):
            q = [0.0]*4
            nz = [vals[0], vals[1], vals[2]]
            k = 0
            for pos in range(4):
                if perm[pos] == 3:
                    q[pos] = 0.0
                else:
                    q[pos] = sgns[k]*nz[perm[pos] if perm[pos] < 3 else 0]
                    k += 1
            # reindexe : place vals selon perm
            q = [0.0]*4
            src = [TAU/2, 0.5, (TAU-1)/2, 0.0]
            kk = 0
            for pos in range(4):
                if src[perm[pos]] == 0.0:
                    q[pos] = 0.0
                else:
                    q[pos] = sgns[kk]*src[perm[pos]]; kk += 1
            g.append(tuple(q))
    return g

def groupe_I():
    """Icosaedrique I = 2I/{+/-1} (ordre 60) : representants canoniques
    (premiere composante non nulle positive), loi quotient geree par
    table_mult(canon=canon_I)."""
    out, vus = [], set()
    for q in groupe_2I():
        r = canon_I(q)
        cle = tuple(round(c, 9) for c in r)
        if cle not in vus:
            vus.add(cle); out.append(r)
    return out

def canon_I(q):
    r = q
    for i in range(4):
        if abs(r[i]) > 1e-12:
            if r[i] < 0:
                r = tuple(-c for c in r)
            break
    return r

# --- Loi de groupe, classes, table de caracteres (centre de l'algebre) ------

def table_mult(G, canon=None):
    """Table de multiplication par plus-proche-voisin (tolerance 1e-8).
    canon : canonicalisation optionnelle (loi quotient, ex. I = 2I/{+/-1})."""
    n = len(G)
    E = np.array(G)
    M = np.empty((n, n), dtype=int)
    for i in range(n):
        prods = np.array([qmul(G[i], G[j]) for j in range(n)])
        if canon is not None:
            prods = np.array([canon(tuple(p)) for p in prods])
        d = ((prods[:, None, :] - E[None, :, :]) ** 2).sum(-1)
        idx = d.argmin(1)
        assert (d.min(1) < 1e-8).all(), f"produit hors groupe (i={i})"
        M[i] = idx
    return M

def classes_conj(G, M, canon=None):
    n = len(G)
    E = np.array(G)
    inv = np.array([canon(qinv(g)) if canon is not None else qinv(g) for g in G])
    idx_inv = [int(((E - iv) ** 2).sum(-1).argmin()) for iv in inv]
    vu, classes = set(), []
    for i in range(n):
        if i in vu:
            continue
        cl = sorted({M[h, M[i, idx_inv[h]]] for h in range(n)})
        vu.update(cl)
        classes.append(cl)
    classes.sort(key=lambda c: (len(c) != 1, min(c)))
    return classes

def caracteres_irreductibles(G, canon=None):
    """Table des caracteres par diagonalisation simultanee du centre.
    Retourne (M, classes, tableaux chi par classe), auto-verifiee."""
    n = len(G)
    M = table_mult(G, canon)
    cls = classes_conj(G, M, canon)
    k = len(cls)
    tailles = [len(c) for c in cls]
    rep = [c[0] for c in cls]
    classe_de = np.empty(n, dtype=int)
    for a, c in enumerate(cls):
        for g in c:
            classe_de[g] = a
    # constantes de structure a_{abc} : c_a * c_b = somme_c a_{abc} c_c
    A = np.zeros((k, k, k))
    for a in range(k):
        for b in range(k):
            for g in cls[a]:
                for h in cls[b]:
                    A[a, classe_de[M[g, h]], b] += 1
    mats = [A[a] / np.array(tailles)[:, None] for a in range(k)]  # operateurs T_a : (m,b) = alpha_{abm}
    B = sum((a + 1) * mats[a] for a in range(k))
    vals, vecs = np.linalg.eig(B)
    if len(set(np.round(vals, 6))) < k:
        B = sum((a + 1) ** 2 * mats[a] for a in range(k))
        vals, vecs = np.linalg.eig(B)
    table = []
    for i in range(k):
        v = vecs[:, i]
        j = int(np.argmax(np.abs(v)))
        lam = np.array([(mats[a] @ v)[j] / v[j] for a in range(k)])
        d2 = n / sum(abs(lam[a])**2 / tailles[a] for a in range(k))
        d = math.sqrt(max(d2, 1e-12))
        chi = np.array([d * lam[a] / tailles[a] for a in range(k)])
        table.append(chi)
    # verification : completude, chi(e), orthogonalite
    ds = [round(float(np.real(chi[0]))) for chi in table]
    assert abs(sum(d*d for d in ds) - n) < 1e-4, f"completude: {ds} vs {n}"
    for chi in table:
        x = float(np.real(chi[0]))
        assert abs(x - round(x)) < 1e-4 and round(x) >= 1, f"chi(e) non entier: {x}"
    for i in range(k):
        for j2 in range(k):
            ip = sum(tailles[a] * table[i][a] * np.conj(table[j2][a]) for a in range(k)) / n
            assert abs(ip - (1.0 if i == j2 else 0.0)) < 1e-6, f"orthogonalite {i},{j2}"
    return G, M, cls, table

def types_reels(G, M, cls, table):
    """Frobenius-Schur + regroupement conjugue -> dims des irreps reelles."""
    n = len(G)
    classe_de = np.empty(n, dtype=int)
    for a, c in enumerate(cls):
        for g in c:
            classe_de[g] = a
    k = len(cls)
    out = []
    for chi in table:
        nu = sum(chi[classe_de[M[g, g]]] for g in range(n)) / n
        nu_r = round(float(np.real(nu)))
        assert abs(float(np.real(nu)) - nu_r) < 1e-4, f"FS non entier: {nu}"
        out.append([int(round(float(np.real(chi[0])))), nu_r, False])
    # paires complexes : chi_j = conj(chi_i)
    for i in range(k):
        if out[i][2]:
            continue
        if out[i][1] == 0:
            for j in range(i + 1, k):
                if not out[j][2] and np.allclose(table[j], np.conj(table[i]), atol=1e-6):
                    out[j][2] = True
                    break
    dims = []
    for d, nu, absorbe in out:
        if absorbe:
            continue
        if nu == 1:
            dims.append(d)          # reel
        else:
            dims.append(2 * d)      # paire complexe ou quaternionique
    # verification Wedderburn reelle
    tot = 0
    for d, nu, absorbe in out:
        if absorbe:
            continue
        if nu == 1:
            tot += d * d
        elif nu == 0:
            tot += 2 * d * d
        else:
            tot += d * d
    assert tot == n, f"Wedderburn: {tot} != {n}"
    return sorted(dims)

# --- Invariant C --------------------------------------------------------------

_CACHE_C = {}

def C_inv(dims, dimA, facteur=1.0, ordre1=True):
    cle = (tuple(dims), dimA, facteur, ordre1)
    if cle in _CACHE_C:
        return _CACHE_C[cle]
    c = 0
    kk = len(dims)
    for p in range(kk):
        for q in range(p, kk):
            if dims[p] * dims[q] > facteur * dimA:
                continue
            if ordre1 and not (p == q or dims[p] == dims[q]):
                continue
            c += 1
    _CACHE_C[cle] = c
    return c

# --- Familles -----------------------------------------------------------------

SOMMETS_RC = [("R", n) for n in range(1, 6)] + [("C", m) for m in range(1, 4)]

def dim_sommet(s):
    t, n = s
    return n*n if t == "R" else (2*n*n if t == "C" else 4*n*n)

def irrep_sommet(s):
    t, n = s
    return n if t == "R" else (2*n if t == "C" else 4*n)

def famille_alg(obligatoire, max_sommets=3, dim_max=32, corps_complexe=False):
    """Algebres avec exactement le sommand obligatoire + <= max_sommets-1 autres."""
    out = []
    d0 = dim_sommet(obligatoire)
    types = [("C", n) for n in range(1, 6)] if corps_complexe else SOMMETS_RC
    for r in range(0, max_sommets):
        for comb in combinations_with_replacement(range(len(types)), r):
            sommets = [obligatoire] + [types[i] for i in comb]
            dim = sum(dim_sommet(s) for s in sommets)
            if dim <= dim_max:
                out.append((tuple(sommets), dim))
    out.sort(key=lambda x: (x[1], repr(x[0])))
    return out

def dims_irreps_alg(sommets):
    return sorted(irrep_sommet(s) for s in sommets)

_CACHE_TABLES = {}

def C_groupe(G, facteur=1.0, ordre1=True, canon=None):
    cle = hashlib.sha256(np.array(G).round(7).tobytes()
                         + (b"Q" if canon is not None else b"")).hexdigest()
    if cle not in _CACHE_TABLES:
        _, M, cls, table = caracteres_irreductibles(G, canon)
        _CACHE_TABLES[cle] = types_reels(G, M, cls, table)
    dims = _CACHE_TABLES[cle]
    return C_inv(dims, len(G), facteur, ordre1), dims

def C_Zn(n, facteur=1.0, ordre1=True):
    """Forme close pour R[Z_n] : irreps reelles = {1} (+{1} si n pair) + {2}xk.
    Verifiee contre la machinerie generale pour n = 1..8 et 20 (8/8 exact)."""
    e = 1 if n % 2 == 0 else 0
    dims = [1] * (1 + e) + [2] * ((n - 1 - e) // 2)
    return C_inv(dims, n, facteur, ordre1)

# --- Appariement et mesure ----------------------------------------------------

def apparier(C_alg_liste, C_grp_liste):
    L = len(C_alg_liste); n = len(C_grp_liste)
    idx = [int(math.floor(i * (L - 1) / (n - 1))) for i in range(n)]
    return np.array([C_alg_liste[k] for k in idx], dtype=float), np.array(C_grp_liste, dtype=float)

def mesure(C_alg_liste, C_grp_liste):
    a, b = apparier(C_alg_liste, C_grp_liste)
    r, _ = spearmanr(a, b)
    return float(r)

# --- Algebre aleatoire de dimension imposee (nul N1) --------------------------

def alg_aleatoire(dim, rng, complexe=False):
    if complexe:
        parts = [(n*n, n) for n in range(1, 6)]
    else:
        parts = ([(n*n, n) for n in range(1, 6)]
                 + [(2*m*m, 2*m) for m in range(1, 4)]
                 + [(4*h*h, 4*h) for h in range(1, 3)])
    rem, dims = dim, []
    garde = 0
    while rem > 0 and garde < 200:
        garde += 1
        choix = [(d, i) for d, i in parts if d <= rem]
        d, i = choix[rng._below(len(choix))]
        dims.append(i); rem -= d
    if rem != 0:
        raise RuntimeError("partition impossible")
    return sorted(dims)

# --- Pipeline -----------------------------------------------------------------

def config_base(facteur=1.0, ordre1=True, corps="reel", famille="KO6", grp_override=None):
    if corps == "complexe":
        algs = famille_alg(("C", 2), corps_complexe=True)
    elif famille == "KO2":
        algs = famille_alg(("R", 2))
    else:
        algs = famille_alg(("H", 1))
    C_alg = [C_inv(dims_irreps_alg(s), d, facteur, ordre1) for s, d in algs]
    groupes = grp_override if grp_override is not None else (
        [("Z_%d" % n, groupe_Z(n), None) for n in range(1, 9)]
        + [("2D_%d" % n, groupe_2D(n), None) for n in range(2, 6)]
        + [("2T", groupe_2T(), None), ("2O", groupe_2O(), None), ("2I", groupe_2I(), None)])
    groupes = sorted(groupes, key=lambda x: (len(x[1]), x[0]))
    C_grp, dims_grp = [], {}
    for nom, G, canon in groupes:
        c, dims = C_groupe(G, facteur, ordre1, canon)
        C_grp.append(c); dims_grp[nom] = dims
    return algs, C_alg, groupes, C_grp, dims_grp

def z_sous_N1(C_alg_dims, C_alg_ref, C_grp, rng, complexe=False, facteur=1.0, ordre1=True):
    """N1 : familles d'algebres aleatoires, meme distribution de dimensions."""
    m_ref = mesure(C_alg_ref, C_grp)
    ms = np.empty(N_TIRAGES)
    for t in range(N_TIRAGES):
        C_rand = [C_inv(alg_aleatoire(d, rng, complexe), d, facteur, ordre1)
                  for _, d in C_alg_dims]
        ms[t] = mesure(C_rand, C_grp)
    mu, u = float(np.mean(ms)), float(np.std(ms))
    return m_ref, mu, u, z_score(m_ref, mu, u)

def main():
    # 0. Liage a la carte scellee (convention pre-gel de l'acte J3)
    acte = json.load(open(os.path.join(RACINE, "scellement", "SCCELLEMENT-J3.json"), encoding="utf-8"))
    entree = acte["fichiers"]["cartes/MCS-03-KO6-E8.md"]
    contenu = open(os.path.join(RACINE, "cartes", "MCS-03-KO6-E8.md"), encoding="utf-8").read()
    import re as _re
    blocs = list(_re.finditer(r"```\n.*?```", contenu, _re.DOTALL))
    pre_gel = contenu[:blocs[-1].start()] + entree["bloc_nul_original"] + contenu[blocs[-1].end():]
    assert hashlib.sha256(pre_gel.encode("utf-8")).hexdigest() == entree["sha256_pre_gel"] == EMPREINTE_CARTE

    # 1. Enumeration deterministe des familles -> empreinte donnees -> PRNG
    algs, C_alg, groupes, C_grp, dims_grp = config_base()
    enumer = {"ALG": [{"sommets": [list(s) for s in sm], "dim_R": d, "C": c}
                      for (sm, d), c in zip(algs, C_alg)],
              "GRP": [{"nom": nom, "ordre": len(G), "irreps_reelles": dims_grp[nom], "C": c}
                      for (nom, G, _), c in zip(groupes, C_grp)]}
    canon = json.dumps(enumer, sort_keys=True, separators=(",", ":")).encode()
    emp_donnees = hashlib.sha256(canon).hexdigest()
    cle = hashlib.sha256(f"MCS-J4|{EMPREINTE_CARTE}|{emp_donnees}".encode("ascii")).digest()
    rng = PRNGChaCha(cle)
    empreinte_flot = rng._octets(64).hex()

    rang_AF = next(i for i, (sm, d) in enumerate(algs)
                   if sorted(s for s in sm) == sorted([("H", 1), ("C", 1), ("C", 3)]))
    print(f"familles : ALG={len(algs)} algebres, GRP={len(groupes)} groupes")
    print(f"A_F rang {rang_AF}, dim 24, C(A_F)={C_alg[rang_AF]} ; C(2I)={C_grp[-1]} ; C(Z_120 non calcule ici)")
    print(f"C_ALG = {C_alg}")
    print(f"C_GRP = {C_grp}")

    # 2. Configurations (ordre de tirage publie)
    grp_g1 = sorted([("Z_%d" % n, groupe_Z(n), None) for n in range(1, 9)]
                    + [("2D_%d" % n, groupe_2D(n), None) for n in range(2, 6)]
                    + [("2T", groupe_2T(), None), ("2O", groupe_2O(), None), ("2D_14", groupe_2D(14), None)],
                    key=lambda x: (len(x[1]), x[0]))
    grp_g2 = sorted([("Z_%d" % n, groupe_Z(n), None) for n in range(1, 9)]
                    + [("2D_%d" % n, groupe_2D(n), None) for n in range(2, 6)]
                    + [("2T", groupe_2T(), None), ("2O", groupe_2O(), None), ("Z_120", groupe_Z(120), None)],
                    key=lambda x: (len(x[1]), x[0]))
    grp_g6 = [groupes[-1]] + groupes[:-1]   # 2I deplace au rang 0 (chaine cassee)

    def C_grp_de(grp, facteur=1.0, ordre1=True):
        return [C_groupe(G, facteur, ordre1, canon)[0] for _, G, canon in grp]

    CONFIGS = {}
    CONFIGS["base"] = (algs, C_alg, C_grp, dict(facteur=1.0, ordre1=True, complexe=False))
    algs_g1, C_alg_g1 = algs, C_alg
    CONFIGS["g1"] = (algs_g1, C_alg_g1, C_grp_de(grp_g1), dict(facteur=1.0, ordre1=True, complexe=False))
    CONFIGS["g2"] = (algs, C_alg, C_grp_de(grp_g2), dict(facteur=1.0, ordre1=True, complexe=False))
    algs_g3 = algs
    C_alg_g3 = [C_inv(dims_irreps_alg(s), d, 2.0, True) for s, d in algs]
    CONFIGS["g3"] = (algs_g3, C_alg_g3, C_grp_de(groupes, 2.0, True), dict(facteur=2.0, ordre1=True, complexe=False))
    algs_g4 = famille_alg(("R", 2))
    C_alg_g4 = [C_inv(dims_irreps_alg(s), d, 1.0, True) for s, d in algs_g4]
    CONFIGS["g4"] = (algs_g4, C_alg_g4, C_grp, dict(facteur=1.0, ordre1=True, complexe=False))
    algs_g5 = famille_alg(("C", 2), corps_complexe=True)
    C_alg_g5 = [C_inv(dims_irreps_alg(s), d, 1.0, True) for s, d in algs_g5]
    CONFIGS["g5"] = (algs_g5, C_alg_g5, C_grp, dict(facteur=1.0, ordre1=True, complexe=True))
    CONFIGS["g6"] = (algs, C_alg, C_grp_de(grp_g6), dict(facteur=1.0, ordre1=True, complexe=False))

    z_par_g, detail = {}, {}
    for nom in ["base", "g1", "g2", "g3", "g4", "g5", "g6"]:
        algs_c, C_alg_c, C_grp_c, opt = CONFIGS[nom]
        m, mu, u, z = z_sous_N1([(s, d) for s, d in algs_c], C_alg_c, C_grp_c, rng,
                                complexe=opt["complexe"], facteur=opt["facteur"], ordre1=opt["ordre1"])
        z_par_g[nom] = z
        detail[nom] = {"m": m, "mu_null": mu, "u_null": u, "z": z}
        print(f"[{nom:5s}] m={m:+7.4f}  mu={mu:+7.4f}  u={u:.4f}  z={z:+8.3f}")

    # 3. N2 (comptage d'ordre) et N3 (permutation des C_GRP) sur la base
    m_base = detail["base"]["m"]
    ms_n2 = np.empty(N_TIRAGES)
    for t in range(N_TIRAGES):
        C_ordre = [C_Zn(1 + rng._below(240)) for _ in range(len(C_grp))]
        ms_n2[t] = mesure(C_alg, C_ordre)
    q_n2 = float(np.mean(ms_n2 <= m_base))
    ms_n3 = np.empty(N_TIRAGES)
    for t in range(N_TIRAGES):
        ms_n3[t] = mesure(C_alg, list(nul_permutation(np.array(C_grp, dtype=float), rng)))
    q_n3 = float(np.mean(ms_n3 <= m_base))

    # 4. Controles positifs (deterministes)
    u_base = detail["base"]["u_null"]
    # c1 : 2I -> I (ordre 60, quotient 2I/{+/-1})
    grp_c1 = sorted([("Z_%d" % n, groupe_Z(n), None) for n in range(1, 9)]
                    + [("2D_%d" % n, groupe_2D(n), None) for n in range(2, 6)]
                    + [("2T", groupe_2T(), None), ("2O", groupe_2O(), None), ("I", groupe_I(), canon_I)],
                    key=lambda x: (len(x[1]), x[0]))
    m_c1 = mesure(C_alg, C_grp_de(grp_c1))
    effet_c1 = (m_base - m_c1) / u_base
    # c2 : intervertir les maxima (forcer A_F <-> 2T)
    grp_c2 = list(groupes)
    i_2I = next(i for i, (nom, _, _) in enumerate(grp_c2) if nom == "2I")
    i_2T = next(i for i, (nom, _, _) in enumerate(grp_c2) if nom == "2T")
    grp_c2[i_2I], grp_c2[i_2T] = grp_c2[i_2T], grp_c2[i_2I]
    m_c2 = mesure(C_alg, C_grp_de(grp_c2))
    effet_c2 = (m_base - m_c2) / u_base
    # c3 : retirer la condition d'ordre 1
    C_alg_sans = [C_inv(dims_irreps_alg(s), d, 1.0, False) for s, d in algs]
    m_c3 = mesure(C_alg_sans, C_grp_de(groupes, 1.0, False))
    effet_c3 = abs(m_base - m_c3) / u_base

    controles = {"c1": effet_c1, "c2": effet_c2, "c3": effet_c3}

    # 5. Verdict (moteur gele ; seuil MCS-03 = 3,4 ; CS0 si un controle muet)
    v = evaluer("MCS-03", z_par_g, controles)

    res = {
        "carte": "MCS-03",
        "empreinte_carte": EMPREINTE_CARTE,
        "empreinte_donnees": emp_donnees,
        "prng": {"algorithme": "ChaCha20-IETF (RFC 8439), nonce = 12 octets nuls",
                 "cle_publique_hex": cle.hex(),
                 "empreinte_flot_64o": empreinte_flot,
                 "octets_consumes": rng.tirages,
                 "ordre_tirages": "N1 (base, g1..g6) puis N2 puis N3"},
        "familles": {"n_ALG": len(algs), "n_GRP": len(groupes),
                     "C_ALG": C_alg, "C_GRP": C_grp,
                     "rang_A_F": rang_AF, "C_A_F": C_alg[rang_AF],
                     "irreps_reelles_GRP": dims_grp},
        "configurations": detail,
        "N2_ordre": {"quantile_m_base": q_n2},
        "N3_permutation": {"quantile_m_base": q_n3},
        "controles": {"c1_2I_vers_I": {"m": m_c1, "effet_u": effet_c1},
                      "c2_maxima_invertes": {"m": m_c2, "effet_u": effet_c2},
                      "c3_sans_ordre1": {"m": m_c3, "effet_u": effet_c3}},
        "verdict": v.to_dict(),
    }
    return res

if __name__ == "__main__":
    res = main()
    os.makedirs(os.path.join(RACINE, "resultats"), exist_ok=True)
    sortie = os.path.join(RACINE, "resultats", "mcs03_resultats.json")
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("\n=== VERDICT MCS-03 ===")
    print(json.dumps(res["verdict"], ensure_ascii=False, indent=2))
    print("sha256(resultats) =", hashlib.sha256(open(sortie, "rb").read()).hexdigest())
