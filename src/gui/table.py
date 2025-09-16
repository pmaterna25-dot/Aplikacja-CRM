"""
Client table GUI component.
"""

import tkinter as tk
from tkinter import ttk

from config import columns, STATUS_KOLORY, ROZMOWA_KOLORY
from models.client import Client


class ClientTable:
    """Table component for displaying clients."""

    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window

        # Create table frame
        self.frame = tk.Frame(parent, bg="#ffffff", bd=2, relief="solid",
                             highlightbackground="black", highlightthickness=3)

        # Create treeview
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=10)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Configure columns
        self._configure_columns()

        # Configure tags for coloring
        self._configure_tags()

        # Bind events
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Control-1>", self._on_ctrl_click)

    def _configure_columns(self):
        """Configure table columns."""
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "#":
                self.tree.column(col, width=36, stretch=True)
            elif col == "Imię i nazwisko":
                self.tree.column(col, width=130, stretch=True)
            elif col == "Telefon":
                self.tree.column(col, width=110, stretch=True)
            elif col == "Email":
                self.tree.column(col, width=150, stretch=True)
            elif col == "Notatki":
                self.tree.column(col, width=130, stretch=True)
            elif col == "Miejscowość":
                self.tree.column(col, width=100, stretch=True)
            elif col == "Status rozmowy":
                self.tree.column(col, width=128, stretch=True)
            else:
                self.tree.column(col, width=90, stretch=True)

    def _configure_tags(self):
        """Configure tags for row coloring."""
        self.tree.tag_configure("highlight", background="#ffcc99")

        # Status colors
        for status, color in STATUS_KOLORY.items():
            self.tree.tag_configure(status, background=color)

        # Conversation colors
        for rozmowa, color in ROZMOWA_KOLORY.items():
            self.tree.tag_configure(rozmowa, background=color)

    def _on_double_click(self, event):
        """Handle double-click on table row."""
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self._open_edit_popup(item_id)

    def _on_ctrl_click(self, event):
        """Handle Ctrl+click on table row."""
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self._open_note_popup(item_id)

    def _open_edit_popup(self, item_id):
        """Open advanced edit popup."""
        values = self.tree.item(item_id)["values"]
        popup = tk.Toplevel(self.main_window.root)
        popup.title("Edycja klienta")
        popup.geometry("560x580")
        popup.configure(bg="#c9e8ff")

        fields_local = columns[1:]  # Skip the # column
        local_entries = {}

        for i, field in enumerate(fields_local):
            tk.Label(popup, text=field+":", bg="#c9e8ff", font=("Arial", 10)).grid(
                row=i, column=0, sticky="w", padx=10, pady=4
            )
            entry = tk.Entry(popup, width=36)
            entry.grid(row=i, column=1, pady=4)
            entry.insert(0, values[i+1] if i+1 < len(values) else "")
            local_entries[field] = entry

        def save_and_close():
            updated = {field: ent.get() for field, ent in local_entries.items()}
            updated_row = [values[0]] + [updated.get(col, "") for col in columns if col != "#"]
            self.tree.item(item_id, values=updated_row)

            # Update in Excel
            client_data = {}
            for i, col in enumerate(columns[1:], 1):  # Skip # column
                client_data[col] = updated.get(col, "")

            from models.client import Client
            client = Client.from_dict({
                'imie_nazwisko': client_data.get("Imię i nazwisko", ""),
                'telefon': client_data.get("Telefon", ""),
                'email': client_data.get("Email", ""),
                'rocznica_majatku': client_data.get("Rocznica majątku", ""),
                'polisa_zyciowa': client_data.get("Polisa życiowa", ""),
                'notatki': client_data.get("Notatki", ""),
                'nieruchomosc': client_data.get("Nieruchomość", ""),
                'status_klienta': client_data.get("Status klienta", ""),
                'styl_rozmowy': client_data.get("Styl rozmowy", ""),
                'data_kontaktu': client_data.get("Data kontaktu", ""),
                'ponowny_kontakt': client_data.get("Ponowny kontakt", ""),
                'godzina_kontaktu': client_data.get("Godzina kontaktu", ""),
                'miejscowosc': client_data.get("Miejscowość", ""),
                'czy_posiada_dzieci': client_data.get("Czy posiada dzieci", ""),
                'status_rozmowy': client_data.get("Status rozmowy", "")
            })

            self.main_window.excel_manager.update_client(int(values[0]), client)
            popup.destroy()

            from tkinter import messagebox
            messagebox.showinfo("Zapisano", "Dane klienta zostały zaktualizowane.")

        btn_save = tk.Button(
            popup, text="Zapisz", font=("Arial", 11, "bold"),
            bg="#d0f0c0", width=12, command=save_and_close
        )
        btn_save.grid(row=len(fields_local), column=0, pady=18, padx=8)

        btn_cancel = tk.Button(
            popup, text="Anuluj", font=("Arial", 11),
            bg="#ffe0b3", width=12, command=popup.destroy
        )
        btn_cancel.grid(row=len(fields_local), column=1, pady=18, padx=8)

    def _open_note_popup(self, item_id):
        """Open note popup for editing."""
        values = self.tree.item(item_id)["values"]
        notatka = values[6] if len(values) > 6 else ""
        klient = values[1] if len(values) > 1 else "?"

        popup = tk.Toplevel(self.main_window.root)
        popup.title(f"Notatka klienta: {klient}")
        popup.geometry("420x220")
        popup.configure(bg="#ffefcc")

        tk.Label(popup, text=f"Notatka klienta: {klient}", font=("Arial", 11), bg="#ffefcc").pack(pady=10)

        note_text = tk.Text(popup, width=48, height=7, font=("Arial", 11), state="normal")
        note_text.pack(pady=2)
        note_text.insert("1.0", notatka)

        def save_note():
            new_note = note_text.get("1.0", "end-1c")
            self.tree.set(item_id, "Notatki", new_note)

            # Update in Excel
            row_num = values[0]
            try:
                from models.client import Client
                client_data = {}
                for i, col in enumerate(columns[1:], 1):
                    if i < len(values):
                        client_data[col] = values[i]

                client_data["Notatki"] = new_note

                client = Client.from_dict({
                    'imie_nazwisko': client_data.get("Imię i nazwisko", ""),
                    'telefon': client_data.get("Telefon", ""),
                    'email': client_data.get("Email", ""),
                    'rocznica_majatku': client_data.get("Rocznica majątku", ""),
                    'polisa_zyciowa': client_data.get("Polisa życiowa", ""),
                    'notatki': new_note,
                    'nieruchomosc': client_data.get("Nieruchomość", ""),
                    'status_klienta': client_data.get("Status klienta", ""),
                    'styl_rozmowy': client_data.get("Styl rozmowy", ""),
                    'data_kontaktu': client_data.get("Data kontaktu", ""),
                    'ponowny_kontakt': client_data.get("Ponowny kontakt", ""),
                    'godzina_kontaktu': client_data.get("Godzina kontaktu", ""),
                    'miejscowosc': client_data.get("Miejscowość", ""),
                    'czy_posiada_dzieci': client_data.get("Czy posiada dzieci", ""),
                    'status_rozmowy': client_data.get("Status rozmowy", "")
                })

                self.main_window.excel_manager.update_client(int(row_num), client)
            except Exception as ex:
                from tkinter import messagebox
                messagebox.showerror("Błąd", f"Nie udało się zapisać notatki: {ex}")

            popup.destroy()
            from tkinter import messagebox
            messagebox.showinfo("Zapisano", "Notatka została zaktualizowana.")

        btn = tk.Button(popup, text="Zapisz notatkę", command=save_note, font=("Arial", 10), bg="#cce5ff")
        btn.pack(pady=10)

    def add_client(self, client: Client):
        """Add a client to the table."""
        numer = len(self.tree.get_children()) + 1
        status = client.status_klienta
        ikona = ""
        if status == "Polecenie":
            ikona = "🤝 "
        elif status == "Grupówka":
            ikona = "👥 "
        elif status == "Przepisana Polisa":
            ikona = "🔄 "

        status_with_icon = f"{ikona}{status}"

        ordered_values = [
            numer,
            client.imie_nazwisko,
            client.telefon,
            client.email,
            client.rocznica_majatku,
            client.polisa_zyciowa,
            client.notatki,
            client.nieruchomosc,
            status_with_icon,
            client.styl_rozmowy,
            client.data_kontaktu,
            client.ponowny_kontakt,
            client.godzina_kontaktu,
            client.miejscowosc,
            client.czy_posiada_dzieci,
            client.status_rozmowy
        ]

        # Determine tags for coloring
        tags = ("highlight", status)
        if client.status_rozmowy in ROZMOWA_KOLORY:
            tags = (client.status_rozmowy,)

        self.tree.insert("", "end", values=ordered_values, tags=tags)

    def update_client(self, item_id, client: Client):
        """Update a client in the table."""
        values = self.tree.item(item_id)["values"]
        numer = values[0]

        status = client.status_klienta
        ikona = ""
        if status == "Polecenie":
            ikona = "🤝 "
        elif status == "Grupówka":
            ikona = "👥 "
        elif status == "Przepisana Polisa":
            ikona = "🔄 "

        status_with_icon = f"{ikona}{status}"

        ordered_values = [
            numer,
            client.imie_nazwisko,
            client.telefon,
            client.email,
            client.rocznica_majatku,
            client.polisa_zyciowa,
            client.notatki,
            client.nieruchomosc,
            status_with_icon,
            client.styl_rozmowy,
            client.data_kontaktu,
            client.ponowny_kontakt,
            client.godzina_kontaktu,
            client.miejscowosc,
            client.czy_posiada_dzieci,
            client.status_rozmowy
        ]

        # Determine tags for coloring
        tags = ("highlight", status)
        if client.status_rozmowy in ROZMOWA_KOLORY:
            tags = (client.status_rozmowy,)

        self.tree.item(item_id, values=ordered_values, tags=tags)

    def clear(self):
        """Clear all items from the table."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def get_selected_client_data(self):
        """Get data of selected client."""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            return dict(zip(columns, values))
        return None
