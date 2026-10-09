"""mcs01_runner.py — Execution unique MCS-01 (jalon 4).

Carte : MCS-01-kZ-AME.md (SHA256_CARTE 45185f63459fcf9e580a0a86725110a9bdf462aa1754b56321259a73ca34c0e1).
Ce fichier est hache et consigne au journal JALON-4 AVANT execution (execution unique).

PRNG (doctrine jalon 4, journal GENESE_J4) :
    cle = SHA-256("MCS-J4|" + empreinte_carte_hex + "|" + empreinte_donnees_hex)
    flot ChaCha20-IETF (RFC 8439), nonce = 12 octets nuls, compteur depuis 0.
    Ordre des tirages (publie) :
      1. pour chaque configuration dans l'ordre [g1, g2, g3, g4, g5, g6_pair,
         g6_impair, g7, g8] : N1 = 10 000 permutations (generateur nul gele) ;
      2. N3 = 10 000 lois lisses (generateur gele lois_lisses_aleatoires)
         sur l'ensemble Z de g1.
    c1, c2, N2 sont deterministes (aucun tirage).

Conventions declarees :
  - annee julienne AN_S = 365,25 * 86400 s ;
  - vallee : 'stbl' (NUBASE) OU t1/2 > 10^9 ans ; JEFF-3.3 : T1/2 = 0 (stable)
    OU T1/2 > 10^9 ans ; etats fondamentaux seuls (LISO = 0) ;
  - N/Z de base : isotope stable le plus lourd a Z donne (lexique) ;
    g7 : moyenne ponderee par abondance IS>0 ; si aucun IS>0 a ce Z,
    repli sur l'isotope le plus lourd (convention declaree) ;
  - nul physique de Weizsaecker : N/Z = 1 + cw * A^(2/3), cw = a_c/(2*a_sym),
    a_c = 0,711 MeV, a_sym = 23,21 MeV ; A(Z) resolu par point fixe
    A <- Z*(2 + cw*A^(2/3)), A0 = 2Z, 50 iterations (deterministe) ;
    c3 : terme coulombien supprime => N/Z = 1 ;
  - u_null : ecart-type population (ddof=0) des 10 000 m permutes ;
  - verdict : moteur gele evaluer("MCS-01", ...), puis regle carte section 8 :
    CS+ exige AUSSI marge N2 >= 0,05, sinon CSp ; si c3 muet (N2 aveugle),
    CS+ impossible => plafond CSp (declare).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import struct
import sys

import numpy as np
from scipy.optimize import curve_fit

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "code"))
sys.path.insert(0, os.path.join(RACINE, "nulls"))
from mcs_score import evaluer, z_score, Verdict, JournalChaine  # noqa: E402
from surrogates import permutation as nul_permutation  # noqa: E402
from surrogates import lois_lisses_aleatoires  # noqa: E402

# --- Empreintes liees (journal J4, record DONNEES_MCS01) ---------------------
EMPREINTE_CARTE = "45185f63459fcf9e580a0a86725110a9bdf462aa1754b56321259a73ca34c0e1"
EMPREINTE_DONNEES = "57caec6e101ff7470d2ff992ddacf875a02cc654cd17193922cbc1cb6df3b05c"
FICHIERS = {
    "AME2012_masses": "donnees/ame/mass.mas12",
    "AME2012_nubase": "donnees/ame/nubtab12.asc",
    "AME2003_masses": "donnees/ame/mass.mas03",
    "AME2003_nubase": "donnees/ame/nubtab03.asc",
    "AME2020_masses": "donnees/ame/mass_1.mas20.txt",
    "AME2020_nubase": "donnees/ame/nubase_4.mas20.txt",
    "JEFF33_decroissance": "donnees/jeff/JEFF33-rdd_all.asc",
}

ALPHA_INV_2018 = 137.035999084   # CODATA 2018 (gele)
ALPHA_INV_2022 = 137.035999177   # CODATA 2022 (deformation g5)
AN_S = 365.25 * 86400.0          # annee julienne en secondes
SEUIL_T12_S = 1.0e9 * AN_S       # 10^9 ans en secondes
N_PERM = 10000                   # N1
N_LOIS = 10000                   # N3
MARGE_N2 = 0.05                  # carte section 8
A_COULOMB = 0.711                # MeV (Weizsaecker)
A_SYM = 23.21                    # MeV
Z_MAGIQUES = (2, 8, 20, 28, 50, 82)

# --- PRNG ChaCha20-IETF (RFC 8439), pur Python, deterministe -----------------

def _qr(x, a, b, c, d):
    x[a] = (x[a] + x[b]) & 0xFFFFFFFF; x[d] ^= x[a]; x[d] = ((x[d] << 16) | (x[d] >> 16)) & 0xFFFFFFFF
    x[c] = (x[c] + x[d]) & 0xFFFFFFFF; x[b] ^= x[c]; x[b] = ((x[b] << 12) | (x[b] >> 20)) & 0xFFFFFFFF
    x[a] = (x[a] + x[b]) & 0xFFFFFFFF; x[d] ^= x[a]; x[d] = ((x[d] << 8) | (x[d] >> 24)) & 0xFFFFFFFF
    x[c] = (x[c] + x[d]) & 0xFFFFFFFF; x[b] ^= x[c]; x[b] = ((x[b] << 7) | (x[b] >> 25)) & 0xFFFFFFFF


def _bloc_chacha20(cle32: bytes, compteur: int, nonce12: bytes) -> bytes:
    const = b"expand 32-byte k"
    etat = list(struct.unpack("<4I", const) + struct.unpack("<8I", cle32)
                + (compteur,) + struct.unpack("<3I", nonce12))
    travail = list(etat)
    for _ in range(10):
        _qr(travail, 0, 4, 8, 12); _qr(travail, 1, 5, 9, 13)
        _qr(travail, 2, 6, 10, 14); _qr(travail, 3, 7, 11, 15)
        _qr(travail, 0, 5, 10, 15); _qr(travail, 1, 6, 11, 12)
        _qr(travail, 2, 7, 8, 13); _qr(travail, 3, 4, 9, 14)
    return struct.pack("<16I", *[(travail[i] + etat[i]) & 0xFFFFFFFF for i in range(16)])


class PRNGChaCha:
    """Flot d'octets ChaCha20-IETF expose en Generateur (duck-typing numpy).

    Methodes : uniform, permutation, integers, normal — couvre l'interface
    utilisee par les generateurs nuls geles.
    """

    def __init__(self, cle32: bytes, nonce12: bytes = b"\x00" * 12):
        self.cle = cle32
        self.nonce = nonce12
        self.compteur = 0
        self.tampon = b""
        self.tirages = 0  # nombre d'octets consommes (traçabilite)

    def _octets(self, n: int) -> bytes:
        while len(self.tampon) < n:
            self.tampon += _bloc_chacha20(self.cle, self.compteur, self.nonce)
            self.compteur = (self.compteur + 1) & 0xFFFFFFFF
        out, self.tampon = self.tampon[:n], self.tampon[n:]
        self.tirages += n
        return out

    def _u64(self, n: int) -> np.ndarray:
        return np.frombuffer(self._octets(8 * n), dtype="<u8").copy()

    def uniform(self, low=0.0, high=1.0, size=None):
        n = 1 if size is None else int(np.prod(size))
        u = (self._u64(n) >> 11) * (1.0 / (1 << 53))
        out = low + (high - low) * u
        if size is None:
            return float(out[0])
        return out.reshape(size)

    def _below(self, n: int) -> int:
        limite = ((1 << 64) // n) * n
        while True:
            x = int(self._u64(1)[0])
            if x < limite:
                return x % n

    def permutation(self, x):
        arr = np.array(x, copy=True)
        for i in range(len(arr) - 1, 0, -1):
            j = self._below(i + 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    def integers(self, low, high=None, size=None):
        if high is None:
            low, high = 0, low
        n = 1 if size is None else int(np.prod(size))
        out = np.array([self._below(high - low) + low for _ in range(n)])
        if size is None:
            return int(out[0])
        return out.reshape(size)

    def normal(self, size=None):
        n = 1 if size is None else int(np.prod(size))
        m = (n + 1) // 2
        u1 = self.uniform(0.0, 1.0, size=m)
        u2 = self.uniform(0.0, 1.0, size=m)
        r = np.sqrt(-2.0 * np.log(u1))
        z = np.concatenate([r * np.cos(2 * np.pi * u2), r * np.sin(2 * np.pi * u2)])[:n]
        if size is None:
            return float(z[0])
        return z.reshape(size)


# --- Lecture des donnees -----------------------------------------------------
UNITES_S = {"ys": 1e-24, "zs": 1e-21, "as": 1e-18, "fs": 1e-15, "ps": 1e-12,
            "ns": 1e-9, "us": 1e-6, "ms": 1e-3, "s": 1.0, "m": 60.0,
            "h": 3600.0, "d": 86400.0, "y": AN_S, "ky": 1e3 * AN_S,
            "My": 1e6 * AN_S, "Gy": 1e9 * AN_S, "Ty": 1e12 * AN_S,
            "Py": 1e15 * AN_S, "Ey": 1e18 * AN_S, "Zy": 1e21 * AN_S,
            "Yy": 1e24 * AN_S}
_RX_T12 = re.compile(r"(\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?)\s*(~?)("
                     + "|".join(sorted(UNITES_S, key=len, reverse=True)) + r")\b")


def lire_nubase(chemin: str, zone=(41, 92)) -> list:
    """Nucléides fondamentaux : (Z, A, t12_s|None, stbl, IS|None)."""
    out = []
    with open(chemin, encoding="ascii") as f:
        for ligne in f:
            if ligne.startswith("#") or len(ligne) < 60:
                continue
            A = int(ligne[0:3])
            Zi = int(ligne[4:8])
            if Zi % 10 != 0:
                continue  # isomères exclus
            Z = Zi // 10
            seg = ligne[zone[0]:zone[1]]
            stbl = "stbl" in seg
            t12 = 0.0 if stbl else None
            if not stbl:
                m = _RX_T12.search(seg)
                if m:
                    t12 = float(m.group(1)) * UNITES_S[m.group(3)]
            m_is = re.search(r"IS=\s*(\d+(?:\.\d+)?)", ligne)
            IS = float(m_is.group(1)) if m_is else None
            out.append((Z, A, t12, stbl, IS))
    return out


def _endf_float(champ: str) -> float:
    x = champ.strip()
    if not x:
        return 0.0
    m = re.match(r"^([+-]?\d*\.\d+|\d+\.?)([+-]\d+)$", x)
    if m:
        return float(f"{m.group(1)}e{m.group(2)}")
    return float(x)


def lire_jeff(chemin: str) -> list:
    """JEFF-3.3 RDD combine : (Z, A, t12_s) sections MF8 MT457, LISO = 0."""
    t12_par_za = {}
    with open(chemin, encoding="ascii", errors="replace") as f:
        lignes = f.readlines()
    i, n = 0, len(lignes)
    while i < n:
        l = lignes[i]
        if len(l) >= 75 and l[70:72] == " 8" and l[72:75] == "457" and int(l[75:80]) == 1:
            ZA = _endf_float(l[0:11])
            LISO = int(_endf_float(l[33:44]))
            t12 = _endf_float(lignes[i + 1][0:11])
            if LISO == 0 and ZA not in t12_par_za:
                t12_par_za[ZA] = t12
            i += 2
        else:
            i += 1
    out = []
    for ZA, t12 in t12_par_za.items():
        Z, A = int(ZA) // 1000, int(ZA) % 1000
        if Z >= 1:
            out.append((Z, A, t12, t12 == 0.0, None))
    return out


def vallee(nuclides: list) -> list:
    """Lexique gele : stbl OU t1/2 > 10^9 ans."""
    return [r for r in nuclides if r[3] or (r[2] is not None and r[2] > SEUIL_T12_S)]


def nz_par_Z(v: list, convention: str = "plus_lourd") -> dict:
    """N/Z observe par Z. plus_lourd : isotope stable le plus lourd ;
    moyenne : ponderee par abondance IS>0 (repli plus_lourd si aucun IS)."""
    par_z = {}
    for Z, A, t12, stbl, IS in v:
        par_z.setdefault(Z, []).append((A, IS))
    out = {}
    for Z, lst in par_z.items():
        if convention == "plus_lourd":
            A = max(a for a, _ in lst)
            out[Z] = (A - Z) / Z
        else:
            ab = [(a, isv) for a, isv in lst if isv is not None and isv > 0]
            if ab:
                w = np.array([isv for _, isv in ab])
                vals = np.array([(a - Z) / Z for a, _ in ab])
                out[Z] = float(np.average(vals, weights=w))
            else:
                A = max(a for a, _ in lst)
                out[Z] = (A - Z) / Z
    return out


# --- Loi candidate, mesure, nuls ---------------------------------------------

def k_loi(Z: np.ndarray, alpha_inv: float = ALPHA_INV_2018) -> np.ndarray:
    """k(Z) = -(1/(1000*alpha)) * ln(Z) + 3/2 — zero parametre libre."""
    return -(alpha_inv / 1000.0) * np.log(Z) + 1.5


def mesure_m(y_obs: np.ndarray, y_pred: np.ndarray) -> float:
    """m = -log10(RMS(residu)), qualite croissante avec la precision."""
    rms = float(np.sqrt(np.mean((y_obs - y_pred) ** 2)))
    return -math.log10(rms)


def nul_weizsacker(Z: np.ndarray, coulomb: bool = True) -> np.ndarray:
    """N/Z = 1 + cw*A^(2/3) ; coulomb=False => N/Z = 1 (controle c3)."""
    if not coulomb:
        return np.ones_like(Z, dtype=float)
    cw = A_COULOMB / (2.0 * A_SYM)
    A = 2.0 * Z.astype(float)
    for _ in range(50):
        A = Z * (2.0 + cw * A ** (2.0 / 3.0))
    return (A - Z) / Z


# --- Pipeline principal ------------------------------------------------------

def main() -> dict:
    # 0. Liage aux donnees declarees au journal
    empreintes = {}
    for nom, rel in sorted(FICHIERS.items()):
        raw = open(os.path.join(RACINE, rel), "rb").read()
        empreintes[nom] = hashlib.sha256(raw).hexdigest()
    canon = "\n".join(f"{nom}:{empreintes[nom]}" for nom in sorted(empreintes))
    emp = hashlib.sha256(canon.encode()).hexdigest()
    assert emp == EMPREINTE_DONNEES, "empreinte donnees : divergence avec le journal J4"
    # Empreinte carte : convention de scellement J3 — hash du contenu PRE-GEL
    # (dernier bloc fenced remplace par le bloc nul conserve dans l'acte).
    acte = json.load(open(os.path.join(RACINE, "scellement", "SCCELLEMENT-J3.json"),
                          encoding="utf-8"))
    entree = acte["fichiers"]["cartes/MCS-01-kZ-AME.md"]
    contenu = open(os.path.join(RACINE, "cartes", "MCS-01-kZ-AME.md"),
                   encoding="utf-8").read()
    blocs = list(re.finditer(r"```\n.*?```", contenu, re.DOTALL))
    pre_gel = contenu[:blocs[-1].start()] + entree["bloc_nul_original"] + contenu[blocs[-1].end():]
    h_carte = hashlib.sha256(pre_gel.encode("utf-8")).hexdigest()
    assert h_carte == entree["sha256_pre_gel"] == EMPREINTE_CARTE, \
        "empreinte carte : divergence avec le scellement J3"

    # 1. PRNG public derive
    cle = hashlib.sha256(f"MCS-J4|{EMPREINTE_CARTE}|{EMPREINTE_DONNEES}".encode("ascii")).digest()
    rng = PRNGChaCha(cle)
    empreinte_flot = rng._octets(64).hex()  # empreinte publique du flot

    # 2. Vallees
    v12 = vallee(lire_nubase(os.path.join(RACINE, FICHIERS["AME2012_nubase"])))
    v03 = vallee(lire_nubase(os.path.join(RACINE, FICHIERS["AME2003_nubase"])))
    v20 = vallee(lire_nubase(os.path.join(RACINE, FICHIERS["AME2020_nubase"]), zone=(45, 100)))
    vj33 = vallee(lire_jeff(os.path.join(RACINE, FICHIERS["JEFF33_decroissance"])))

    nz_train = {z: nz for z, nz in nz_par_Z(v12).items() if 1 <= z <= 82}   # AME2012, apprentissage des nuls
    nz_20 = {z: nz for z, nz in nz_par_Z(v20).items() if 1 <= z <= 92}     # AME2020, test
    nz_20_moy = {z: nz for z, nz in nz_par_Z(v20, "moyenne").items() if 1 <= z <= 92}
    nz_03 = {z: nz for z, nz in nz_par_Z(v03).items() if 1 <= z <= 92}
    nz_j33 = {z: nz for z, nz in nz_par_Z(vj33).items() if 1 <= z <= 92}

    # 3. Configurations (ordre de tirage publie)
    def conf(nz_dict, alpha=ALPHA_INV_2018, zmin=1, zmax=92, retrait=()):
        Z = np.array(sorted(z for z in nz_dict if zmin <= z <= zmax and z not in retrait), dtype=float)
        y = np.array([nz_dict[int(z)] for z in Z])
        return Z, y

    CONFIGS = [
        ("g1", *conf(nz_20)),                                    # AME2012 -> AME2020 (hors-echantillon)
        ("g2", *conf(nz_03)),                                    # AME2020 -> AME2003
        ("g3", *conf(nz_j33)),                                   # AME -> JEFF-3.3
        ("g4", *conf(nz_20, retrait=Z_MAGIQUES)),                # retrait Z magiques
        ("g5", *conf(nz_20, alpha=ALPHA_INV_2022)),              # CODATA 2022
        ("g6_pair", *conf(nz_20, retrait=())),                   # filtre pair applique ci-dessous
        ("g6_impair", *conf(nz_20)),
        ("g7", *conf(nz_20_moy)),                                # moyenne ponderee
        ("g8", *conf(nz_20, zmin=20)),                           # retrait des legers
    ]
    # g6 : sous-ensembles de parite
    cfgs = []
    for nom, Z, y in CONFIGS:
        if nom == "g6_pair":
            m = (Z % 2 == 0); Z, y = Z[m], y[m]
        elif nom == "g6_impair":
            m = (Z % 2 == 1); Z, y = Z[m], y[m]
        cfgs.append((nom, Z, y))

    alpha_par_conf = {"g5": ALPHA_INV_2022}

    # 4. m de la candidate + N1 (10 000 permutations) par configuration
    z_par_g, detail = {}, {}
    for nom, Z, y in cfgs:
        alpha = alpha_par_conf.get(nom, ALPHA_INV_2018)
        y_pred = k_loi(Z, alpha)
        m_reel = mesure_m(y, y_pred)
        m_nuls = np.empty(N_PERM)
        for i in range(N_PERM):
            y_perm = nul_permutation(y, rng)
            m_nuls[i] = mesure_m(y_perm, y_pred)
        mu, u = float(np.mean(m_nuls)), float(np.std(m_nuls))  # ddof=0
        z = z_score(m_reel, mu, u)
        z_par_g[nom] = z
        detail[nom] = {"n_Z": len(Z), "m": m_reel, "mu_null": mu, "u_null": u, "z": z}
        print(f"[{nom:10s}] nZ={len(Z):3d}  m={m_reel:8.4f}  mu={mu:7.4f}  u={u:.4f}  z={z:+8.3f}")

    # 5. N2 : trois nuls ajustes sur AME2012 (Z<=82), evalues sur AME2020 (g1)
    Ztr = np.array(sorted(nz_train), dtype=float)
    ytr = np.array([nz_train[int(z)] for z in Ztr])
    Zev, yev = cfgs[0][1], cfgs[0][2]

    a1, b1 = np.polyfit(np.log(Ztr), ytr, 1)
    f_ln = lambda Z: a1 * np.log(Z) + b1
    f_pow = lambda Z, a, b, c: a * Z ** b + c
    popt, _ = curve_fit(f_pow, Ztr, ytr, p0=(0.015, 0.667, 1.0), maxfev=20000)
    c2poly = np.polyfit(Ztr, ytr, 2)
    f_poly = lambda Z: np.polyval(c2poly, Z)

    nuls_ajustes = {
        "a*lnZ+b": {"params": [float(a1), float(b1)],
                    "m_train": mesure_m(ytr, f_ln(Ztr)), "m_eval": mesure_m(yev, f_ln(Zev))},
        "a*Z^b+c": {"params": [float(p) for p in popt],
                    "m_train": mesure_m(ytr, f_pow(Ztr, *popt)), "m_eval": mesure_m(yev, f_pow(Zev, *popt))},
        "poly_degre2": {"params": [float(p) for p in c2poly],
                        "m_train": mesure_m(ytr, f_poly(Ztr)), "m_eval": mesure_m(yev, f_poly(Zev))},
    }
    m_cand_eval = detail["g1"]["m"]
    meilleur_nul = max(nuls_ajustes, key=lambda k: nuls_ajustes[k]["m_eval"])
    marge = m_cand_eval - nuls_ajustes[meilleur_nul]["m_eval"]
    marge_ok = bool(marge >= MARGE_N2)

    # Nul physique Weizsaecker (complexite egale) + controle c3
    y_weiz = nul_weizsacker(Zev, coulomb=True)
    y_un = nul_weizsacker(Zev, coulomb=False)
    m_weiz, m_un = mesure_m(yev, y_weiz), mesure_m(yev, y_un)
    c3_effet = m_weiz - m_un          # > 0 attendu : retirer Coulomb degrade
    n2_aveugle = bool(c3_effet < 0)

    # 6. N3 : 10 000 lois lisses (generateur gele) sur l'ensemble g1
    lois = lois_lisses_aleatoires(Zev, N_LOIS, rng)
    m_famille = np.array([mesure_m(yev, lois[i]) for i in range(N_LOIS)])
    q99 = float(np.quantile(m_famille, 0.99))
    n3_ok = bool(m_cand_eval > q99)

    # 7. Controles positifs (deterministes)
    mu1, u1 = detail["g1"]["mu_null"], detail["g1"]["u_null"]
    # c1 : permutation Z <-> N dans les donnees (AME2020, Z' <= 92)
    swap = {}
    for Z, A, *_ in v20:
        N = A - Z
        if 1 <= N <= 92:
            swap.setdefault(N, []).append(A)
    Zc1 = np.array(sorted(swap), dtype=float)
    yc1 = np.array([(max(swap[int(z)]) - int(z)) / int(z) for z in Zc1])
    m_c1 = mesure_m(yc1, k_loi(Zc1))
    z_c1 = z_score(m_c1, mu1, u1)
    effet_c1 = detail["g1"]["z"] - z_c1       # chute de z ; >= 2 exige
    # c2 : alpha -> alpha/2 (pente doublee)
    m_c2 = mesure_m(yev, k_loi(Zev, 2.0 * ALPHA_INV_2018))
    z_c2 = z_score(m_c2, mu1, u1)
    effet_c2 = detail["g1"]["z"] - z_c2

    controles = {"c1": effet_c1, "c2": effet_c2}

    # 8. Verdict (moteur gele + regle carte section 8 pour N2)
    v = evaluer("MCS-01", z_par_g, controles)
    motif = v.motif
    verdict = v.verdict
    if verdict == "CS+" and not marge_ok:
        verdict, motif = "CSp", "Sigma >= seuil mais marge N2 < 0,05 (carte section 8)"
    if verdict == "CS+" and n2_aveugle:
        verdict, motif = "CSp", "Sigma >= seuil mais c3 muet : N2 aveugle (declare)"
    vfinal = Verdict(verdict, v.sigma, v.seuil, motif, z_par_g, controles)

    # 9. Resultat complet
    res = {
        "carte": "MCS-01",
        "empreinte_carte": EMPREINTE_CARTE,
        "empreinte_donnees": EMPREINTE_DONNEES,
        "empreintes_fichiers": empreintes,
        "prng": {"algorithme": "ChaCha20-IETF (RFC 8439), nonce = 12 octets nuls",
                 "cle_publique_hex": cle.hex(),
                 "derivation": "SHA-256('MCS-J4|' + empreinte_carte + '|' + empreinte_donnees)",
                 "empreinte_flot_64o": empreinte_flot,
                 "octets_consumes": rng.tirages,
                 "ordre_tirages": "N1 (g1..g8) puis N3 (g1)"},
        "vallees": {"AME2012": len(v12), "AME2003": len(v03),
                    "AME2020": len(v20), "JEFF33": len(vj33)},
        "configurations": detail,
        "N2": {"nuls_ajustes": nuls_ajustes, "meilleur_nul": meilleur_nul,
               "m_candidate_eval": m_cand_eval, "marge": marge,
               "marge_requise": MARGE_N2, "marge_ok": marge_ok},
        "N3": {"q99_famille": q99, "m_candidate": m_cand_eval, "hors_q99": n3_ok},
        "controles": {"c1": {"m_sabote": m_c1, "z_sabote": z_c1, "effet_u": effet_c1},
                      "c2": {"m_sabote": m_c2, "z_sabote": z_c2, "effet_u": effet_c2},
                      "c3": {"m_weizsacker": m_weiz, "m_sans_coulomb": m_un,
                             "effet_m": c3_effet, "n2_aveugle": n2_aveugle}},
        "verdict": vfinal.to_dict(),
    }
    return res


if __name__ == "__main__":
    res = main()
    os.makedirs(os.path.join(RACINE, "resultats"), exist_ok=True)
    sortie = os.path.join(RACINE, "resultats", "mcs01_resultats.json")
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("\n=== VERDICT MCS-01 ===")
    print(json.dumps(res["verdict"], ensure_ascii=False, indent=2))
    print("sha256(resultats) =", hashlib.sha256(open(sortie, "rb").read()).hexdigest())
