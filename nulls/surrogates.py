"""surrogates.py — Generateurs de modeles nuls (jalon 2).

Doctrine : chaque carte declare ce que le hasard structurel peut produire seul.
Ce module fournit les briques :

- surrogates FT (phase randomisee, spectre de puissance conserve exactement) ;
- surrogates IAAFT (spectre ET distribution d'amplitude conserves) — c'est le
  nul central de MCS-02 : si une coincidence est spectrale, elle y survit ;
  si elle est dans la phase, elle y meurt ;
- permutation (nul de reappariement, MCS-01) ;
- bootstrap par blocs (dependances temporelles) ;
- famille de lois lisses aleatoires a*ln(Z)+b (nul N3 de MCS-01) ;
- bruit filtre de meme DSP (nul N2 de MCS-02).

Les graines sont explicites et consignees au journal. Pour les campagnes
scellees (jalon 4), le PRNG sera ChaCha20-IETF conformement au manifeste ;
ici (synthetique), numpy.default_rng suffit et est documente.
"""
from __future__ import annotations

import numpy as np


def ft_surrogate(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Surrogate a phase randomisee : spectre de puissance inchange, phase detruite."""
    X = np.fft.rfft(x)
    n = len(X)
    phases = rng.uniform(0.0, 2.0 * np.pi, size=n)
    phases[0] = 0.0
    if len(x) % 2 == 0:
        phases[-1] = 0.0  # composante de Nyquist reelle
    return np.fft.irfft(np.abs(X) * np.exp(1j * phases), n=len(x))


def iaaft(x: np.ndarray, rng: np.random.Generator, n_iter: int = 10) -> np.ndarray:
    """IAAFT : conserve le spectre (approx.) et la distribution d'amplitude.
    Reference : Schreiber & Schmitz, surrogates iteres a amplitude ajustee."""
    amplitudes = np.abs(np.fft.rfft(x))
    valeurs_triees = np.sort(x)
    s = ft_surrogate(x, rng)
    for _ in range(n_iter):
        # 1) imposer les amplitudes spectrales d'origine
        S = np.fft.rfft(s)
        s = np.fft.irfft(amplitudes * np.exp(1j * np.angle(S)), n=len(x))
        # 2) imposer la distribution temporelle d'origine (par les rangs)
        s = valeurs_triees[np.argsort(np.argsort(s))]
    return s


def permutation(valeurs: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Reappariement aleatoire : detruit toute correspondance reelle entre
    indice et valeur, conserve la distribution marginale."""
    return rng.permutation(valeurs)


def bootstrap_blocs(x: np.ndarray, taille_bloc: int,
                    rng: np.random.Generator) -> np.ndarray:
    """Bootstrap par blocs : conserve les dependances courtes, detruit les longues."""
    n = len(x)
    n_blocs = int(np.ceil(n / taille_bloc))
    starts = rng.integers(0, max(1, n - taille_bloc), size=n_blocs)
    out = np.concatenate([x[s:s + taille_bloc] for s in starts])
    return out[:n]


def lois_lisses_aleatoires(Z: np.ndarray, n: int,
                           rng: np.random.Generator) -> np.ndarray:
    """Famille nulle N3 de MCS-01 : y = a*ln(Z) + b,
    a ~ U(-3, 0), b ~ U(0, 4). Retourne une matrice (n, len(Z))."""
    a = rng.uniform(-3.0, 0.0, size=(n, 1))
    b = rng.uniform(0.0, 4.0, size=(n, 1))
    return a * np.log(Z)[None, :] + b


def bruit_meme_dsp(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Bruit synthetique de meme densite spectrale, sans structure de phase.
    Operationnellement identique au surrogate FT ; alias documente (nul N2)."""
    return ft_surrogate(x, rng)
