import matplotlib
import numpy as np
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

def create_histogram(df: pd.DataFrame, column: str, is_dark_mode: bool = False, bins : int = -1, bar_color: str = "#4A90E2") -> FigureCanvas:    
    # Define theme colors
    bg_color = "#1E1E1E" if is_dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if is_dark_mode else "#000000"
    grid_color = "#444444" if is_dark_mode else "#DDDDDD"

    # Setup figure and axes
    fig = Figure(figsize=(8, 5), dpi=1500)
    fig.patch.set_facecolor(bg_color)
    
    ax = fig.add_subplot(111)
    ax.set_facecolor(bg_color)
    
    data = df[column].dropna()
    
    # Calculate bin count and edge color
    if bins == -1:
        actual_bins = np.histogram_bin_edges(data, bins="auto")
        num_bins = len(actual_bins) - 1 
    else:
        actual_bins = bins
        num_bins = bins

    edge_color = text_color if num_bins <= 50 else None

    # Plot histogram
    ax.hist(data, bins=actual_bins, edgecolor=edge_color, alpha=0.8, color=bar_color)
    
    # Style axes and text
    ax.set_title(f"Histogram of {column}", color=text_color)
    ax.set_xlabel(column, color=text_color)
    ax.set_ylabel("Frequency", color=text_color)
    ax.tick_params(colors=text_color)
    
    for spine in ax.spines.values():
        spine.set_color(text_color)
        
    ax.grid(True, linestyle='--', alpha=0.5, color=grid_color)

    # Calculate statistics
    mean_val = data.mean()
    median_val = data.median()
    std_val = data.std()
    min_val = data.min()
    max_val = data.max()
    
    stats_text = (
        f"Mean: {mean_val:.2f}\n"
        f"Median: {median_val:.2f}\n"
        f"Std Dev: {std_val:.2f}\n"
        f"Min: {min_val:.2f}\n"
        f"Max: {max_val:.2f}"
    )
    
    # Render stats box
    props = dict(boxstyle='round', facecolor=bg_color, alpha=0.9, edgecolor=grid_color)
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right', 
            bbox=props, color=text_color)

    fig.tight_layout()
    return FigureCanvas(fig)