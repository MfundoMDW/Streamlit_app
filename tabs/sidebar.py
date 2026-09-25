import streamlit as st

# Inject Custom Modern Tech CSS
st.markdown(
    """
    <style>
    /* Dark glassmorphic card container */
    .tech-card {
        background: linear-gradient(135deg, rgba(25, 30, 45, 0.7) 0%, rgba(15, 18, 28, 0.85) 100%);
        border: 1px solid rgba(0, 229, 255, 0.18);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(8px);
    }
    
    /* Header with glowing text */
    .tech-header {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.05em;
        color: #00E5FF;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        text-transform: uppercase;
    }
    
    /* Step-by-step list design */
    .tech-step {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 10px;
        font-size: 0.85rem;
        color: #C5D1EC;
        line-height: 1.4;
    }
    
    /* Neon Step Numbers */
    .step-num {
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid #00E5FF;
        color: #00E5FF;
        font-weight: bold;
        font-size: 0.75rem;
        min-width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 6px rgba(0, 229, 255, 0.4);
        flex-shrink: 0;
        margin-top: 1px;
    }
    
    /* High-tech pill tags */
    .tech-pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }
    
    .tech-pill {
        background: rgba(123, 97, 255, 0.12);
        border: 1px solid rgba(123, 97, 255, 0.4);
        color: #B39DDB;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-family: 'Fira Code', monospace;
        font-weight: 600;
        letter-spacing: 0.03em;
        transition: all 0.2s ease;
    }
    .tech-pill:hover {
        background: rgba(0, 229, 255, 0.2);
        border-color: #00E5FF;
        color: #FFFFFF;
        box-shadow: 0 0 8px rgba(0, 229, 255, 0.5);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Layout
with st.sidebar:
    # Header Section
    st.image("https://img.icons8.com/color/96/wizard.png", width=60)
    st.markdown(
        "<h2 style='margin: 0; color: #FFFFFF;'>PlotterGuru</h2>",
        unsafe_allow_html=True,
    )
    st.caption("⚡ v1.2 | Data Science  & Tabular Data Workbench")

    st.markdown("<br>", unsafe_allow_html=True)

    # Card 1: Quick Start Guide
    st.markdown(
        """
        <div class="tech-card">
            <div class="tech-header">
                🚀 <span>Quick Start</span>
            </div>
            <div class="tech-step">
                <div class="step-num">1</div>
                <div><b>Upload</b> dataset or click <i>Sample Dataset</i>.</div>
            </div>
            <div class="tech-step">
                <div class="step-num">2</div>
                <div>Check health & missing values in <b>Diagnostics</b>.</div>
            </div>
            <div class="tech-step">
                <div class="step-num">3</div>
                <div>Calculate median, MAD, & <b>NMAD</b> in <b>Analytics</b>.</div>
            </div>
            <div class="tech-step">
                <div class="step-num">4</div>
                <div>Plot heatmaps & scatter plots in <b>Smart Visuals</b>.</div>
            </div>
            <div class="tech-step">
                <div class="step-num">5</div>
                <div>Deduplicate & export in <b>1-Click Cleaner</b>.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Card 2: Supported Formats
    st.markdown(
        """
        <div class="tech-card">
            <div class="tech-header" style="color: #B39DDB; text-shadow: 0 0 10px rgba(179, 157, 219, 0.3);">
                ⚙️ <span>Supported Formats</span>
            </div>
            <div class="tech-pill-container">
                <span class="tech-pill">CSV</span>
                <span class="tech-pill">TSV</span>
                <span class="tech-pill">DAT</span>
                <span class="tech-pill">TXT</span>
                <span class="tech-pill">XLSX</span>
                <span class="tech-pill">Parquet</span>
                <span class="tech-pill">JSON</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
