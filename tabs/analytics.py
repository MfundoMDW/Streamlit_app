import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def render(df: pd.DataFrame):
    col_sel = st.selectbox(
        "Select a Column to inspect:", df.columns.tolist()
    )
    if col_sel:
        col_data = df[col_sel]
        with st.expander("🔍 Debug Column Data & Stats"):
            st.write(f"**Selected Column:** `{col_sel}`")
            st.write(f"**Detected Dtype:** `{col_data.dtype}`")
            st.write(f"**Raw Non-Null Count:** {col_data.count()} / {len(df)}")
            coerced_series = pd.to_numeric(col_data, errors="coerce").dropna()
            st.write(f"**Clean Numeric Rows:** {len(coerced_series)}")
            if not coerced_series.empty:
                st.write(f"**Calculated Mean:** {coerced_series.mean():.6e}")
                st.write(f"**Calculated Median:** {coerced_series.median():.6e}")
                med_val = coerced_series.median()
                mad_val = (coerced_series - med_val).abs().median()
                nmad_val = 1.4826 * mad_val
                st.write(f"**Manual MAD:** {mad_val:.6e}")
                st.write(f"**Manual NMAD (1.4826 × MAD):** {nmad_val:.6e}")

        if pd.api.types.is_numeric_dtype(col_data):
            st.markdown("---")
            st.subheader("📐 Absolute Deviation Diagnostics (NMAD)")
            clean_series = col_data.dropna()
            if not clean_series.empty:
                med = clean_series.median()
                abs_dev = (clean_series - med).abs()
                mad = abs_dev.median()
                nmad = 1.4826 * mad

                nm_col1, nm_col2, nm_col3 = st.columns(3)
                nm_col1.metric("Median", f"{med:.4e}")
                nm_col2.metric("MAD", f"{mad:.4e}")
                nm_col3.metric("NMAD (1.4826 × MAD)", f"{nmad:.4e}")

                scale_col1, scale_col2 = st.columns(2)
                with scale_col1:
                    log_y_nmad = st.checkbox(
                        "Log Scale Y-Axis (Count)",
                        value=True,
                        key="nmad_log_y",
                    )
                with scale_col2:
                    log_x_nmad = st.checkbox(
                        "Log Scale X-Axis (|X - Median|)",
                        value=False,
                        key="nmad_log_x",
                    )

                fig_dev = px.histogram(
                    x=abs_dev,
                    nbins=25,
                    template="plotly_dark",
                    log_y=log_y_nmad,
                    log_x=log_x_nmad,
                    labels={
                        "x": f"Absolute Deviation |{col_sel} - Median|",
                        "y": "Frequency / Row Count",
                    },
                    title=f"Distribution of Absolute Deviations from Median ({col_sel})",
                )
                fig_dev.update_xaxes(tickformat=".2e", showexponent="all", exponentformat="e")
                fig_dev.update_yaxes(showexponent="all", exponentformat="e")
                # Staggered vertical lines for MAD and NMAD
                fig_dev.add_vline(
                    x=0,
                    line_dash="solid",
                    line_color="cyan",
                    annotation_text="Median Base (0)",
                    annotation_position="top left",
                    annotation=dict(
                        font_size=11,
                        bgcolor="rgba(0,0,0,0.6)",
                        bordercolor="cyan",
                    ),
                )
                fig_dev.add_vline(
                    x=mad,
                    line_dash="dash",
                    line_color="yellow",
                    annotation_text=f"MAD ({mad:.4e})",
                    annotation_position="top right",
                    annotation=dict(
                        font_size=11,
                        bgcolor="rgba(0,0,0,0.6)",
                        bordercolor="yellow",
                        yshift=-25,
                    ),
                )
                fig_dev.add_vline(
                    x=nmad,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"NMAD ({nmad:.4e})",
                    annotation_position="top right",
                    annotation=dict(
                        font_size=11,
                        bgcolor="rgba(0,0,0,0.6)",
                        bordercolor="red",
                        yshift=-50,
                    ),
                )

                fig_dev.update_layout(
                    xaxis_title=f"Absolute Deviation |{col_sel} - Median|",
                    yaxis_title="Frequency / Row Count",
                )
                st.plotly_chart(fig_dev, use_container_width=True)
            else:
                st.warning("Selected column contains only null values.")