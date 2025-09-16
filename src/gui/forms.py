"""
Client form GUI component.
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

from config import (
    ROZMOWA_OPCJE, style_opcje, nieruchomosci_opcje, rocznica_przedzialy,
    godziny_opcje, STATUS_KOLORY
)


class ClientForm:
    """Form for entering client information."""

    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window

        # Create form frame
        self.frame = tk.Frame(parent, bg="#fcae61", bd=0, highlightthickness=3)

        # Form fields storage
        self.entries = {}
        self.nieruchomosc_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.styl_var = tk.StringVar()
        self.contact_date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        self.ponowny_kontakt_var = tk.StringVar()
        self.miejscowosc_entry = None
        self.dzieci_var = tk.StringVar(value="Nie")
        self.godzina_kontaktu_var = tk.StringVar(value="12:00")
        self.rozmowa_var = tk.StringVar(value=ROZMOWA_OPCJE[0])

        self._create_form()

    def _create_form(self):
        """Create the form layout."""
        # Basic fields
        fields = ["Imię i nazwisko", "Telefon", "Email", "Rocznica majątku", "Polisa życiowa", "Notatki"]

        for i, field in enumerate(fields):
            tk.Label(self.frame, text=field + ":", bg="#fcae61", font=("Arial", 10)).grid(
                row=i, column=0, sticky="w", padx=8, pady=3
            )

            if field == "Rocznica majątku":
                self.rocznica_var = tk.StringVar()
                rocznica_dropdown = ttk.Combobox(
                    self.frame, textvariable=self.rocznica_var,
                    values=rocznica_przedzialy, state="readonly", width=20
                )
                rocznica_dropdown.grid(row=i, column=1, pady=3)
                rocznica_dropdown.set(rocznica_przedzialy[0])
                self.entries[field] = rocznica_dropdown
            else:
                entry = tk.Entry(self.frame, width=22, bg="white")
                entry.grid(row=i, column=1, pady=3)
                self.entries[field] = entry

        # Property field
        tk.Label(self.frame, text="Nieruchomość:", bg="#fcae61", font=("Arial", 10)).grid(
            row=6, column=0, sticky="w", padx=8, pady=3
        )
        nieruchomosc_dropdown = ttk.Combobox(
            self.frame, textvariable=self.nieruchomosc_var,
            values=nieruchomosci_opcje, state="readonly", width=20
        )
        nieruchomosc_dropdown.grid(row=6, column=1, pady=3)
        nieruchomosc_dropdown.set(nieruchomosci_opcje[0])

        # Client status
        tk.Label(self.frame, text="Status klienta:", bg="#fcae61", font=("Arial", 10)).grid(
            row=0, column=2, sticky="w", padx=8
        )
        status_dropdown = ttk.Combobox(
            self.frame, textvariable=self.status_var,
            values=list(STATUS_KOLORY.keys()),
            state="readonly", width=18
        )
        status_dropdown.grid(row=0, column=3, pady=3)
        status_dropdown.set("Obecny klient z polisą")

        # Contact date
        tk.Label(self.frame, text="Data kontaktu:", bg="#fcae61", font=("Arial", 10)).grid(
            row=1, column=2, sticky="w", padx=8
        )
        contact_date_entry = tk.Entry(
            self.frame, textvariable=self.contact_date_var, width=16, bg="white"
        )
        contact_date_entry.grid(row=1, column=3, pady=3)

        # Follow-up contact
        tk.Label(self.frame, text="Ponowny kontakt:", bg="#fcae61", font=("Arial", 10)).grid(
            row=2, column=2, sticky="w", padx=8
        )
        try:
            ponowny_kontakt_picker = DateEntry(
                self.frame, textvariable=self.ponowny_kontakt_var,
                date_pattern="yyyy-mm-dd", locale="pl", firstweekday="monday", width=14
            )
        except Exception:
            ponowny_kontakt_picker = DateEntry(
                self.frame, textvariable=self.ponowny_kontakt_var,
                date_pattern="yyyy-mm-dd", width=14
            )
        ponowny_kontakt_picker.grid(row=2, column=3, pady=3)

        # Location
        tk.Label(self.frame, text="Miejscowość:", bg="#fcae61", font=("Arial", 10)).grid(
            row=3, column=2, sticky="w", padx=8
        )
        self.miejscowosc_entry = tk.Entry(self.frame, width=16, bg="white")
        self.miejscowosc_entry.grid(row=3, column=3, pady=3)

        # Children
        tk.Label(self.frame, text="Czy posiada dzieci:", bg="#fcae61", font=("Arial", 10)).grid(
            row=4, column=2, sticky="w", padx=8
        )
        dzieci_dropdown = ttk.Combobox(
            self.frame, textvariable=self.dzieci_var,
            values=["Tak", "Nie"], state="readonly", width=12
        )
        dzieci_dropdown.grid(row=4, column=3, pady=3)

        # Contact time
        tk.Label(self.frame, text="Godzina kontaktu:", bg="#fcae61", font=("Arial", 10)).grid(
            row=5, column=2, sticky="w", padx=8
        )
        godzina_kontaktu_combo = ttk.Combobox(
            self.frame, textvariable=self.godzina_kontaktu_var,
            values=godziny_opcje, width=12, state="readonly"
        )
        godzina_kontaktu_combo.grid(row=5, column=3, pady=3)

        # Conversation style
        tk.Label(self.frame, text="Styl rozmowy:", bg="#fcae61", font=("Arial", 10)).grid(
            row=6, column=2, sticky="w", padx=8
        )
        styl_dropdown = ttk.Combobox(
            self.frame, textvariable=self.styl_var,
            values=style_opcje, state="readonly", width=18
        )
        styl_dropdown.grid(row=6, column=3, pady=3)
        styl_dropdown.set(style_opcje[0])

        # Conversation status
        tk.Label(self.frame, text="Status rozmowy:", bg="#fcae61", font=("Arial", 10, "bold")).grid(
            row=7, column=0, sticky="w", padx=8, pady=3
        )
        rozmowa_dropdown = ttk.Combobox(
            self.frame, textvariable=self.rozmowa_var,
            values=ROZMOWA_OPCJE, state="readonly", width=20
        )
        rozmowa_dropdown.grid(row=7, column=1, pady=3)

        # Buttons
        button_frame = tk.Frame(self.frame, bg="#fcae61")
        button_frame.grid(row=9, column=0, columnspan=4, pady=18)

        btn_save = tk.Button(
            button_frame, text="Zapisz", bg="#ffe0b3", font=("Arial", 11), width=12,
            command=self.main_window.save_client
        )
        btn_save.grid(row=0, column=0, padx=12)

        btn_delete = tk.Button(
            button_frame, text="Usuń", bg="#ff9999", font=("Arial", 11), width=12,
            command=self.main_window.delete_client
        )
        btn_delete.grid(row=0, column=1, padx=12)

    def get_client_data(self):
        """Get client data from form fields."""
        return {
            "imie_nazwisko": self.entries["Imię i nazwisko"].get(),
            "telefon": self.entries["Telefon"].get(),
            "email": self.entries["Email"].get(),
            "rocznica_majatku": self.rocznica_var.get(),
            "polisa_zyciowa": self.entries["Polisa życiowa"].get(),
            "notatki": self.entries["Notatki"].get(),
            "nieruchomosc": self.nieruchomosc_var.get(),
            "status_klienta": self.status_var.get(),
            "styl_rozmowy": self.styl_var.get(),
            "data_kontaktu": self.contact_date_var.get(),
            "ponowny_kontakt": self.ponowny_kontakt_var.get(),
            "godzina_kontaktu": self.godzina_kontaktu_var.get(),
            "miejscowosc": self.miejscowosc_entry.get(),
            "czy_posiada_dzieci": self.dzieci_var.get(),
            "status_rozmowy": self.rozmowa_var.get()
        }

    def reset_form(self):
        """Reset form to default values."""
        for entry in self.entries.values():
            try:
                entry.delete(0, tk.END)
            except Exception:
                entry.set("")

        self.nieruchomosc_var.set(nieruchomosci_opcje[0])
        self.status_var.set("Obecny klient z polisą")
        self.styl_var.set(style_opcje[0])
        self.contact_date_var.set(datetime.today().strftime("%Y-%m-%d"))
        self.ponowny_kontakt_var.set("")
        self.miejscowosc_entry.delete(0, tk.END)
        self.dzieci_var.set("Nie")
        self.godzina_kontaktu_var.set("12:00")
        self.rozmowa_var.set(ROZMOWA_OPCJE[0])

    def populate_form(self, client_data):
        """Populate form with client data."""
        self.entries["Imię i nazwisko"].insert(0, client_data.get("Imię i nazwisko", ""))
        self.entries["Telefon"].insert(0, client_data.get("Telefon", ""))
        self.entries["Email"].insert(0, client_data.get("Email", ""))
        self.rocznica_var.set(client_data.get("Rocznica majątku", ""))
        self.entries["Polisa życiowa"].insert(0, client_data.get("Polisa życiowa", ""))
        self.entries["Notatki"].insert(0, client_data.get("Notatki", ""))
        self.nieruchomosc_var.set(client_data.get("Nieruchomość", ""))
        self.status_var.set(client_data.get("Status klienta", ""))
        self.styl_var.set(client_data.get("Styl rozmowy", ""))
        self.contact_date_var.set(client_data.get("Data kontaktu", ""))
        self.ponowny_kontakt_var.set(client_data.get("Ponowny kontakt", ""))
        self.godzina_kontaktu_var.set(client_data.get("Godzina kontaktu", ""))
        self.miejscowosc_entry.insert(0, client_data.get("Miejscowość", ""))
        self.dzieci_var.set(client_data.get("Czy posiada dzieci", ""))
        self.rozmowa_var.set(client_data.get("Status rozmowy", ""))
