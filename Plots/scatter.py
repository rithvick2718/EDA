import matplotlib
import numpy as np
import pandas as pd
import warnings

matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def create_scatter_plot(
    df: pd.DataFrame, 
    x_column: str, 
    y_column: str, 
    is_dark_mode: bool = False, 
    marker_color: str = "#4A90E2",
    marker_size: float = 20.0,
    alpha: float = 0.8
) -> FigureCanvas:
    
    # Define theme colors
    bg_color = "#1E1E1E" if is_dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if is_dark_mode else "#000000"
    grid_color = "#444444" if is_dark_mode else "#DDDDDD"

    # FIX 1: Lower DPI to a reasonable screen resolution to prevent memory/lag issues
    fig = Figure(figsize=(8, 5), dpi=120)
    fig.patch.set_facecolor(bg_color)
    
    ax = fig.add_subplot(111)
    ax.set_facecolor(bg_color)
    
    # FIX 2: Ensure data is numeric and handle NaNs gracefully
    plot_data = df[[x_column, y_column]].copy()
    plot_data[x_column] = pd.to_numeric(plot_data[x_column], errors='coerce')
    plot_data[y_column] = pd.to_numeric(plot_data[y_column], errors='coerce')
    plot_data = plot_data.dropna()
    
    x_data = plot_data[x_column]
    y_data = plot_data[y_column]
    
    # Plot scatter
    ax.scatter(x_data, y_data, color=marker_color, alpha=alpha, s=marker_size)
    
    # Style axes and text
    ax.set_title(f"{y_column} vs {x_column}", color=text_color)
    ax.set_xlabel(x_column, color=text_color)
    ax.set_ylabel(y_column, color=text_color)
    ax.tick_params(colors=text_color)
    
    for spine in ax.spines.values():
        spine.set_color(text_color)
        
    ax.grid(True, linestyle='--', alpha=0.5, color=grid_color)

    # Calculate statistics relevant to scatter plots
    n_points = len(plot_data)
    
    if n_points > 1:
        correlation = x_data.corr(y_data)
        
        # FIX 3: Prevent Polyfit crashes if there is no variance in X
        if x_data.nunique() > 1:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', np.exceptions.RankWarning)
                slope, intercept = np.polyfit(x_data, y_data, 1)
            
            stats_text = (
                f"N: {n_points}\n"
                f"Correlation (r): {correlation:.3f}\n"
                f"Slope: {slope:.3f}\n"
                f"Intercept: {intercept:.3f}"
            )
        else:
             stats_text = (
                f"N: {n_points}\n"
                f"Correlation (r): {correlation:.3f}\n"
                f"Slope: Undefined (Zero X variance)"
            )           
    else:
        stats_text = f"N: {n_points}\nInsufficient data."
    
    # Render stats box
    props = dict(boxstyle='round', facecolor=bg_color, alpha=0.9, edgecolor=grid_color)
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right', 
            bbox=props, color=text_color)

    fig.tight_layout()
    return FigureCanvas(fig)