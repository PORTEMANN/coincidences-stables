"""positive_controls.py — Sabotages obligatoires (jalon 2).

Doctrine (manifeste section 4, regle 4) : un controle positif est un sabotage
qui DOIT casser une correspondance reelle. S'il ne casse rien, le test est
aveugle et le verdict est CS0 — quelle que soit la valeur de Sigma.

Les controles portent sur le BANC (donnees de calibration a effet connu),
pas sur la carte : on demontre que l'instrument voit ce qu'il doit voir
et perd ce qu'il doit perdre.

Effets mesures en unites u_null (seuil de pouvoir : >= 2, gele dans mcs_score).
"""
from __future__ import annotations

import numpy as np


def effet_u(m_avant: float, m_apres: float, u_null: float) -> float:
    """Effet d'un sabotage en unites d'incertitude du nul.
    Positif = la mesure a chute comme prevu. < SEUIL_CONTROLE => controle muet."""
    if u_null <= 0:
        raise ValueError("u_null nul")
    return (m_avant - m_apres) / u_null


def melange_appariement(seq_a: np.ndarray, seq_b: np.ndarray,
                        rng: np.random.Generator) -> tuple:
    """c1 : brise l'appariement index par index entre deux domaines.
    Toute correspondance plantee par fenetre doit s'effondrer."""
    return seq_a, seq_b[rng.permutation(len(seq_b))]


def injecter_pac(fs: float, duree_s: float, profondeur: float,
                 rng: np.random.Generator,
                 f_theta: float = 6.0, f_gamma: float = 40.0) -> np.ndarray:
    """c2 : signal de calibration avec couplage phase-amplitude CONNU.
    La bande gamma est modulee par la phase theta a la profondeur donnee.
    Le banc doit retrouver un I4 eleve ; sinon I4 est aveugle."""
    n = int(fs * duree_s)
    t = np.arange(n) / fs
    theta = np.sin(2.0 * np.pi * f_theta * t
                   + 0.5 * np.cumsum(rng.normal(0, 0.02, n)))
    phase_theta = np.angle(_signal_analytique(theta))
    gamma = rng.normal(0, 1, n)
    gamma = _passe_bande(gamma, fs, f_gamma - 2.0, f_gamma + 2.0)
    envelope = 1.0 + profondeur * np.cos(phase_theta)
    fond = 0.3 * rng.normal(0, 1, n)
    return theta + envelope * gamma + fond


def _signal_analytique(x: np.ndarray) -> np.ndarray:
    X = np.fft.fft(x)
    n = len(x)
    h = np.zeros(n)
    h[0] = 1.0
    h[1:(n + 1) // 2] = 2.0
    if n % 2 == 0:
        h[n // 2] = 1.0
    return np.fft.ifft(X * h)


def _passe_bande(x: np.ndarray, fs: float, f1: float, f2: float) -> np.ndarray:
    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(len(x), d=1.0 / fs)
    X[(freqs < f1) | (freqs > f2)] = 0.0
    return np.fft.irfft(X, n=len(x))
