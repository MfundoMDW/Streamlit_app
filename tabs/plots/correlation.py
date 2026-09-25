import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def correlation_heatmap(df: pd.DataFrame, all_num_cols: list):
    """Renders the Pearson Correlation Heatmap for numeric columns."""
    if len(all_num_cols) >= 2:
        st.subheader("🔗 Correlation Heatmap")
        corr = df[all_num_cols].corr().round(2)

        fig_corr = go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.index,
                colorscale="RdBu_r",
                zmin=-1,
                zmax=1,
                text=corr.values,
                texttemplate="%{text}",
                colorbar=dict(title="Pearson Corr (r)"),
            )
        )
        fig_corr.update_layout(
            template="plotly_dark",
            height=400,
            xaxis_title="Features",
            yaxis_title="Features",
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        st.markdown("---")