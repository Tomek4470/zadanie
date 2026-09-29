"""
Generator Haseł – aplikacja desktopowa (Python + tkinter)
"""
import tkinter as tk
from tkinter import messagebox
import secrets
import string

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

# ── Paleta kolorów ──────────────────────────────────────────────
BG          = "#0f0f1a"
CARD        = "#1a1a2e"
ACCENT      = "#7c3aed"
ACCENT_HOV  = "#5b21b6"
TEXT        = "#e2e8f0"
TEXT_DIM    = "#94a3b8"
INPUT_BG    = "#16213e"
SUCCESS     = "#22c55e"
BORDER      = "#2d2d4e"
PURPLE_LIGHT= "#a78bfa"

# ── Zbiory znaków ───────────────────────────────────────────────
UPPER   = string.ascii_uppercase
LOWER   = string.ascii_lowercase
DIGITS  = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"


def evaluate_strength(pwd: str) -> tuple[str, str]:
    """Zwraca (etykieta, kolor) opisujące siłę hasła."""
    n = len(pwd)
    variety = sum([
        any(c in UPPER   for c in pwd),
        any(c in LOWER   for c in pwd),
        any(c in DIGITS  for c in pwd),
        any(c in SYMBOLS for c in pwd),
    ])
    score = variety
    if n >= 8:  score += 1
    if n >= 12: score += 1
    if n >= 20: score += 1

    if score <= 2:  return "Słabe",         "#ef4444"
    if score <= 4:  return "Średnie",        "#f97316"
    if score <= 5:  return "Mocne",          "#eab308"
    return              "Bardzo mocne",  SUCCESS


def make_password(length: int, upper: bool, lower: bool,
                  digits: bool, symbols: bool) -> str:
    alphabet  = ""
    mandatory = []

    if upper:   alphabet += UPPER;   mandatory.append(secrets.choice(UPPER))
    if lower:   alphabet += LOWER;   mandatory.append(secrets.choice(LOWER))
    if digits:  alphabet += DIGITS;  mandatory.append(secrets.choice(DIGITS))
    if symbols: alphabet += SYMBOLS; mandatory.append(secrets.choice(SYMBOLS))

    if not alphabet:
        raise ValueError("Zaznacz co najmniej jeden typ znaków.")

    rest = [secrets.choice(alphabet) for _ in range(length - len(mandatory))]
    pool = mandatory + rest
    secrets.SystemRandom().shuffle(pool)
    return "".join(pool)


