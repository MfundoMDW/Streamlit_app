import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats
import streamlit as st


def scatter_plotter(df: pd.DataFrame, all_num_cols: list):
    """Renders 2D Scatter plots and Gaussian KDE density maps."""
    st.subheader("🌌 Scatter Plotter & Density Map")
    if len(all_num_cols) < 2:
        st.warning(
            "At least 2 numeric columns are required for a scatter plot."
        )
        return

    col_x, col_y, col_color = st.columns(3)
    with col_x:
        x_var = st.selectbox("X-Axis Variable:", all_num_cols, index=0)
    with col_y:
        y_default = 1 if len(all_num_cols) > 1 else 0
        y_var = st.selectbox("Y-Axis Variable:", all_num_cols, index=y_default)
    with col_color:
        color_var = st.selectbox(
            "Color Grouping (Optional):",
            ["Density (Point Concentration)", "None"] + df.columns.tolist(),
        )

    ctrl_1, ctrl_2, ctrl_3 = st.columns(3)
    with ctrl_1:
        fig_height = st.slider("Figure Height (px):", 400, 1000, 650)
    with ctrl_2:
        lock_aspect = st.checkbox(
            "Lock Aspect Ratio (1:1 Spatial Scale)", value=False
        )
    with ctrl_3:
        point_size = st.slider("Point Size:", 1, 10, 3)

    log_s1, log_s2 = st.columns(2)
    with log_s1:
        scatter_log_x = st.checkbox(
            "Log Scale X-Axis", value=False, key="scat_x"
        )
    with log_s2:
        scatter_log_y = st.checkbox(
            "Log Scale Y-Axis", value=False, key="scat_y"
        )

    # DENSITY SCATTER BRANCH
    if color_var == "Density (Point Concentration)":
        plot_df = df[[x_var, y_var]].dropna()

        if not plot_df.empty:
            if len(plot_df) > 10000:
                st.info(
                    "⚡ Downsampling to 10,000 points for fast density calculation."
                )
                plot_df = plot_df.sample(n=10000, random_state=42)

            x_vals = plot_df[x_var].values
            y_vals = plot_df[y_var].values

            xy = np.vstack([x_vals, y_vals])
            density = scipy.stats.gaussian_kde(xy)(xy)

            fig_scatter = go.Figure(
                data=go.Scattergl(
                    x=x_vals,
                    y=y_vals,
                    mode="markers",
                    marker=dict(
                        size=point_size,
                        color=density,
                        colorscale="Plasma",
                        showscale=True,
                        colorbar=dict(title="Local Density"),
                        opacity=0.8,
                    ),
                )
            )
            fig_scatter.update_layout(
                template="plotly_dark",
                title=f"Scatter Density Map: {x_var} vs {y_var}",
            )
        else:
            st.warning("No valid numeric points to calculate density.")
            fig_scatter = go.Figure()

    # STANDARD SCATTER BRANCH
    else:
        color_arg = None if color_var == "None" else color_var
        fig_scatter = px.scatter(
            df,
            x=x_var,
            y=y_var,
            color=color_arg,
            log_x=scatter_log_x,
            log_y=scatter_log_y,
            template="plotly_dark",
            title=f"{x_var} vs {y_var}",
            labels={
                x_var: x_var,
                y_var: y_var,
                color_var: color_var if color_var else "",
            },
        )
        fig_scatter.update_traces(marker=dict(size=point_size))

    layout_updates = {
        "height": fig_height,
        "xaxis_title": x_var,
        "yaxis_title": y_var,
    }

    fig_scatter.update_xaxes(
        tickformat=".2e", showexponent="all", exponentformat="e"
    )
    fig_scatter.update_yaxes(
        tickformat=".2e", showexponent="all", exponentformat="e"
    )

    if lock_aspect:
        layout_updates["yaxis"] = dict(
            title=y_var, scaleanchor="x", scaleratio=1
        )

    fig_scatter.update_layout(**layout_updates)
    st.plotly_chart(fig_scatter, use_container_width=True)