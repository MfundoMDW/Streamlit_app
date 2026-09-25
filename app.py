#Main (app.py)

import streamlit as st
from tabs import sidebar
from tabs import diagnostics, analytics, visuals, cleaner
from utils import file_uploader as uploader
from utils import data_loader


st.set_page_config(
    page_title="PlotterGuru - Smart Data Explorer",
    page_icon="🧙‍♂️",
    layout="wide",
)

# --- MAIN HEADER ---
st.title("🧙‍♂️ PlotterGuru")
st.caption(
"Your intelligent companion for data profiling, instant visualisations, and robust scatter/density mapping.")

#subcaption
st.caption(
"Developed by [Mfundo Mdwadube](https://github.com/MfundoMDW) - Empowering Data scientiscts & Enthusiasts Everywhere!")

sidebar.render()
uploaded_file = uploader.render()

if uploaded_file:
    try:
        if (
            "df" not in st.session_state
            or st.session_state.get("file_name") != uploaded_file.name
        ):
            st.session_state.df = data_loader.load_data(uploaded_file)
            st.session_state.file_name = uploaded_file.name

        df = st.session_state.df

        st.success(
            f"Successfully ingested **{uploaded_file.name}** ({df.shape[0]} rows × {df.shape[1]} columns)"
        )

        # --- TAB NAVIGATION ---
        tab_health, tab_stats, tab_visuals, tab_clean = st.tabs(
            [
                "🏥 Data Health Diagnostics",
                "📈 Column Analytics",
                "📊 Smart Visuals",
                "🧹 1-Click Data Cleaner",
            ]
        )

        # --- TAB 1: DATA HEALTH DIAGNOSTICS ---
        with tab_health:
            diagnostics.render(df)

        # --- TAB 2: COLUMN ANALYTICS ---
        with tab_stats:
            analytics.render(df)

        # --- TAB 3: SMART VISUALS ---
        with tab_visuals:
            visuals.render(df)

        # --- TAB 4: 1-CLICK DATA CLEANER ---
        with tab_clean:
            cleaner.render(df)

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Upload any tabular data file above to begin scanning.")
