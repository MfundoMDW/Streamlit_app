import streamlit as st
import pandas as pd

def render(df: pd.DataFrame):
    st.subheader("Quick Clean Actions")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Drop Duplicate Rows"):
            st.session_state.df = df.drop_duplicates()
            st.success("Duplicates removed!")
            st.rerun()
    with col_btn2:
        if st.button("Drop Rows with Missing Values"):
            st.session_state.df = df.dropna()
            st.success("Null values removed!")
            st.rerun()
    st.markdown("---")
    st.subheader("Export Cleaned Data")
    export_format = st.selectbox(
        "Choose export format:", ["CSV (.csv)", "TSV (.tsv)"]
    )
    is_tsv = "TSV" in export_format
    sep = "\t" if is_tsv else ","
    file_ext = "tsv" if is_tsv else "csv"
    cleaned_bytes = df.to_csv(index=False, sep=sep).encode("utf-8")
    st.download_button(
        label=f"📥 Download Processed File ({export_format.split()[0]})",
        data=cleaned_bytes,
        file_name=f"plotterguru_cleaned.{file_ext}",
        mime="text/plain",
    )
