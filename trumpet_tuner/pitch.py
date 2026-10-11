from collections import deque

import numpy as np

F_MIN = 150.0
F_MAX = 1100.0
PRAG_YIN = 0.2   # mai mic = mai strict


def nivel_rms(semnal: np.ndarray) -> float:
    semnal = semnal - np.mean(semnal)
    return float(np.sqrt(np.mean(semnal ** 2)))


def detecteaza_frecventa(semnal: np.ndarray, fs: int,
                         f_min: float = F_MIN, f_max: float = F_MAX,
                         prag: float = PRAG_YIN):
    """YIN. Intoarce frecventa in Hz sau None daca nu gaseste un sunet clar."""
    semnal = semnal.astype(np.float64) - np.mean(semnal)

    tau_min = int(fs / f_max)
    tau_max = int(fs / f_min)
    w = len(semnal) - tau_max
    if w <= tau_max:
        return None

    # functia de diferenta
    d = np.zeros(tau_max + 1)
    for tau in range(1, tau_max + 1):
        dif = semnal[:w] - semnal[tau:tau + w]
        d[tau] = np.dot(dif, dif)

    # diferenta cumulativ normalizata
    cmnd = np.ones(tau_max + 1)
    suma = np.cumsum(d[1:])
    cmnd[1:] = d[1:] * np.arange(1, tau_max + 1) / np.maximum(suma, 1e-12)

    # primul minim local sub prag
    tau = None
    for t in range(tau_min, tau_max):
        if cmnd[t] < prag:
            while t + 1 < tau_max and cmnd[t + 1] < cmnd[t]:
                t += 1
            tau = t
            break
    if tau is None:
        return None

    # interpolare parabolica
    s0, s1, s2 = cmnd[tau - 1], cmnd[tau], cmnd[tau + 1]
    numitor = 2 * (s0 - 2 * s1 + s2)
    deplasare = (s0 - s2) / numitor if numitor != 0 else 0.0

    return fs / (tau + deplasare)


class Netezire:
    """Mediana pe ultimele valori, ca acul sa nu tremure."""

    def __init__(self, marime: int = 5):
        self._valori = deque(maxlen=marime)

    def adauga(self, hz: float) -> float:
        self._valori.append(hz)
        return float(np.median(self._valori))

    def reseteaza(self):
        self._valori.clear()
