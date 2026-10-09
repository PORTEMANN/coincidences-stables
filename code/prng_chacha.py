"""prng_chacha.py — PRNG ChaCha20-IETF partage (jalon 4).

Doctrine jalon 4 (journal GENESE_J4) : graine publique deterministe
    cle = SHA-256("MCS-J4|" + empreinte_carte_hex + "|" + empreinte_donnees_hex)
flot ChaCha20-IETF (RFC 8439), nonce = 12 octets nuls, compteur depuis 0.
Aucune graine secrete : l'exigence est la reproductibilite.

Interface duck-typing numpy Generator : uniform, permutation, integers, normal.
"""
from __future__ import annotations

import struct

import numpy as np


def _qr(x, a, b, c, d):
    x[a] = (x[a] + x[b]) & 0xFFFFFFFF; x[d] ^= x[a]; x[d] = ((x[d] << 16) | (x[d] >> 16)) & 0xFFFFFFFF
    x[c] = (x[c] + x[d]) & 0xFFFFFFFF; x[b] ^= x[c]; x[b] = ((x[b] << 12) | (x[b] >> 20)) & 0xFFFFFFFF
    x[a] = (x[a] + x[b]) & 0xFFFFFFFF; x[d] ^= x[a]; x[d] = ((x[d] << 8) | (x[d] >> 24)) & 0xFFFFFFFF
    x[c] = (x[c] + x[d]) & 0xFFFFFFFF; x[b] ^= x[c]; x[b] = ((x[b] << 7) | (x[b] >> 25)) & 0xFFFFFFFF


def bloc_chacha20(cle32: bytes, compteur: int, nonce12: bytes) -> bytes:
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


def _rotl(v, n):
    return ((v << n) | (v >> (32 - n))).astype(np.uint32)


def _qr_vec(x, a, b, c, d):
    x[a] = x[a] + x[b]; x[d] = _rotl(x[d] ^ x[a], 16)
    x[c] = x[c] + x[d]; x[b] = _rotl(x[b] ^ x[c], 12)
    x[a] = x[a] + x[b]; x[d] = _rotl(x[d] ^ x[a], 8)
    x[c] = x[c] + x[d]; x[b] = _rotl(x[b] ^ x[c], 7)


def blocs_chacha20_vec(cle32: bytes, compteur_debut: int, n_blocs: int, nonce12: bytes) -> bytes:
    """n_blocs blocs ChaCha20-IETF consecutifs, vectorises numpy.
    Produit un flot STRICTEMENT IDENTIQUE a bloc_chacha20 (version scalaire)."""
    const = np.frombuffer(b"expand 32-byte k", dtype="<u4")
    cles = np.frombuffer(cle32, dtype="<u4")
    nonce = np.frombuffer(nonce12, dtype="<u4")
    compteurs = (compteur_debut + np.arange(n_blocs, dtype=np.uint64)).astype(np.uint32)
    etat = np.zeros((16, n_blocs), dtype=np.uint32)
    etat[0:4] = const[:, None]
    etat[4:12] = cles[:, None]
    etat[12] = compteurs
    etat[13:16] = nonce[:, None]
    travail = etat.copy()
    for _ in range(10):
        _qr_vec(travail, 0, 4, 8, 12); _qr_vec(travail, 1, 5, 9, 13)
        _qr_vec(travail, 2, 6, 10, 14); _qr_vec(travail, 3, 7, 11, 15)
        _qr_vec(travail, 0, 5, 10, 15); _qr_vec(travail, 1, 6, 11, 12)
        _qr_vec(travail, 2, 7, 8, 13); _qr_vec(travail, 3, 4, 9, 14)
    out = travail + etat
    return out.T.astype("<u4").tobytes()


class PRNGChaCha:
    """Flot d'octets ChaCha20-IETF expose en Generateur (duck-typing numpy)."""

    LOT = 512  # blocs generes par appel vectorise (32 Ko)

    def __init__(self, cle32: bytes, nonce12: bytes = b"\x00" * 12):
        self.cle = cle32
        self.nonce = nonce12
        self.compteur = 0
        self.tampon = b""
        self.tirages = 0

    def _octets(self, n: int) -> bytes:
        while len(self.tampon) < n:
            self.tampon += blocs_chacha20_vec(self.cle, self.compteur, self.LOT, self.nonce)
            self.compteur = (self.compteur + self.LOT) & 0xFFFFFFFF
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

    def normal(self, loc=0.0, scale=1.0, size=None):
        n = 1 if size is None else int(np.prod(size))
        m = (n + 1) // 2
        u1 = self.uniform(0.0, 1.0, size=m)
        u2 = self.uniform(0.0, 1.0, size=m)
        r = np.sqrt(-2.0 * np.log(u1))
        z = np.concatenate([r * np.cos(2 * np.pi * u2), r * np.sin(2 * np.pi * u2)])[:n]
        out = loc + scale * z
        if size is None:
            return float(out[0])
        return out.reshape(size)
