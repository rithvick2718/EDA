
# 📊 EDA Analysis Dashboard

A fast, interactive, and beautifully designed Exploratory Data Analysis (EDA) desktop application built with Python and PySide6.

This application allows users to upload datasets, instantly profile columns, and generate high-quality Matplotlib visualizations through an intuitive graphical interface. It features a central dashboard where analysts can save their favorite graphs and export them as high-resolution images.

## ✨ Features

* **Intelligent Data Profiling:** Automatically detects Categorical vs. Numerical columns, calculates missing values, and tracks memory usage.
* **Univariate Analysis:** Instantly generate Histograms, Bar Plots, and Pie Charts based on the selected variable's data type.
* **Bivariate Analysis:** Explore relationships using Scatter Plots (Num vs Num), Categorical Bar Plots (Cat vs Num), and Stacked/Grouped Bar Charts (Cat vs Cat).
* **Correlation Heatmaps:** Automatically compute and visualize Pearson correlation coefficients across all numerical variables.
* **Dashboard Gallery:** A "shopping cart" style home page where users can save important graphs, review them in a grid layout, and remove discarded ones.
* **High-Res Exporting:** Export any saved graph from the dashboard as a high-quality PNG or SVG file.
* **Native Dark Mode:** Seamlessly integrates with system dark mode settings for a comfortable viewing experience.

## 🛠️ Tech Stack

* **GUI Framework:** [PySide6](https://doc.qt.io/qtforpython-6/) (Qt for Python)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Data Visualization:** [Matplotlib](https://matplotlib.org/)
* **Executable Build:** [PyInstaller](https://pyinstaller.org/en/stable/)

## 📂 Project Structure

```text
├── main.py                  # Application entry point
├── loader.py                # CSV loading and error handling logic
├── profiler.py              # Dataset column typing and profiling logic
├── dark_mode.py             # System theme detection
├── resource_path.py         # PyInstaller absolute path management
│
├── UI/                      # User Interface Layouts
│   ├── main_window.py       # Core application shell and sidebar logic
│   ├── welcome_window.py    # Initial landing screen
│   └── Pages/               # QStackedWidget Pages
│       ├── home.py               # Dashboard Gallery
│       ├── univariate_page.py    # Single variable analysis
│       ├── bivariate_page.py     # Two-variable relationship analysis
│       └── correlation.py        # Heatmap analysis
│
├── Plots/                   # Matplotlib Figure Canvas Generators
│   ├── histogram.py
│   ├── barplot.py
│   ├── piechart.py
│   ├── scatter.py
│   ├── catplot.py
│   └── heatmap.py
│
└── Icons/                   # Application icon assets

```

## 🚀 Running from Source

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd <repository-folder>

```

**2. Install dependencies**
Ensure you have Python 3.8+ installed, then run:

```bash
pip install PySide6 pandas matplotlib numpy

```

**3. Run the application**

```bash
python main.py

```

## 📦 Compiling to an Executable (.exe)

This project is fully configured to be compiled into a standalone Windows executable using PyInstaller.

**1. Install PyInstaller**

```bash
pip install pyinstaller

```

**2. Build the Application**
Run the following command from the root directory. This uses the `--onedir` flag to ensure fast startup times for heavy data-science libraries:

```bash
pyinstaller --noconsole --onedir --name "EDA_Dashboard" --icon="Icons/favicon.ico" --add-data "Icons;Icons" main.py

```

**3. Locate your Build**
Once finished, navigate to the newly created `dist/EDA_Dashboard` folder. Double-click `EDA_Dashboard.exe` to launch the app!

## 💡 Usage Guide

1. **Upload Data:** Click `File -> Upload CSV` or use the `Ctrl+N` shortcut to load a dataset.
2. **Analyze:** Use the left sidebar to navigate between Univariate, Bivariate, and Correlation analysis tools.
3. **Select Variables:** Use the dropdown menus to select your variables. The UI will dynamically adjust the available plot types (e.g., hiding pie charts for numerical data).
4. **Save Insights:** Click **"Save to Dashboard"** on any graph you find valuable.
5. **Export:** Navigate back to the **Dashboard (Home)** to view all your saved graphs. Click **Export** to save them to your local drive as crisp `300 DPI` PNG or SVG files.