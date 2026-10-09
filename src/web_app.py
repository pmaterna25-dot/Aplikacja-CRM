"""
Read-only web preview of the Materna CRM application.

Run from the project root:
    streamlit run src/web_app.py
"""

import os
import sys
from dataclasses import fields
from datetime import datetime

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import STATUS_KOLORY, columns
from models.client import Client
from utils.excel_manager import ExcelManager

EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "materna_ind.xlsx")
STATUS_KLIENTA_KOL = "Status klienta"


def koloruj_wiersz(wiersz: pd.Series) -> list:
    kolor = STATUS_KOLORY.get(wiersz[STATUS_KLIENTA_KOL])
    return [f"background-color: {kolor}" if kolor else "" for _ in wiersz]


st.set_page_config(page_title="Materna CRM – podgląd", layout="wide")
st.title("Materna – CRM dla doradcy ubezpieczeniowego")
st.caption("Podgląd webowy, tylko do odczytu. Dane z materna_ind.xlsx.")

manager = ExcelManager(filename=EXCEL_PATH)
clients = manager.load_all_clients()
today = datetime.today().strftime("%Y-%m-%d")
stats = manager.get_statistics_for_date(today)

col1, col2, col3 = st.columns(3)
col1.metric("Klienci łącznie", len(clients))
col2.metric("Kontakty dziś", manager.get_today_clients_count(today))
col3.metric("Nowi klienci dziś", stats.nowi_klienci if stats else 0)

statusy = sorted({c.status_klienta for c in clients if c.status_klienta})
wybrane = st.multiselect("Filtruj po statusie klienta", statusy)
if wybrane:
    clients = [c for c in clients if c.status_klienta in wybrane]

if not clients:
    st.info("Brak klientów do wyświetlenia.")
else:
    df = pd.DataFrame([c.to_dict() for c in clients], columns=[f.name for f in fields(Client)])
    df.columns = columns[1:]
    st.dataframe(df.style.apply(koloruj_wiersz, axis=1), hide_index=True)
