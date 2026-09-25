# PlotterGuru Web App Documentation

## Table of Contents
1. [Overview](#overview)
2. [Live Demo](#live-demo)
3. [Key Features](#key-features)
4. [Supported Data Formats](#supported-data-formats)
5. [Usage Guide](#usage-guide)
6. [FAQ](#faq)
7. [For Developers](#for-developers)
8. [Contributing](#contributing)
9. [License](#license)
10. [Credits & Contact](#credits--contact)

---

## Overview
PlotterGuru is a browser-based Streamlit web app for exploring, diagnosing, cleaning, and visualising tabular datasets from any domain. With support for a wide variety of file formats and advanced analytics, PlotterGuru makes data understanding accessible, interactive, and precise.

---

## Live Demo
🌐 **Try PlotterGuru Instantly:**
[https://data-guru.streamlit.app/](https://data-guru.streamlit.app/)

No installation required; just open the link and start exploring your data!

---

## Key Features
- **Precision Handling**: Correctly displays and analyses floating-point scales as small as 10⁻¹², preventing display round-off errors.
- **Density-Colored Scatter Mapping**: Visualise point density in 2D scatter plots using Gaussian KDE and WebGL rendering.
- **Absolute Deviation Diagnostics**: Compute and plot Median, MAD, and NMAD for any column.
- **Versatile Visualisation Suite**: Histograms, bar charts, box plots, scatter, and density maps, with options for log scaling and customisation.
- **Data Health Diagnostics**: Instantly view missing values, duplicates, and summary statistics.
- **1-Click Data Cleaner**: Remove duplicates, drop rows with missing values, and export cleaned data.
- **Dark Mode UI**: Modern, distraction-free interface for long analytical sessions.

---

## Supported Data Formats
- CSV, TSV, DAT, TXT
- Excel (XLSX)
- Parquet
- JSON

---

## Usage Guide
1. **Open the Web App:** [https://data-guru.streamlit.app/](https://data-guru.streamlit.app/)
2. **Upload Your Dataset:** Use the sidebar to upload your file, or select the sample dataset provided.
3. **Explore Data Health:** View summary stats, missing values, and duplicates at a glance.
4. **Analyse Columns:** Select any column for in-depth metrics (mean, median, MAD, NMAD) and absolute deviation plots.
5. **Visualise Data:** Choose from a range of plots, histograms, bar, box, scatter, or density maps.
6. **Clean Data:** Use 1-click cleaning tools, then export your cleaned dataset if needed.
7. All features are accessible directly from the browser; no code required!

---

## FAQ
**Q: Do I need to install anything?**  
A: No. Just use the web app; no local install is needed for normal use.

**Q: Is my data private?**  
A: Data is processed in memory and not stored after your session ends. For highly sensitive data, run PlotterGuru locally (see developer section).

**Q: What file sizes can I upload?**  
A: The app is optimised for moderate-sized tabular datasets. Very large files may be limited by browser or Streamlit Cloud constraints.

---

## For Developers
If you wish to contribute, run PlotterGuru locally or extend its features:

### Local Installation
- Python 3.8+
- pip

#### Steps
```bash
git clone https://github.com/yourusername/plotterguru.git
cd plotterguru
pip install -r requirements.txt
# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
