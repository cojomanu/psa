import tkinter as tk

import sounddevice as sd

from audio import Microfon
from gui import FereastraAcordor
from notes import hz_la_nota
from pitch import Netezire, detecteaza_frecventa, nivel_rms

# sub acest volum nu se considera ca cant nimic
PRAG_RMS = 0.01


def main():
    try:
        microfon = Microfon()
    except sd.PortAudioError as eroare:
        print("Nu pot deschide microfonul:", eroare)
        return

    netezire = Netezire(marime=5)

    def ia_nota(a4):
        bloc = microfon.ultimul_bloc()

        if nivel_rms(bloc) < PRAG_RMS:
            netezire.reseteaza()
            return None

        hz = detecteaza_frecventa(bloc, microfon.fs)
        if hz is None:
            return None

        return hz_la_nota(netezire.adauga(hz), a4)

    root = tk.Tk()
    fereastra = FereastraAcordor(root, ia_nota)

    microfon.porneste()
    try:
        fereastra.porneste()
    finally:
        microfon.opreste()


if __name__ == "__main__":
    main()
