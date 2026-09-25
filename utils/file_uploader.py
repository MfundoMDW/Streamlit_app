import streamlit as st

def render():
    """
    Renders the file uploader component of streamlit.
    """
    uploaded_file = st.file_uploader(
    "Upload your dataset (.csv, .tsv, .dat, .txt/ascii, .xlsx, .parquet, .json)",
    type=["csv", "tsv", "dat", "txt", "ascii", "xlsx", "parquet", "json"],)
    return (uploaded_file)

