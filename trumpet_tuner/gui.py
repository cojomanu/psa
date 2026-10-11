import tkinter as tk

INTERVAL_MS = 40
TOLERANTA_OK = 5          # centi
TOLERANTA_APROAPE = 15

VERDE = "#2e9e4f"
PORTOCALIU = "#e0a21b"
ROSU = "#d64545"
GRI = "#8a8a8a"

LATIME_SCALA = 400
MARGINE = 20


class FereastraAcordor:
    def __init__(self, root: tk.Tk, ia_nota):
        self.root = root
        self.ia_nota = ia_nota

        root.title("Acordor trompeta (Si♭)")
        root.geometry("460x400")
        root.resizable(False, False)

        tk.Label(root, text="Nota scrisa", font=("Helvetica", 11)).pack(pady=(15, 0))
        self.nota_mare = tk.Label(root, text="-", font=("Helvetica", 72, "bold"))
        self.nota_mare.pack()

        self.nota_reala = tk.Label(root, text="", font=("Helvetica", 12))
        self.nota_reala.pack()

        self.hz = tk.Label(root, text="", font=("Helvetica", 12))
        self.hz.pack()

        self._construieste_scala()

        self.stare = tk.Label(root, text="Canta o nota", font=("Helvetica", 16, "bold"))
        self.stare.pack(pady=5)

        cadru = tk.Frame(root)
        cadru.pack(pady=10)
        tk.Label(cadru, text="A4 =").pack(side="left")
        self.a4 = tk.IntVar(value=440)
        tk.Spinbox(cadru, from_=430, to=450, width=5, textvariable=self.a4).pack(side="left")
        tk.Label(cadru, text="Hz").pack(side="left")

    def _construieste_scala(self):
        self.scala = tk.Canvas(self.root, width=LATIME_SCALA + 2 * MARGINE, height=70,
                               highlightthickness=0)
        self.scala.pack(pady=10)

        self.scala.create_rectangle(self._x(-TOLERANTA_OK), 20, self._x(TOLERANTA_OK), 50,
                                    fill="#cfeedd", outline="")
        self.scala.create_rectangle(self._x(-50), 20, self._x(50), 50, outline="black")

        for centi in (-50, -25, 0, 25, 50):
            x = self._x(centi)
            self.scala.create_line(x, 50, x, 56)
            self.scala.create_text(x, 64, text=str(centi), font=("Helvetica", 9))

        self.ac = self.scala.create_line(self._x(0), 12, self._x(0), 58, width=4, fill=GRI)

    def _x(self, centi: float) -> float:
        return MARGINE + (centi + 50) / 100 * LATIME_SCALA

    def _culoare(self, centi: float) -> str:
        if abs(centi) <= TOLERANTA_OK:
            return VERDE
        if abs(centi) <= TOLERANTA_APROAPE:
            return PORTOCALIU
        return ROSU

    def _arata_nota(self, nota):
        culoare = self._culoare(nota.centi)
        self.nota_mare.config(text=nota.nume_scris, fg=culoare)
        self.nota_reala.config(text=f"Suna: {nota.nume_real}")
        self.hz.config(text=f"{nota.hz:.1f} Hz  |  {nota.centi:+.0f} centi")

        centi = max(-50, min(50, nota.centi))
        x = self._x(centi)
        self.scala.coords(self.ac, x, 12, x, 58)
        self.scala.itemconfig(self.ac, fill=culoare)

        if abs(nota.centi) <= TOLERANTA_OK:
            text = "Acordat ✓"
        elif nota.centi > 0:
            text = "Prea sus"
        else:
            text = "Prea jos"
        self.stare.config(text=text, fg=culoare)

    def _arata_inactiv(self):
        self.nota_mare.config(text="-", fg=GRI)
        self.nota_reala.config(text="")
        self.hz.config(text="")
        x = self._x(0)
        self.scala.coords(self.ac, x, 12, x, 58)
        self.scala.itemconfig(self.ac, fill=GRI)
        self.stare.config(text="Canta o nota", fg=GRI)

    def _citeste_a4(self) -> int:
        try:
            return self.a4.get()
        except tk.TclError:   # camp gol sau text invalid
            return 440

    def _actualizeaza(self):
        nota = self.ia_nota(self._citeste_a4())
        if nota is None:
            self._arata_inactiv()
        else:
            self._arata_nota(nota)
        self.root.after(INTERVAL_MS, self._actualizeaza)

    def porneste(self):
        self._actualizeaza()
        self.root.mainloop()
