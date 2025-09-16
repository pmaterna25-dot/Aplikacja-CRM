"""
Popup dialogs for the Materna CRM application.
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

from config import STYLES


class StatisticsPopup:
    """Statistics popup dialog."""

    def __init__(self, parent, excel_manager):
        self.parent = parent
        self.excel_manager = excel_manager

        self.popup = tk.Toplevel(parent)
        self.popup.title("Statystyki dnia")
        self.popup.geometry("430x300")
        self.popup.configure(bg="#dbefff")

        tk.Label(
            self.popup, text="Statystyki CRM", font=("Arial", 13, "bold"), bg="#dbefff"
        ).pack(pady=(15, 2))

        # Date selection frame
        frame = tk.Frame(self.popup, bg="#dbefff")
        frame.pack(pady=0)
        tk.Label(frame, text="Data:", bg="#dbefff").grid(row=0, column=0)
        self.data_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        date_picker = DateEntry(
            frame, textvariable=self.data_var, date_pattern="yyyy-mm-dd", width=10
        )
        date_picker.grid(row=0, column=1, padx=6)

        # Statistics labels
        stat_labels = ["Nowych klientów", "Odebrany", "Nieodebrany", "Umówione spotkanie",
                      "Niezainteresowany", "Ponowny kontakt", "Potencjał"]
        self.result_labels = []

        for i, txt in enumerate(stat_labels):
            lbl = tk.Label(frame, text=f"{txt}: 0", bg="#dbefff", font=("Arial", 11))
            lbl.grid(row=i+1, column=0, columnspan=2, sticky="w", padx=4, pady=2)
            self.result_labels.append(lbl)

        # Refresh button
        btn = tk.Button(
            frame, text="Pokaż", command=self._refresh_stats, font=("Arial", 10), bg="#cce5ff"
        )
        btn.grid(row=0, column=2, padx=8)

        # Initial refresh
        self._refresh_stats()

    def _refresh_stats(self):
        """Refresh statistics for selected date."""
        from models.client import Statistics

        d = self.data_var.get()
        stats = self.excel_manager.get_statistics_for_date(d)

        stat_labels = ["Nowych klientów", "Odebrany", "Nieodebrany", "Umówione spotkanie",
                      "Niezainteresowany", "Ponowny kontakt", "Potencjał"]

        if stats:
            values = [
                stats.nowi_klienci, stats.odebrany, stats.nieodebrany,
                stats.umowione_spotkanie, stats.niezainteresowany,
                stats.ponowny_kontakt, stats.potencjal
            ]
            for lbl, val in zip(self.result_labels, values):
                lbl.config(text=f"{stat_labels[self.result_labels.index(lbl)]}: {val}")
        else:
            for lbl, txt in zip(self.result_labels, stat_labels):
                lbl.config(text=f"{txt}: 0")


class StyleSelector:
    """Style selector popup dialog."""

    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback

        self.popup = tk.Toplevel(parent)
        self.popup.title("Wybierz styl aplikacji")
        self.popup.geometry("320x230")
        self.popup.transient(parent)
        self.popup.grab_set()
        self.popup.configure(bg="#e6f2ff")

        # Create style buttons
        for i, (style_name, style_file) in enumerate(STYLES):
            btn = tk.Button(
                self.popup, text=style_name, width=18, height=2, font=("Arial", 10),
                command=lambda f=style_file: self._set_style(f)
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=8)

    def _set_style(self, style_file):
        """Set the selected style and close popup."""
        self.callback(style_file)
        self.popup.destroy()


class NotePopup:
    """Note editing popup."""

    def __init__(self, parent, client_name, current_note, save_callback):
        self.parent = parent
        self.client_name = client_name
        self.current_note = current_note
        self.save_callback = save_callback

        self.popup = tk.Toplevel(parent)
        self.popup.title(f"Notatka klienta: {client_name}")
        self.popup.geometry("420x220")
        self.popup.configure(bg="#ffefcc")

        tk.Label(
            self.popup, text=f"Notatka klienta: {client_name}",
            font=("Arial", 11), bg="#ffefcc"
        ).pack(pady=10)

        self.note_text = tk.Text(
            self.popup, width=48, height=7, font=("Arial", 11), state="normal"
        )
        self.note_text.pack(pady=2)
        self.note_text.insert("1.0", current_note)

        btn = tk.Button(
            self.popup, text="Zapisz notatkę", command=self._save_note,
            font=("Arial", 10), bg="#cce5ff"
        )
        btn.pack(pady=10)

    def _save_note(self):
        """Save the note and close popup."""
        new_note = self.note_text.get("1.0", "end-1c")
        self.save_callback(new_note)
        self.popup.destroy()


class EditPopup:
    """Advanced edit popup for client data."""

    def __init__(self, parent, client_data, columns, save_callback):
        self.parent = parent
        self.client_data = client_data
        self.columns = columns
        self.save_callback = save_callback

        self.popup = tk.Toplevel(parent)
        self.popup.title("Edycja klienta")
        self.popup.geometry("560x580")
        self.popup.configure(bg="#c9e8ff")

        # Create form fields
        self.fields_local = columns[1:]  # Skip the # column
        self.local_entries = {}

        for i, field in enumerate(self.fields_local):
            tk.Label(
                self.popup, text=field+":", bg="#c9e8ff", font=("Arial", 10)
            ).grid(row=i, column=0, sticky="w", padx=10, pady=4)

            entry = tk.Entry(self.popup, width=36)
            entry.grid(row=i, column=1, pady=4)
            entry.insert(0, client_data.get(field, ""))
            self.local_entries[field] = entry

        # Buttons
        btn_save = tk.Button(
            self.popup, text="Zapisz", font=("Arial", 11, "bold"),
            bg="#d0f0c0", width=12, command=self._save_and_close
        )
        btn_save.grid(row=len(self.fields_local), column=0, pady=18, padx=8)

        btn_cancel = tk.Button(
            self.popup, text="Anuluj", font=("Arial", 11),
            bg="#ffe0b3", width=12, command=self.popup.destroy
        )
        btn_cancel.grid(row=len(self.fields_local), column=1, pady=18, padx=8)

    def _save_and_close(self):
        """Save changes and close popup."""
        updated = {field: ent.get() for field, ent in self.local_entries.items()}
        self.save_callback(updated)
        self.popup.destroy()
