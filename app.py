import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats
import streamlit as st

st.set_page_config(
    page_title="PlotterGuru - Smart Data Explorer",
    page_icon="🧙‍♂️",
    layout="wide",
)

# --- SIDEBAR HELP & INFORMATION ---
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


# --- MAIN HEADER ---
st.title("🧙‍♂️ PlotterGuru")
st.caption(
"Your intelligent companion for data profiling, instant visualizations, and robust scatter/density mapping."
)

st.caption(
"Developed by [Raymond Mdwadube](https://github.com/RaymondM) - Empowering Data scientiscts & Enthusiasts Everywhere!"
)


uploaded_file = st.file_uploader(
    "Upload your dataset (.csv, .tsv, .dat, .txt/ascii, .xlsx, .parquet, .json)",
    type=["csv", "tsv", "dat", "txt", "ascii", "xlsx", "parquet", "json"],
)


@st.cache_data
def load_data(file):
    filename = file.name.lower()

    if filename.endswith(".xlsx"):
        return pd.read_excel(file)
    elif filename.endswith(".parquet"):
        return pd.read_parquet(file)
    elif filename.endswith(".json"):
        return pd.read_json(file)
    else:
        try:
            return pd.read_csv(file, sep=None, engine="python")
        except Exception:
            file.seek(0)
            return pd.read_csv(file, sep=r"\s+", engine="python")


if uploaded_file:
    try:
        if (
            "df" not in st.session_state
            or st.session_state.get("file_name") != uploaded_file.name
        ):
            st.session_state.df = load_data(uploaded_file)
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

        # --- TAB 2: COLUMN ANALYTICS & NMAD ---
        with tab_stats:
            col_sel = st.selectbox(
                "Select a Column to inspect:", df.columns.tolist()
            )
            if col_sel:
                col_data = df[col_sel]
                
                # --- DEBUG / DIAGNOSTIC BLOCK ---
                with st.expander("🔍 Debug Column Data & Stats"):
                    st.write(f"**Selected Column:** `{col_sel}`")
                    st.write(f"**Detected Dtype:** `{col_data.dtype}`")
                    st.write(f"**Raw Non-Null Count:** {col_data.count()} / {len(df)}")
                    
                    # Coerce to numeric if it was ingested as object/string
                    coerced_series = pd.to_numeric(col_data, errors="coerce").dropna()
                    
                    st.write(f"**Clean Numeric Rows:** {len(coerced_series)}")
                    if not coerced_series.empty:
                        st.write(f"**Calculated Mean:** {coerced_series.mean():.6e}")
                        st.write(f"**Calculated Median:** {coerced_series.median():.6e}")
                        
                        # Manual MAD calculation check
                        med_val = coerced_series.median()
                        mad_val = (coerced_series - med_val).abs().median()
                        nmad_val = 1.4826 * mad_val
                        
                        st.write(f"**Manual MAD:** {mad_val:.6e}")
                        st.write(f"**Manual NMAD (1.4826 × MAD):** {nmad_val:.6e}")

                # --- NMAD Diagnostics Section ---
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

                        # Force scientific notation on axis tick labels
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

        # --- TAB 3: VISUALISATION PLOTS & CORRELATION ---
        with tab_visuals:
            num_cols = [
                c
                for c in df.select_dtypes(include="number").columns
                if c.lower() not in ["#", "index", "id", "unnamed: 0"]
            ]
            all_num_cols = df.select_dtypes(include="number").columns.tolist()

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

            viz_mode = st.radio(
                "Select Visualization Mode:",
                ["Distribution Plotter", "Scatter Plotter"],
                horizontal=True,
            )



            if viz_mode == "Distribution Plotter":
                st.subheader("📊 Distribution Plotter")
                if all_num_cols:
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
                            "Fill Style:",
                            ["Filled", "Unfilled / Outline"],
                            horizontal=True,
                        )
                    with ctrl_col3:
                        if chart_type in ["Histogram", "Bar Chart"]:
                            bins = st.slider("Select Number of Bins:", 5, 100, 20)

                    log_c1, log_c2 = st.columns(2)
                    with log_c1:
                        use_log_y = st.checkbox("Log Scale Y-Axis", value=False)
                    with log_c2:
                        use_log_x = st.checkbox("Log Scale X-Axis", value=False)

                    if selected_vars:
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
                                counts, bin_edges = np.histogram(
                                    df[var].dropna(), bins=bins
                                )
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
                    else:
                        st.info("Please select at least one numeric column above.")
                else:
                    st.warning("No numeric columns found for plotting.")

            else:
                st.subheader("🌌 Scatter Plotter & Density Map")
                if len(all_num_cols) >= 2:
                    col_x, col_y, col_color = st.columns(3)
                    with col_x:
                        x_var = st.selectbox(
                            "X-Axis Variable:", all_num_cols, index=0
                        )
                    with col_y:
                        y_default = 1 if len(all_num_cols) > 1 else 0
                        y_var = st.selectbox(
                            "Y-Axis Variable:", all_num_cols, index=y_default
                        )
                    with col_color:
                        color_var = st.selectbox(
                            "Color Grouping (Optional):",
                            ["Density (Point Concentration)", "None"]
                            + df.columns.tolist(),
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

                    # -------------------------------------------------------------
                    # DENSITY SCATTER BRANCH (Calculates KDE per point)
                    # -------------------------------------------------------------
                    if color_var == "Density (Point Concentration)":
                        plot_df = df[[x_var, y_var]].dropna()

                        if not plot_df.empty:
                            # Downsample if dataset is large for quick execution
                            if len(plot_df) > 10000:
                                st.info("⚡ Downsampling to 10,000 points for fast density calculation.")
                                plot_df = plot_df.sample(n=10000, random_state=42)

                            x_vals = plot_df[x_var].values
                            y_vals = plot_df[y_var].values

                            # Compute 2D Gaussian Kernel Density Estimate
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

                    # -------------------------------------------------------------
                    # STANDARD SCATTER BRANCH
                    # -------------------------------------------------------------
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

                    # Common Layout Configuration & Formatting
                    layout_updates = {
                        "height": fig_height,
                        "xaxis_title": x_var,
                        "yaxis_title": y_var,
                    }
                    
                    # Scientific notation on tick labels for tiny values
                    fig_scatter.update_xaxes(tickformat=".2e", showexponent="all", exponentformat="e")
                    fig_scatter.update_yaxes(tickformat=".2e", showexponent="all", exponentformat="e")

                    if lock_aspect:
                        layout_updates["yaxis"] = dict(
                            title=y_var, scaleanchor="x", scaleratio=1
                        )

                    fig_scatter.update_layout(**layout_updates)
                    st.plotly_chart(fig_scatter, use_container_width=True)

                else:
                    st.warning("At least 2 numeric columns are required for a scatter plot.")

        # --- TAB 4: DATA CLEANER & EXPORT ---
        with tab_clean:
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

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Upload any tabular data file above to begin scanning.")