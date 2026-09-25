import streamlit as st
import pandas as pd

def render(df: pd.DataFrame):
    st.subheader("Data Health Scorecard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Duplicate Rows", df.duplicated().sum())
    col4.metric("Total Missing Cells", df.isnull().sum().sum())

    st.write("**Missing Values Breakdown:**")
    missing_df = (
        df.isnull()
        .sum()
        .reset_index()
        .rename(columns={"index": "Column", 0: "Missing Count"})
    )
    missing_df["Missing %"] = (
        missing_df["Missing Count"] / len(df) * 100
    ).round(1)

    active_missing = missing_df[missing_df["Missing Count"] > 0]
    if not active_missing.empty:
        st.dataframe(active_missing, use_container_width=True)
    else:
        st.info("No missing values found in this dataset!")
