"""ash_invariants.py — Pipeline ASH gele (carte MCS-02, section 2).

Pipeline : retrait de tendance lineaire -> Welch (segments 4 s, recouvrement 50 %)
-> I = (I1, I2, I3, I4) dans R^4.

I1 : pente beta de la regression log-log de la DSP sur 1-40 Hz.
I2 : entropie de Shannon de la DSP normalisee sur 1-40 Hz / log(nb bins).
I3 : fraction de l'energie des pics (prominence > 3 sigma) dont les rapports
     de frequences sont entiers a +/- 2 %.
I4 : indice de modulation (Tort) entre phase 4-8 Hz et amplitude 30-45 Hz.

Toute modification de ce fichier apres le gel = nouvelle carte.
Implementation numpy seule ; transformee de Hilbert par FFT (signal analytique).
"""
from __future__ import annotations

import numpy as np

BANDE_I12 = (1.0, 40.0)
BANDE_PHASE = (4.0, 8.0)
BANDE_AMPLITUDE = (30.0, 45.0)
NB_BINS_PAC = 18
TOLERANCE_HARMONIE = 0.02


def _detrend(x: np.ndarray) -> np.ndarray:
    t = np.arange(len(x))
    p = np.polyfit(t, x, 1)
    return x - np.polyval(p, t)


def welch_psd(x: np.ndarray, fs: float, seg_s: float = 4.0,
              overlap: float = 0.5) -> tuple:
    seg = int(seg_s * fs)
    step = int(seg * (1.0 - overlap))
    win = np.hanning(seg)
    s2 = np.sum(win ** 2)
    psds = []
    for start in range(0, len(x) - seg + 1, step):
        X = np.fft.rfft(x[start:start + seg] * win)
        psds.append(np.abs(X) ** 2 / (fs * s2))
    return np.fft.rfftfreq(seg, d=1.0 / fs), np.mean(psds, axis=0)


def _signal_analytique(x: np.ndarray) -> np.ndarray:
    X = np.fft.fft(x)
    n = len(x)
    h = np.zeros(n)
    h[0] = 1.0
    h[1:(n + 1) // 2] = 2.0
    if n % 2 == 0:
        h[n // 2] = 1.0
    return np.fft.ifft(X * h)


def _passe_bande(x: np.ndarray, fs: float, bande: tuple) -> np.ndarray:
    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(len(x), d=1.0 / fs)
    X[(freqs < bande[0]) | (freqs > bande[1])] = 0.0
    return np.fft.irfft(X, n=len(x))


def I1_pente(x: np.ndarray, fs: float) -> float:
    f, P = welch_psd(x, fs)
    m = (f >= BANDE_I12[0]) & (f <= BANDE_I12[1]) & (P > 0)
    if m.sum() < 4:
        return float("nan")
    return float(np.polyfit(np.log10(f[m]), np.log10(P[m]), 1)[0])


def I2_entropie(x: np.ndarray, fs: float) -> float:
    f, P = welch_psd(x, fs)
    m = (f >= BANDE_I12[0]) & (f <= BANDE_I12[1])
    p = P[m]
    p = p / p.sum()
    return float(-np.sum(p * np.log(p + 1e-300)) / np.log(len(p)))


def I3_harmonicite(x: np.ndarray, fs: float) -> float:
    f, P = welch_psd(x, fs)
    m = (f >= BANDE_I12[0]) & (f <= BANDE_I12[1])
    f, P = f[m], P[m]
    seuil = P.mean() + 3.0 * P.std()
    pics = P > seuil
    if pics.sum() < 2:
        return 0.0
    fp, Pp = f[pics], P[pics]
    harmonique = np.zeros(len(fp), dtype=bool)
    for i in range(len(fp)):
        for j in range(i + 1, len(fp)):
            r = max(fp[i], fp[j]) / min(fp[i], fp[j])
            n = round(r)
            if n >= 2 and abs(r - n) / n <= TOLERANCE_HARMONIE:
                harmonique[i] = harmonique[j] = True
    if Pp.sum() <= 0:
        return 0.0
    return float(Pp[harmonique].sum() / Pp.sum())


def I4_pac(x: np.ndarray, fs: float) -> float:
    phase = np.angle(_signal_analytique(_passe_bande(x, fs, BANDE_PHASE)))
    amp = np.abs(_signal_analytique(_passe_bande(x, fs, BANDE_AMPLITUDE)))
    bords = np.linspace(-np.pi, np.pi, NB_BINS_PAC + 1)
    moyennes = np.array([
        amp[(phase >= bords[k]) & (phase < bords[k + 1])].mean()
        if np.any((phase >= bords[k]) & (phase < bords[k + 1])) else 0.0
        for k in range(NB_BINS_PAC)
    ])
    if moyennes.sum() <= 0:
        return 0.0
    p = moyennes / moyennes.sum()
    return float((np.log(NB_BINS_PAC)
                  + np.sum(p * np.log(p + 1e-300))) / np.log(NB_BINS_PAC))


def vecteur_invariants(x: np.ndarray, fs: float) -> np.ndarray:
    """I = (I1, I2, I3, I4). Entree : fenetre brute. Pipeline gele."""
    x = _detrend(np.asarray(x, dtype=float))
    return np.array([I1_pente(x, fs), I2_entropie(x, fs),
                     I3_harmonicite(x, fs), I4_pac(x, fs)])


def fenetres(x: np.ndarray, fs: float, fenetre_s: float = 10.0) -> list:
    n = int(fs * fenetre_s)
    return [x[k:k + n] for k in range(0, len(x) - n + 1, n)]
