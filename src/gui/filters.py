"""
Filter panel GUI component.
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta

from config import rocznica_przedzialy, nieruchomosci_opcje


class FilterPanel:
    """Filter panel for client data."""

    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window

        # Create filter frame
        self.frame = tk.Frame(parent, bg="#e6f2ff", bd=2, relief="solid",
                             highlightbackground="black", highlightthickness=2)

        # Filter variables
        self.filter_majatkowy_var = tk.StringVar()
        self.filter_nieruchomosc_var = tk.StringVar()
        self.filter_data_var = tk.StringVar()
        self.filter_miejscowosc_var = tk.StringVar()
        self.filter_imie_var = tk.StringVar()
        self.filter_telefon_var = tk.StringVar()
        self.filtr_typ_var = tk.StringVar(value="Konkretny dzień")
        self.filtr_data_kontaktu_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))

        self._create_filters()

    def _create_filters(self):
        """Create filter UI components."""
        # First row of filters
        tk.Label(self.frame, text="Filtr majątkowy:", font=("Arial", 10), bg="#e6f2ff").grid(
            row=0, column=0, padx=6, pady=3
        )
        filter_majatkowy_menu = ttk.Combobox(
            self.frame, textvariable=self.filter_majatkowy_var,
            values=rocznica_przedzialy, state="readonly", width=14
        )
        filter_majatkowy_menu.grid(row=0, column=1)

        tk.Label(self.frame, text="Filtr nieruchomości:", font=("Arial", 10), bg="#e6f2ff").grid(
            row=0, column=2, padx=6
        )
        filter_nieruchomosc_menu = ttk.Combobox(
            self.frame, textvariable=self.filter_nieruchomosc_var,
            values=nieruchomosci_opcje, state="readonly", width=12
        )
        filter_nieruchomosc_menu.grid(row=0, column=3)

        tk.Label(self.frame, text="Filtr daty kontaktu:", font=("Arial", 10), bg="#e6f2ff").grid(
            row=0, column=4, padx=6
        )
        try:
            filter_data_picker = DateEntry(
                self.frame, textvariable=self.filter_data_var,
                date_pattern="yyyy-mm-dd", locale="pl", width=10
            )
        except Exception:
            filter_data_picker = DateEntry(
                self.frame, textvariable=self.filter_data_var,
                date_pattern="yyyy-mm-dd", width=10
            )
        filter_data_picker.grid(row=0, column=5)

        tk.Label(self.frame, text="Filtr miejscowości:", font=("Arial", 10), bg="#e6f2ff").grid(
            row=0, column=6, padx=6
        )
        filter_miejscowosc_entry = tk.Entry(
            self.frame, textvariable=self.filter_miejscowosc_var, width=12
        )
        filter_miejscowosc_entry.grid(row=0, column=7)

        # Second row of filters
        tk.Label(self.frame, text="Filtr imię/nazwisko:", font=("Arial", 10), bg="#e6f2ff").grid(
            row=1, column=0, padx=6
        )
        filter_imie_entry = tk.Entry(self.frame, textvariable=self.filter_imie_var, width=12)
        filter_imie_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Filtr tel.:", font=("Arial", 10), bg="#e6f2ff").grid(
            row=1, column=2, padx=6
        )
        filter_telefon_entry = tk.Entry(self.frame, textvariable=self.filter_telefon_var, width=12)
        filter_telefon_entry.grid(row=1, column=3)

        tk.Label(self.frame, text="Ponowny kontakt:", font=("Arial", 10), bg="#e6f2ff").grid(
            row=1, column=4, padx=10
        )
        filtr_typ_menu = ttk.Combobox(
            self.frame, textvariable=self.filtr_typ_var,
            values=["Konkretny dzień", "Grupa <->", "Ten tydzień", "Ten miesiąc"],
            state="readonly", width=14
        )
        filtr_typ_menu.grid(row=1, column=5)

        try:
            filtr_data_kontaktu_picker = DateEntry(
                self.frame, textvariable=self.filtr_data_kontaktu_var,
                date_pattern="yyyy-mm-dd", locale="pl", width=10
            )
        except Exception:
            filtr_data_kontaktu_picker = DateEntry(
                self.frame, textvariable=self.filtr_data_kontaktu_var,
                date_pattern="yyyy-mm-dd", width=10
            )
        filtr_data_kontaktu_picker.grid(row=1, column=6, padx=8)

        # Filter buttons
        btn_filter = tk.Button(
            self.frame, text="Filtruj", command=self._apply_filter,
            bg="#cce5ff", font=("Arial", 10)
        )
        btn_filter.grid(row=2, column=0, padx=6, pady=3)

        btn_filtruj_kontakt = tk.Button(
            self.frame, text="Filtruj ponowny", command=self._apply_followup_filter,
            bg="#cce5ff", font=("Arial", 10)
        )
        btn_filtruj_kontakt.grid(row=2, column=1, padx=10, pady=3)

        btn_clear_filters = tk.Button(
            self.frame, text="Wyczyść filtry", command=self._clear_filters,
            bg="#f2f2f2", font=("Arial", 10)
        )
        btn_clear_filters.grid(row=2, column=2, padx=10, pady=3)

        # Statistics and style section
        frame_stats = tk.Frame(self.frame, bg="#e6f2ff")
        # Labels are managed by main window, just add buttons here
        btn_statystyki = tk.Button(
            frame_stats, text="Statystyki", font=("Arial", 10), width=10,
            command=self.main_window.show_statistics_popup
        )
        btn_statystyki.pack(side="left", padx=8)
        frame_stats.grid(row=2, column=3, padx=16, pady=3, sticky="w")

        frame_style = tk.Frame(self.frame, bg="#e6f2ff")
        tk.Label(frame_style, text="Styl aplikacji:", font=("Arial", 10), bg="#e6f2ff").pack(side="left", padx=4)
        btn_style = tk.Button(
            frame_style, text="Wybierz", font=("Arial", 10), width=8,
            command=self.main_window.show_style_selector
        )
        btn_style.pack(side="left", padx=4)
        frame_style.grid(row=2, column=4, padx=16, pady=3, sticky="e")

    def _apply_filter(self):
        """Apply filters to the client table."""
        # Clear current table
        for item in self.main_window.client_table.tree.get_children():
            self.main_window.client_table.tree.delete(item)

        try:
            clients = self.main_window.excel_manager.load_all_clients()

            for client in clients:
                if self._matches_filters(client):
                    self.main_window.client_table.add_client(client)

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Błąd", f"Nie udało się przefiltrować danych:\n{e}")

    def _matches_filters(self, client):
        """Check if client matches current filters."""
        # Asset anniversary filter
        if self.filter_majatkowy_var.get() and client.rocznica_majatku != self.filter_majatkowy_var.get():
            return False

        # Property filter
        if self.filter_nieruchomosc_var.get() and client.nieruchomosc != self.filter_nieruchomosc_var.get():
            return False

        # Contact date filter
        if self.filter_data_var.get() and client.data_kontaktu != self.filter_data_var.get():
            return False

        # Location filter
        if (self.filter_miejscowosc_var.get() and
            self.filter_miejscowosc_var.get().lower() not in client.miejscowosc.lower()):
            return False

        # Name filter
        if (self.filter_imie_var.get() and
            self.filter_imie_var.get().lower() not in client.imie_nazwisko.lower()):
            return False

        # Phone filter
        if (self.filter_telefon_var.get() and
            self.filter_telefon_var.get() not in client.telefon):
            return False

        return True

    def _apply_followup_filter(self):
        """Apply follow-up contact filters."""
        try:
            data_wybrana = datetime.strptime(self.filtr_data_kontaktu_var.get(), "%Y-%m-%d").date()
        except Exception:
            from tkinter import messagebox
            messagebox.showwarning("Data", "Wybierz poprawną datę.")
            return

        # Clear current table
        for item in self.main_window.client_table.tree.get_children():
            self.main_window.client_table.tree.delete(item)

        try:
            clients = self.main_window.excel_manager.load_all_clients()

            for client in clients:
                if not client.ponowny_kontakt:
                    continue

                try:
                    data_kontaktu = datetime.strptime(client.ponowny_kontakt, "%Y-%m-%d").date()
                except Exception:
                    continue

                if self._matches_followup_filter(data_kontaktu, data_wybrana):
                    self.main_window.client_table.add_client(client)

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Błąd filtra", f"Nie udało się przefiltrować danych:\n{e}")

    def _matches_followup_filter(self, contact_date, selected_date):
        """Check if contact date matches follow-up filter criteria."""
        typ = self.filtr_typ_var.get()

        if typ == "Konkretny dzień":
            return contact_date == selected_date
        elif typ == "Grupa <->":
            return abs((contact_date - selected_date).days) <= 5
        elif typ == "Ten tydzień":
            start = selected_date - timedelta(days=selected_date.weekday())
            end = start + timedelta(days=6)
            return start <= contact_date <= end
        elif typ == "Ten miesiąc":
            return (contact_date.month == selected_date.month and
                   contact_date.year == selected_date.year)

        return False

    def _clear_filters(self):
        """Clear all filters."""
        self.filter_majatkowy_var.set("")
        self.filter_nieruchomosc_var.set("")
        self.filter_data_var.set("")
        self.filter_miejscowosc_var.set("")
        self.filter_imie_var.set("")
        self.filter_telefon_var.set("")
        self.filtr_typ_var.set("Konkretny dzień")
        self.filtr_data_kontaktu_var.set(datetime.today().strftime("%Y-%m-%d"))

        # Reload all clients
        self.main_window._load_all_clients()
