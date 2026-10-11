import threading

import numpy as np
import sounddevice as sd

FS = 48000
MARIME_BUFFER = 4096
MARIME_BLOC = 1024


class Microfon:
    def __init__(self, fs: int = FS, dispozitiv=None):
        self.fs = fs
        self._buffer = np.zeros(MARIME_BUFFER, dtype=np.float32)
        self._lacat = threading.Lock()
        self._flux = sd.InputStream(
            samplerate=fs,
            channels=1,
            dtype="float32",
            blocksize=MARIME_BLOC,
            device=dispozitiv,
            callback=self._callback,
        )

    def _callback(self, indata, frames, timp, status):
        date = indata[:, 0]
        with self._lacat:
            self._buffer = np.roll(self._buffer, -len(date))
            self._buffer[-len(date):] = date

    def porneste(self):
        self._flux.start()

    def opreste(self):
        self._flux.stop()
        self._flux.close()

    def ultimul_bloc(self) -> np.ndarray:
        with self._lacat:
            return self._buffer.copy()


def listeaza_dispozitive():
    print(sd.query_devices())
