import math
from dataclasses import dataclass

NUME_NOTE = ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]

A4_IMPLICIT = 440.0

# trompeta in Si bemol: nota scrisa = nota care suna + 2 semitonuri
TRANSPOZITIE_SIB = 2


@dataclass
class Nota:
    hz: float
    hz_ideal: float
    centi: float       # intre -50 si +50
    nume_real: str     # nota care suna, ex: "La#3"
    nume_scris: str    # nota din partitura, ex: "Do4"


def midi_la_nume(midi: int) -> str:
    octava = midi // 12 - 1
    return f"{NUME_NOTE[midi % 12]}{octava}"


def hz_la_nota(hz: float, a4: float = A4_IMPLICIT) -> Nota:
    if hz <= 0:
        raise ValueError("Frecventa trebuie sa fie pozitiva")

    midi_exact = 69 + 12 * math.log2(hz / a4)
    midi = round(midi_exact)

    hz_ideal = a4 * 2 ** ((midi - 69) / 12)
    centi = 1200 * math.log2(hz / hz_ideal)

    return Nota(
        hz=hz,
        hz_ideal=hz_ideal,
        centi=centi,
        nume_real=midi_la_nume(midi),
        nume_scris=midi_la_nume(midi + TRANSPOZITIE_SIB),
    )
