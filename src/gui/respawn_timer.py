"""
Metin2 respawn reminder window.
"""

import tkinter as tk
from datetime import datetime, timedelta

RESPAWN_INTERVAL = timedelta(minutes=30)
ALERT_FLASHES = 30
FLASH_INTERVAL_MS = 500
BG = "#e6f2ff"


def compute_next_reminder(start, now):
    """Return the first start + k * 30 min moment strictly after now."""
    if start > now + timedelta(hours=12):
        start -= timedelta(days=1)
    next_time = start + RESPAWN_INTERVAL
    while next_time <= now:
        next_time += RESPAWN_INTERVAL
    return next_time


class RespawnTimer:
    """Counts down to the next respawn reminder every 30 minutes."""

    def __init__(self, parent):
        self.popup = tk.Toplevel(parent)
        self.popup.title("Respy Metin2")
        self.popup.geometry("340x290")
        self.popup.resizable(False, False)
        self.popup.configure(bg=BG)
        self.popup.protocol("WM_DELETE_WINDOW", self.close)

        self.next_reminder = None
        self.tick_id = None
        self.flash_id = None

        tk.Label(
            self.popup, text="Czas, od którego liczyć (HH:MM):",
            font=("Arial", 10), bg=BG
        ).pack(pady=(14, 4))

        self.time_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        tk.Entry(
            self.popup, textvariable=self.time_var, width=10,
            justify="center", font=("Arial", 12)
        ).pack()

        self.error_label = tk.Label(self.popup, text="", fg="red", bg=BG, font=("Arial", 9))
        self.error_label.pack()

        buttons = tk.Frame(self.popup, bg=BG)
        buttons.pack(pady=6)
        tk.Button(
            buttons, text="Start", width=10, bg="#cce5ff", font=("Arial", 10),
            command=self.start
        ).pack(side="left", padx=6)
        tk.Button(
            buttons, text="Stop", width=10, bg="#f2f2f2", font=("Arial", 10),
            command=self.stop
        ).pack(side="left", padx=6)

        self.status_label = tk.Label(
            self.popup, text="Zegarek zatrzymany", font=("Arial", 11, "bold"), bg=BG
        )
        self.status_label.pack(pady=(6, 2))

        self.countdown_label = tk.Label(self.popup, text="", font=("Arial", 22, "bold"), bg=BG)
        self.countdown_label.pack()

        self.alert_label = tk.Label(self.popup, text="", font=("Arial", 13, "bold"), bg=BG)
        self.alert_label.pack(pady=(8, 0))

    def start(self):
        try:
            start_time = datetime.strptime(self.time_var.get().strip(), "%H:%M").time()
        except ValueError:
            self.error_label.config(text="Podaj czas w formacie HH:MM")
            return

        self.error_label.config(text="")
        self.stop()

        now = datetime.now()
        start = datetime.combine(now.date(), start_time)
        self.next_reminder = compute_next_reminder(start, now)
        self._tick()

    def stop(self):
        if self.tick_id is not None:
            self.popup.after_cancel(self.tick_id)
            self.tick_id = None
        if self.flash_id is not None:
            self.popup.after_cancel(self.flash_id)
            self.flash_id = None

        self.next_reminder = None
        self.status_label.config(text="Zegarek zatrzymany")
        self.countdown_label.config(text="")
        self.alert_label.config(text="", bg=BG)

    def close(self):
        self.stop()
        self.popup.destroy()

    def _tick(self):
        now = datetime.now()
        remaining = self.next_reminder - now

        if remaining.total_seconds() <= 0:
            fired_at = self.next_reminder
            self.next_reminder = compute_next_reminder(fired_at, now)
            self._alert(fired_at)
            remaining = self.next_reminder - now

        minutes, seconds = divmod(int(remaining.total_seconds()), 60)
        self.status_label.config(text=f"Następny respawn o {self.next_reminder:%H:%M}")
        self.countdown_label.config(text=f"{minutes:02d}:{seconds:02d}")
        self.tick_id = self.popup.after(1000, self._tick)

    def _alert(self, fired_at):
        self.popup.bell()
        self.popup.deiconify()
        self.popup.lift()

        if self.flash_id is not None:
            self.popup.after_cancel(self.flash_id)
        self.alert_label.config(text=f"RESP! ({fired_at:%H:%M})")
        self._flash(ALERT_FLASHES)

    def _flash(self, remaining):
        if remaining <= 0:
            self.flash_id = None
            self.alert_label.config(text="", bg=BG)
            return

        colour = "#ff3b3b" if remaining % 2 else BG
        self.alert_label.config(bg=colour)
        self.flash_id = self.popup.after(FLASH_INTERVAL_MS, self._flash, remaining - 1)