# ════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generator Haseł 🔐")
        self.resizable(False, False)
        self.configure(bg=BG)

        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = 540, 660
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self._current_pwd = ""
        self._build()

    # ─────────────────────────────────────────────────────────────
    def _build(self):
        # ── Nagłówek ─────────────────────────────────────────────
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", pady=(30, 10))

        tk.Label(hdr, text="🔐", font=("Segoe UI Emoji", 40), bg=BG).pack()
        tk.Label(hdr, text="Generator Haseł",
                 font=("Segoe UI", 22, "bold"), fg=TEXT, bg=BG).pack(pady=(4, 0))
        tk.Label(hdr, text="Twórz silne, bezpieczne hasła w jednej chwili",
                 font=("Segoe UI", 10), fg=TEXT_DIM, bg=BG).pack()

        # ── Karta ustawień ────────────────────────────────────────
        card = tk.Frame(self, bg=CARD,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", padx=36, pady=16)
        inner = tk.Frame(card, bg=CARD)
        inner.pack(fill="x", padx=24, pady=20)

        # -- Długość -------------------------------------------------
        tk.Label(inner, text="Liczba znaków",
                 font=("Segoe UI", 10, "bold"), fg=TEXT_DIM, bg=CARD,
                 anchor="w").pack(fill="x")

        ctrl = tk.Frame(inner, bg=CARD)
        ctrl.pack(fill="x", pady=(6, 16))

        self.length_var = tk.IntVar(value=16)

        slider = tk.Scale(ctrl, from_=4, to=64, orient="horizontal",
                          variable=self.length_var,
                          bg=CARD, fg=PURPLE_LIGHT,
                          troughcolor=INPUT_BG,
                          activebackground=ACCENT,
                          highlightthickness=0,
                          showvalue=False,
                          sliderlength=20,
                          length=340)
        slider.pack(side="left")

        entry = tk.Entry(ctrl, textvariable=self.length_var,
                         width=4, justify="center",
                         font=("Segoe UI", 13, "bold"),
                         fg=TEXT, bg=INPUT_BG,
                         insertbackground=TEXT,
                         relief="flat",
                         highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=ACCENT)
        entry.pack(side="left", padx=(12, 0))
        entry.bind("<Return>",   lambda e: self._clamp_length())
        entry.bind("<FocusOut>", lambda e: self._clamp_length())

        # -- Opcje znaków -------------------------------------------
        tk.Label(inner, text="Zawiera",
                 font=("Segoe UI", 10, "bold"), fg=TEXT_DIM, bg=CARD,
                 anchor="w").pack(fill="x")

        self.opt_upper   = tk.BooleanVar(value=True)
        self.opt_lower   = tk.BooleanVar(value=True)
        self.opt_digits  = tk.BooleanVar(value=True)
        self.opt_symbols = tk.BooleanVar(value=False)

        options = [
            ("Wielkie litery  A–Z", self.opt_upper),
            ("Małe litery  a–z",    self.opt_lower),
            ("Cyfry  0–9",          self.opt_digits),
            ("Symbole  !@#…",       self.opt_symbols),
        ]

        opts_frame = tk.Frame(inner, bg=CARD)
        opts_frame.pack(fill="x", pady=(8, 0))

        for label, var in options:
            row = tk.Frame(opts_frame, bg=CARD)
            row.pack(fill="x", pady=2)

            cb = tk.Checkbutton(
                row,
                variable=var,
                bg=CARD,
                activebackground=CARD,
                # Na Windows NIE ustawiamy selectcolor – pozwalamy
                # systemowi renderować ptaszek natywnie (czytelnie).
                fg=TEXT,
                activeforeground=TEXT,
                cursor="hand2",
                relief="flat",
            )
            cb.pack(side="left")
            tk.Label(row, text=label,
                     font=("Segoe UI", 10), fg=TEXT, bg=CARD).pack(side="left")

        # ── Przycisk generowania ──────────────────────────────────
        btn_wrap = tk.Frame(self, bg=BG)
        btn_wrap.pack(fill="x", padx=36, pady=(0, 12))

        self.btn_gen = tk.Button(
            btn_wrap,
            text="✦  Generuj hasło",
            font=("Segoe UI", 12, "bold"),
            fg="white", bg=ACCENT,
            activeforeground="white", activebackground=ACCENT_HOV,
            relief="flat", bd=0,
            padx=20, pady=12,
            cursor="hand2",
            command=self._generate,
        )
        self.btn_gen.pack(fill="x")
        self.btn_gen.bind("<Enter>", lambda e: self.btn_gen.config(bg=ACCENT_HOV))
        self.btn_gen.bind("<Leave>", lambda e: self.btn_gen.config(bg=ACCENT))

        # ── Sekcja wyniku (zawsze widoczna, początkowo pusta) ─────
        res_card = tk.Frame(self, bg=CARD,
                            highlightbackground=BORDER, highlightthickness=1)
        res_card.pack(fill="x", padx=36, pady=(0, 16))
        res_inner = tk.Frame(res_card, bg=CARD)
        res_inner.pack(fill="x", padx=24, pady=16)

        tk.Label(res_inner, text="Twoje hasło to…",
                 font=("Segoe UI", 10, "bold"), fg=TEXT_DIM, bg=CARD,
                 anchor="w").pack(fill="x", pady=(0, 8))

        # Ramka z hasłem i przyciskiem kopiowania
        pw_box = tk.Frame(res_inner, bg=INPUT_BG,
                          highlightbackground=ACCENT, highlightthickness=2)
        pw_box.pack(fill="x")

        self.lbl_pwd = tk.Label(
            pw_box,
            text="— naciśnij Generuj hasło —",
            font=("Consolas", 13, "bold"),
            fg=TEXT_DIM, bg=INPUT_BG,
            wraplength=340, justify="center",
            pady=14,
        )
        self.lbl_pwd.pack(side="left", expand=True, padx=12)

        self.btn_copy = tk.Button(
            pw_box,
            text="📋 Kopiuj",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT, bg=ACCENT,
            activeforeground=TEXT, activebackground=ACCENT_HOV,
            relief="flat", bd=0,
            padx=10, pady=6,
            cursor="hand2",
            command=self._copy,
        )
        self.btn_copy.pack(side="right", padx=10, pady=10)

        # Toast + siła hasła
        bottom = tk.Frame(res_inner, bg=CARD)
        bottom.pack(fill="x", pady=(8, 0))

        self.lbl_strength = tk.Label(bottom, text="",
                                     font=("Segoe UI", 10), fg=TEXT_DIM, bg=CARD,
                                     anchor="w")
        self.lbl_strength.pack(side="left")

        self.lbl_toast = tk.Label(bottom, text="✔ Skopiowano!",
                                  font=("Segoe UI", 10), fg=SUCCESS, bg=CARD,
                                  anchor="e")
        # pakowane dynamicznie

    # ─────────────────────────────────────────────────────────────
    def _clamp_length(self):
        try:
            v = int(self.length_var.get())
            self.length_var.set(max(4, min(64, v)))
        except (tk.TclError, ValueError):
            self.length_var.set(16)

    def _generate(self):
        self._clamp_length()
        try:
            pwd = make_password(
                length  = self.length_var.get(),
                upper   = self.opt_upper.get(),
                lower   = self.opt_lower.get(),
                digits  = self.opt_digits.get(),
                symbols = self.opt_symbols.get(),
            )
        except ValueError as exc:
            messagebox.showwarning("Brak opcji", str(exc))
            return

        self._current_pwd = pwd

        # Wyświetl hasło
        self.lbl_pwd.config(text=pwd, fg=PURPLE_LIGHT)

        # Siła hasła
        label, color = evaluate_strength(pwd)
        self.lbl_strength.config(text=f"Siła hasła: {label}", fg=color)

        # Schowaj ewentualny toast
        self.lbl_toast.pack_forget()

    def _copy(self):
        if not self._current_pwd:
            return

        # Kopiuj do schowka
        if HAS_PYPERCLIP:
            pyperclip.copy(self._current_pwd)
        else:
            self.clipboard_clear()
            self.clipboard_append(self._current_pwd)
            self.update()

        self.btn_copy.config(text="✔ Skopiowano")
        self.lbl_toast.pack(side="right")
        self.after(2500, self._reset_copy)

    def _reset_copy(self):
        self.btn_copy.config(text="📋 Kopiuj")
        self.lbl_toast.pack_forget()


# ── Punkt wejścia ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
