# Acordor pentru trompeta (Si bemol)

Aplicatie desktop in Python care asculta trompeta prin microfon si arata in timp real
ce nota canta utilizatorul si cat de aproape este de acordaj.

## Ce face

- afiseaza nota scrisa (cum o citeste trompetistul) si nota reala care suna
- afiseaza frecventa in Hz si abaterea in centi (-50 ... +50)
- indicator vizual: verde (+-5 centi), portocaliu (+-15), rosu (mai mult)
- A4 reglabil (430-450 Hz)

## Structura

| Fisier | Rol |
|---|---|
| `audio.py` | captura de la microfon, buffer glisant de 4096 esantioane |
| `pitch.py` | frecventa fundamentala (YIN), nivel RMS, netezire cu mediana |
| `notes.py` | Hz -> nota + centi, transpozitie Si bemol |
| `gui.py` | fereastra tkinter, doar afiseaza |
| `main.py` | porneste aplicatia si leaga modulele |

## Flux

1. Microfonul trimite blocuri audio (44100 Hz, mono) intr-un buffer.
2. La ~40 ms, interfata cere o nota de la `main.py`.
3. Daca volumul (RMS) e sub prag, nu se canta nimic.
4. YIN gaseste frecventa fundamentala (150-1100 Hz).
5. Mediana ultimelor 5 valori elimina salturile.
6. `midi = 69 + 12*log2(f/A4)`, nota = `round(midi)`, `centi = 1200*log2(f/f_ideala)`.
7. Nota scrisa = nota reala + 2 semitonuri.

YIN in loc de FFT: trompeta are armonici puternice, iar varful din FFT poate pica pe
armonica 2 sau 3 si da o octava gresita. YIN cauta periodicitatea si gaseste fundamentala.

## Rulare

```
pip install -r requirements.txt
python main.py
```

## Teste

```
pytest
```

## Probleme frecvente

- **Nu detecteaza nimic:** scade `PRAG_RMS` in `main.py` sau apropie-te de microfon.
- **Acul sare haotic:** canta la 30-50 cm de laptop si dezactiveaza imbunatatirile audio din setarile de sunet.
- **Eroare la microfon:** schimba `FS` in `audio.py` la 48000 sau alege dispozitivul cu `listeaza_dispozitive()`.

## Limitari

- o singura nota o data (nu acorduri)
- sensibil la zgomot de fond puternic
- plaja detectata: 150-1100 Hz
