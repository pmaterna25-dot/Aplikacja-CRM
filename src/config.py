"""
Configuration and constants for the Materna CRM application.
"""

# Excel file configuration
EXCEL_FILE = "materna_ind.xlsx"

# Status colors for client status
STATUS_KOLORY = {
    "Obecny klient z polisą": "#90EE90",
    "Hotcall": "#FFD700",
    "Hotlead": "#FFA07A",
    "Lead umówiony": "#ADD8E6",
    "Polecenie": "#87CEFA",
    "Grupówka": "#DDA0DD",
    "Przepisana Polisa": "#FFA500"
}

# Conversation status options
ROZMOWA_OPCJE = [
    "Odebrany",
    "Nieodebrany",
    "Umówione spotkanie",
    "Niezainteresowany",
    "Ponowny kontakt",
    "Potencjał"
]

# Conversation status colors
ROZMOWA_KOLORY = {
    "Ponowny kontakt": "#99c9ff",
    "Potencjał": "#90ee90",
    "Niezainteresowany": "#ffcccc",
    "Nieodebrany": "#e7e7e7"
}

# Asset anniversary intervals
rocznica_przedzialy = [
    "Styczeń 1–15", "Styczeń 16–31", "Luty 1–14", "Luty 15–28",
    "Marzec 1–15", "Marzec 16–31", "Kwiecień 1–15", "Kwiecień 16–30",
    "Maj 1–15", "Maj 16–31", "Czerwiec 1–15", "Czerwiec 16–30",
    "Lipiec 1–15", "Lipiec 16–31", "Sierpień 1–15", "Sierpień 16–31",
    "Wrzesień 1–15", "Wrzesień 16–30", "Październik 1–15", "Październik 16–31",
    "Listopad 1–15", "Listopad 16–30", "Grudzień 1–15", "Grudzień 16–31"
]

# Property options
nieruchomosci_opcje = ["Dom", "Mieszkanie", "Więcej", "Brak informacji"]

# Conversation style options
style_opcje = [
    "Swobodny / Koleżeński", "Neutralny / Uprzejmy", "Formalny / Sztywny",
    "Z dystansem / Ostrożny", "Rodzinny / Znajomy", "Młodzieżowy / Na Ty",
    "Senior / Z szacunkiem"
]

# Contact hours options
godziny_opcje = [f"{h:02d}:{m:02d}" for h in range(8, 21) for m in (0, 30)]

# Table columns
columns = [
    "#", "Imię i nazwisko", "Telefon", "Email", "Rocznica majątku", "Polisa życiowa", "Notatki",
    "Nieruchomość", "Status klienta", "Styl rozmowy", "Data kontaktu", "Ponowny kontakt",
    "Godzina kontaktu", "Miejscowość", "Czy posiada dzieci", "Status rozmowy"
]

# Background styles
STYLES = [
    ("Kosmici", "kosmici.jpg"),
    ("Las", "las.jpg"),
    ("Góry", "gory.jpg"),
    ("Japonia", "japonia.jpg"),
    ("Dark soulsy", "darksouls.jpg"),
    ("Potwór morski", "potwor.jpg"),
]

# Window dimensions
WINDOW_W = 1184
WINDOW_H = 692
