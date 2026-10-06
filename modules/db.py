import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

@st.cache_resource
def get_connection():
    """Establishes Google Sheets Connection."""
    return st.connection("gsheets", type=GSheetsConnection)

def fetch_data(worksheet_name: str) -> pd.DataFrame:
    """Reads data from a specified Google Sheet worksheet."""
    conn = get_connection()
    try:
        df = conn.read(worksheet=worksheet_name, ttl="1m")
        return df
    except Exception:
        return pd.DataFrame()

def append_row(worksheet_name: str, new_row_dict: dict):
    """Appends a new record to the worksheet."""
    conn = get_connection()
    df = fetch_data(worksheet_name)
    updated_df = pd.concat([df, pd.DataFrame([new_row_dict])], ignore_index=True)
    conn.update(worksheet=worksheet_name, data=updated_df)
    st.cache_data.clear()

def generate_visit_id(worker_id: str, daily_visit_count: int) -> str:
    """Generates unique Visit ID: VISIT-YYYYMMDD-W001-001"""
    date_str = pd.Timestamp.now().strftime("%Y%m%d")
    return f"VISIT-{date_str}-{worker_id.upper()}-{daily_visit_count:03d}"