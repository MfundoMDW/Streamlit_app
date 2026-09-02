\# 🌌 PlotterGuru



\*\*PlotterGuru\*\* is a Streamlit application built for exploring, diagnosing, and visualizing large-scale astronomical and tabular scientific datasets. It handles extreme floating-point scales (down to $10^{-12}$) without precision loss or round-off truncation, features dynamic point-density mapping and absolute deviation diagnostics.



\---



\## ⚡ Key Features



\* \*\*🔬 Scientific Precision Handling:\*\* Automatic formatting (`.6e` / `.2e`) for microscopic floating-point scales ($10^{-12}$), preventing display round-off errors across metrics and axis ticks.

\* \*\*🌌 Density-Colored Scatter Mapping:\*\* Calculates 2D Gaussian Kernel Density Estimation (KDE) to dynamically color scatter points based on local spatial density using WebGL (`go.Scattergl`).

\* \*\*📐 Absolute Deviation Diagnostics (NMAD):\*\* Calculates Median, Median Absolute Deviation (MAD), and Normalized MAD (NMAD) with staggered, color-coded Plotly vertical annotations.

\* \*\*📊 Multi-Distribution Suite:\*\* Custom visualization modes supporting Histograms (filled/unfilled outlines), Bar Charts, and Box Plots with logarithmic axis scaling toggles.

\* \*\*🌑 Dark-Mode Native UI:\*\* Optimized layout designed for long analytical workflows with clean diagnostics and interactive sampling options.



\---



\## 🛠️ Tech Stack



\* \*\*Framework:\*\* \[Streamlit](https://streamlit.io/)

\* \*\*Data Processing:\*\* \[Pandas](https://pandas.pydata.org/), \[NumPy](https://numpy.org/)

\* \*\*Scientific Computing:\*\* \[SciPy](https://scipy.org/) (`scipy.stats.gaussian\_kde`)

\* \*\*Interactive Graphics:\*\* \[Plotly Express \& Graph Objects](https://plotly.com/python/) (WebGL rendering)



\---



