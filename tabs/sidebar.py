# sidebar.py
import streamlit as st

def render():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/wizard.png", width=70)
        st.title("PlotterGuru")
        st.caption("v1.2 | Astronomical & Tabular Data Workbench")
        st.markdown("---")
        
        st.markdown("### 🚀 Quick Start")
        st.markdown("""
        1. **Upload** your dataset or click **Use Sample Dataset**.
        2. Inspect dataset health & missing values in **Diagnostics**.
        3. Calculate median, MAD, and **NMAD** in **Column Analytics**.
        4. Plot **Histograms**, **Density Heatmaps**, or **Scatter Plots** in **Smart Visuals**.
        5. Clean duplicates and export in **1-Click Cleaner**.
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Supported Formats")
        st.code("CSV, TSV, DAT, TXT, XLSX, Parquet, JSON")
