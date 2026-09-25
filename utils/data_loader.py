import pandas as pd 
import streamlit as st

@st.cache_data
def load_data(file):
    filename = file.name.lower()

    if filename.endswith(".xlsx"):
        return pd.read_excel(file)
    elif filename.endswith(".parquet"):
        return pd.read_parquet(file)
    elif filename.endswith(".json"):
        return pd.read_json(file)
    else:
        try:
            return pd.read_csv(file, sep=None, engine="python")
        except Exception:
            file.seek(0)
            return pd.read_csv(file, sep=r"\s+", engine="python")
