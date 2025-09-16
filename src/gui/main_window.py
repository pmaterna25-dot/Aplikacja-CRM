"""
Main window for the Materna CRM application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time
import os

from config import (
    WINDOW_W, WINDOW_H, STYLES, STATUS_KOLORY, ROZMOWA_KOLORY,
    ROZMOWA_OPCJE, style_opcje, nieruchomosci_opcje, rocznica_przedzialy,
    godziny_opcje, columns
)
from models.client import Client
from utils.excel_manager import ExcelManager
from gui.forms import ClientForm
from gui.table import ClientTable
from gui.filters import FilterPanel
from gui.popups import StatisticsPopup, StyleSelector


class MainWindow:
    """Main application window."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Materna – CRM dla doradcy ubezpieczeniowego")
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.minsize(800, 600)
        self.root.resizable(True, True)

        # Initialize components
        self.excel_manager = ExcelManager()
        self.current_style_file = "kosmici.jpg"
        self.session_start = time.time()
        self.today_str = datetime.today().strftime("%Y-%m-%d")

        # Initialize edit mode variables
        self.edit_mode = False
        self.selected_item_id = None
        self.selected_row_number = None

        # Setup UI
        self._setup_background()
        self._setup_components()
        self._setup_layout()

        # Load initial data
        self._load_initial_data()

    def _setup_background(self):
        """Setup background image."""
        try:
            from PIL import Image, ImageTk
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            assets_dir = os.path.join(os.path.dirname(script_dir), "assets")
            img_path = os.path.join(assets_dir, self.current_style_file)
            img = Image.open(img_path).resize((WINDOW_W, WINDOW_H))
            self.bg_photo = ImageTk.PhotoImage(img)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background: {e}")
            self.bg_photo = None
            self.bg_label = tk.Label(self.root, bg="#f0f0f0")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def _setup_components(self):
        """Setup main UI components."""
        self.client_form = ClientForm(self.root, self)
        self.client_table = ClientTable(self.root, self)
        self.filter_panel = FilterPanel(self.root, self)

        # Statistics labels
        self.label_time = tk.Label(self.root, text="", font=("Arial", 10), bg="#e6f2ff")
        self.label_clients = tk.Label(self.root, text="", font=("Arial", 10), bg="#e6f2ff")

    def _setup_layout(self):
        """Setup the layout and bindings."""
        self.root.bind('<Configure>', self._scale_layout)

        # Initial layout
        self._scale_layout()

        # Set up layering
        self.client_form.frame.lift()
        self.client_table.frame.lift()
        self.filter_panel.frame.lift()

    def _load_initial_data(self):
        """Load initial data and start timers."""
        self.root.after(400, self._scale_layout)
        self.root.after(700, self._load_all_clients)
        self.root.after(1000, self._update_stats_labels)

    def _scale_layout(self, event=None):
        """Scale layout based on window size."""
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        # Update background
        self._update_background(w, h)

        # Form (top, 60% width)
        form_w = int(w * 0.6)
        form_w = max(form_w, 500)
        form_h = int(h * 0.36)
        form_h = max(form_h, 270)
        self.client_form.frame.place(x=30, y=30, width=form_w, height=form_h)

        # Table (middle)
        table_w = min(max(1100, int(w * 0.93)), w - 60)
        table_h = min(max(100, int(h * 0.14)), h - 60)
        table_x = 30
        table_y = 30 + form_h + 12
        self.client_table.frame.place(x=table_x, y=table_y, width=table_w, height=table_h)

        # Filter panel (bottom)
        filter_w = table_w
        filter_h = min(max(110, int(h * 0.17)), h - 60)
        filter_x = 30
        filter_y = table_y + table_h + 10
        self.filter_panel.frame.place(x=filter_x, y=filter_y, width=filter_w, height=filter_h)

        # Place statistics labels in the filter panel area
        self.label_time.place(x=filter_x + 400, y=filter_y + 10)
        self.label_clients.place(x=filter_x + 600, y=filter_y + 10)

    def _update_background(self, width, height):
        """Update background image."""
        if self.bg_photo:
            try:
                from PIL import Image, ImageTk
                # Get the directory where this script is located
                script_dir = os.path.dirname(os.path.abspath(__file__))
                assets_dir = os.path.join(os.path.dirname(script_dir), "assets")
                img_path = os.path.join(assets_dir, self.current_style_file)
                img = Image.open(img_path).resize((max(1, width), max(1, height)))
                self.bg_photo = ImageTk.PhotoImage(img)
                self.bg_label.config(image=self.bg_photo)
                self.bg_label.image = self.bg_photo
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"Error updating background: {e}")

    def _update_stats_labels(self):
        """Update statistics labels."""
        elapsed = int(time.time() - self.session_start)
        h, m, s = elapsed // 3600, (elapsed // 60) % 60, elapsed % 60
        self.label_time.config(text=f"Czas dzisiaj: {h:02d}:{m:02d}:{s:02d}")

        count = self.excel_manager.get_today_clients_count(self.today_str)
        self.label_clients.config(text=f"Nowych klientów dzisiaj: {count}")

        self.root.after(1000, self._update_stats_labels)

    def _load_all_clients(self):
        """Load all clients from Excel."""
        self.client_table.clear()
        clients = self.excel_manager.load_all_clients()
        for client in clients:
            self.client_table.add_client(client)

    def save_client(self):
        """Save current client data."""
        client_data = self.client_form.get_client_data()

        if self.edit_mode and self.selected_item_id is not None and self.selected_row_number is not None:
            # Update existing client
            client = Client.from_dict(client_data)
            if self.excel_manager.update_client(self.selected_row_number, client):
                self.client_table.update_client(self.selected_item_id, client)
                messagebox.showinfo("Zaktualizowano", "Kontakt został zaktualizowany.")
        else:
            # Save new client
            client = Client.from_dict(client_data)
            if self.excel_manager.save_client(client):
                self.excel_manager.add_statistics_for_today(self.today_str, client.status_rozmowy)
                self.client_table.add_client(client)
                messagebox.showinfo("Zapisano", "Kontakt został dodany!")

        self.edit_mode = False
        self.client_form.reset_form()

    def delete_client(self):
        """Delete selected client."""
        selected = self.client_table.tree.selection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Wybierz kontakt do usunięcia.")
            return

        item_id = selected[0]
        values = self.client_table.tree.item(item_id)["values"]
        if not values:
            return

        # Confirmation dialog
        imie_nazwisko = values[1]
        if messagebox.askyesno("Potwierdzenie usunięcia",
                              f"Czy na pewno chcesz usunąć klienta:\n{imie_nazwisko}?"):
            row_number = int(values[0])
            if self.excel_manager.delete_client(row_number):
                self.client_table.tree.delete(item_id)
                self.client_form.reset_form()
                self._load_all_clients()
                messagebox.showinfo("Usunięto", f"Klient {imie_nazwisko} został usunięty.")

    def show_statistics_popup(self):
        """Show statistics popup."""
        StatisticsPopup(self.root, self.excel_manager)

    def show_style_selector(self):
        """Show style selector popup."""
        def on_style_selected(style_file):
            self.current_style_file = style_file
            self._scale_layout()

        StyleSelector(self.root, on_style_selected)

    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
