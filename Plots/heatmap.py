import matplotlib
import numpy as np
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

def create_correlation_heatmap(
    df: pd.DataFrame, 
    is_dark_mode: bool = False, 
    cmap: str = "coolwarm",
    annotate: bool = True
) -> FigureCanvas:
    
    # Define theme colors
    bg_color = "#1E1E1E" if is_dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if is_dark_mode else "#000000"
    grid_color = "#444444" if is_dark_mode else "#DDDDDD"

    # Setup figure and axes (slightly taller to accommodate rotated labels)
    fig = Figure(figsize=(9, 6), dpi=1500)
    fig.patch.set_facecolor(bg_color)
    
    ax = fig.add_subplot(111)
    ax.set_facecolor(bg_color)
    
    # Isolate numeric columns and calculate the correlation matrix
    plot_data = df.select_dtypes(include=[np.number])
    corr_matrix = plot_data.corr()
    columns = corr_matrix.columns
    
    # Handle edge case where no numeric data exists
    if len(columns) == 0:
        ax.text(0.5, 0.5, "No numeric data available", color=text_color, 
                ha='center', va='center', fontsize=12, transform=ax.transAxes)
        fig.tight_layout()
        return FigureCanvas(fig)

    # Plot heatmap (-1 to 1 bounds for Pearson correlation)
    im = ax.imshow(corr_matrix, cmap=cmap, vmin=-1, vmax=1, aspect='auto')
    
    # Add and style colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.yaxis.set_tick_params(colors=text_color)
    cbar.outline.set_edgecolor(text_color)
    
    # Style axes and text
    ax.set_title("Correlation Heatmap", color=text_color, pad=15)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(columns)))
    ax.set_yticks(np.arange(len(columns)))
    ax.set_xticklabels(columns, color=text_color, rotation=45, ha="right")
    ax.set_yticklabels(columns, color=text_color)
    
    # Heatmaps shouldn't have gridlines slicing through the cells
    ax.grid(False)
    
    for spine in ax.spines.values():
        spine.set_color(text_color)

    # Annotate cells with correlation values
    if annotate:
        for i in range(len(columns)):
            for j in range(len(columns)):
                val = corr_matrix.iloc[i, j]
                # High absolute values get white text, low values get black text for contrast
                cell_text_color = "white" if abs(val) > 0.5 else "black"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", 
                        color=cell_text_color, fontsize=8)

    # Calculate statistics (find strongest correlation excluding diagonal 1.0s)
    if len(columns) > 1:
        # 1. Create a clean copy of the dataframe
        masked_df = corr_matrix.copy()
        
        # 2. Iterate through the columns and replace the diagonal with NaN
        for col in masked_df.columns:
            masked_df.loc[col, col] = float('nan') 
        
    # Stack to get pairwise, drop NaNs, and find absolute max...        
        # Stack to get pairwise, drop NaNs, and find absolute max
        stacked = masked_df.unstack().dropna()
        max_idx = stacked.abs().idxmax()
        max_val = stacked[max_idx]
        var1, var2 = max_idx
        
        stats_text = (
            f"Variables: {len(columns)}\n"
            f"Strongest Pair:\n"
            f"{var1} & {var2}\n"
            f"r: {max_val:.3f}"
        )
    else:
        stats_text = f"Variables: {len(columns)}\nInsufficient pairs."

    # Render stats box (pushed outside the axes to right side to avoid covering cells)
    props = dict(boxstyle='round', facecolor=bg_color, alpha=0.9, edgecolor=grid_color)
    ax.text(1.25, 1.0, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='left', 
            bbox=props, color=text_color)

    # Adjust layout manually rather than tight_layout so the external text box isn't clipped
    fig.subplots_adjust(left=0.15, right=0.75, bottom=0.2, top=0.9)
    return FigureCanvas(fig)