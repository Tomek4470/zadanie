# Generator Haseł 🔐

Desktopowa aplikacja do generowania bezpiecznych haseł, napisana w Pythonie z interfejsem graficznym (tkinter).

---

## Wymagania

| Wymaganie | Wersja |
|-----------|--------|
| Python    | ≥ 3.10 |
| pyperclip | ≥ 1.8  |

> **Uwaga:** `tkinter` jest wbudowany w Pythona — nie wymaga osobnej instalacji.

---

## Instalacja i uruchomienie

### 1. Sprawdź, czy masz zainstalowanego Pythona

Otwórz **PowerShell** lub **Wiersz poleceń** i wpisz:

```powershell
python --version
```

Jeśli Python nie jest zainstalowany, pobierz go ze strony: https://www.python.org/downloads/

---

### 2. Zainstaluj wymagane biblioteki

W katalogu projektu uruchom:

```powershell
pip install -r requirements.txt
```

---

### 3. Uruchom aplikację

```powershell
python password_generator.py
```

Otworzy się okno aplikacji.

---

## Jak używać

1. **Przesuń suwak** lub wpisz liczbę w pole obok, aby wybrać długość hasła (4–64 znaki).
2. **Zaznacz typy znaków**, które ma zawierać hasło:
   - Wielkie litery A–Z
   - Małe litery a–z
   - Cyfry 0–9
   - Symbole (!@#…)
3. Kliknij przycisk **✦ Generuj hasło**.
4. Pojawi się Twoje hasło wraz z informacją o jego sile.
5. Kliknij **📋 Kopiuj**, aby skopiować hasło do schowka.

---

## Struktura projektu

```
2.1-generator-4tc-2-tomasz-g/
├── password_generator.py   # Główny plik aplikacji
├── requirements.txt        # Zależności Python
├── README.md               # Ten plik
└── Obserwacje/             # Notatki obserwacyjne
```

---

## Bezpieczeństwo

Hasła generowane są za pomocą modułu `secrets` — kryptograficznie bezpiecznego generatora liczb losowych wbudowanego w Pythona.
