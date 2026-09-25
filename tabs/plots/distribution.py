import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def distribution_plotter(
    df: pd.DataFrame, all_num_cols: list, num_cols: list
):
    """Renders distribution plots (Histogram, Bar Chart, Box Plot)."""
    st.subheader("📊 Distribution Plotter")
    if not all_num_cols:
        st.warning("No numeric columns found for plotting.")
        return

    selected_vars = st.multiselect(
        "Choose up to two columns to plot distributions for:",
        options=all_num_cols,
        default=num_cols[: min(2, len(num_cols))],
        max_selections=2,
    )

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)
    with ctrl_col1:
        chart_type = st.radio(
            "Chart Type:",
            ["Histogram", "Bar Chart", "Box Plot"],
            horizontal=True,
        )
    with ctrl_col2:
        plot_style = st.radio(
            "Fill Style:", ["Filled", "Unfilled / Outline"], horizontal=True
        )
    with ctrl_col3:
        if chart_type in ["Histogram", "Bar Chart"]:
            bins = st.slider("Select Number of Bins:", 5, 100, 20)

    log_c1, log_c2 = st.columns(2)
    with log_c1:
        use_log_y = st.checkbox("Log Scale Y-Axis", value=False)
    with log_c2:
        use_log_x = st.checkbox("Log Scale X-Axis", value=False)

    if not selected_vars:
        st.info("Please select at least one numeric column above.")
        return

    for var in selected_vars:
        st.markdown(f"### Distribution of **{var}**")

        if chart_type == "Histogram":
            fig = px.histogram(
                df,
                x=var,
                nbins=bins,
                log_y=use_log_y,
                log_x=use_log_x,
                template="plotly_dark",
                title=f"Histogram of {var}",
                labels={var: var, "count": "Frequency / Count"},
            )
            if plot_style == "Unfilled / Outline":
                fig.update_traces(
                    marker=dict(
                        color="rgba(0,0,0,0)",
                        line=dict(color="#636EFA", width=1.5),
                    )
                )
            fig.update_layout(
                xaxis_title=var, yaxis_title="Frequency / Count"
            )

        elif chart_type == "Bar Chart":
            counts, bin_edges = np.histogram(df[var].dropna(), bins=bins)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            if plot_style == "Filled":
                fig = px.bar(
                    x=bin_centers,
                    y=counts,
                    log_y=use_log_y,
                    log_x=use_log_x,
                    labels={"x": var, "y": "Frequency / Count"},
                    template="plotly_dark",
                    title=f"Bar Chart of {var}",
                )
            else:
                fig = px.line(
                    x=bin_centers,
                    y=counts,
                    log_y=use_log_y,
                    log_x=use_log_x,
                    labels={"x": var, "y": "Frequency / Count"},
                    template="plotly_dark",
                    title=f"Bar Line Chart of {var}",
                )
            fig.update_layout(
                xaxis_title=var, yaxis_title="Frequency / Count"
            )

        else:
            fig = px.box(
                df,
                y=var,
                log_y=use_log_y,
                template="plotly_dark",
                title=f"Box Plot of {var}",
                labels={var: var},
            )
            fig.update_layout(yaxis_title=var)

        st.plotly_chart(fig, use_container_width=True)