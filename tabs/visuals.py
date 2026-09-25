import pandas as pd
import streamlit as st

from tabs.plots.correlation import correlation_heatmap
from tabs.plots.distribution import distribution_plotter
from tabs.plots.scatter import scatter_plotter

#from tabs.plots import correlation_heatmap, distribution_plotter, scatter_plotter

def render(df: pd.DataFrame):
    """Main rendering wrapper for Tab 3: Visuals."""
    num_cols = [
        c
        for c in df.select_dtypes(include="number").columns
        if c.lower() not in ["#", "index", "id", "unnamed: 0"]
    ]
    all_num_cols = df.select_dtypes(include="number").columns.tolist()

    # 1. Render Heatmap
    correlation_heatmap(df, all_num_cols)

    # 2. Render Mode Radio Selector
    viz_mode = st.radio(
        "Select Visualization Mode:",
        ["Distribution Plotter", "Scatter Plotter"],
        horizontal=True,
    )

    # 3. Render Chosen Sub-View
    if viz_mode == "Distribution Plotter":
        distribution_plotter(df, all_num_cols, num_cols)
    else:
        scatter_plotter(df, all_num_cols)