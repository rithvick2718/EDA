import matplotlib
import pandas as pd
import numpy as np

matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.cm as cm

def create_cat_v_num(
    df: pd.DataFrame,
    cat_col: str,
    num_col: str,
    is_dark_mode: bool = False,
    max_categories: int = 25,
    bar_color: str = "#4A90E2"
) -> FigureCanvas:
    
    # Define theme colors
    bg_color = "#1E1E1E" if is_dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if is_dark_mode else "#000000"
    grid_color = "#444444" if is_dark_mode else "#DDDDDD"

    # Setup figure and axes (Defaulted to 100 DPI for GUI performance)
    fig = Figure(figsize=(8, 5), dpi=100)
    fig.patch.set_facecolor(bg_color)

    ax = fig.add_subplot(111)
    ax.set_facecolor(bg_color)

    # Aggregate: sum the numerical column grouped by categorical
    agg_df = df.groupby(cat_col)[num_col].sum().dropna()

    # Sort and limit categories if too many
    agg_df = agg_df.sort_values(ascending=False)
    if len(agg_df) > max_categories:
        agg_df = agg_df.head(max_categories)

    # Create bar plot
    ax.bar(
        agg_df.index.astype(str),
        agg_df.values,
        color=bar_color,
        edgecolor=text_color,
        alpha=0.8
    )

    # Styling
    ax.set_title(f"Sum of {num_col} by {cat_col}", color=text_color)
    ax.set_xlabel(cat_col, color=text_color)
    ax.set_ylabel(f"Total {num_col}", color=text_color)

    ax.tick_params(axis='x', colors=text_color, rotation=45)
    ax.tick_params(axis='y', colors=text_color)

    for spine in ax.spines.values():
        spine.set_color(text_color)

    ax.grid(True, axis='y', linestyle='--', alpha=0.5, color=grid_color)

    # Statistics Box
    unique_categories = df[cat_col].nunique(dropna=True)

    if len(agg_df) > 0:
        highest_cat = agg_df.idxmax()
        highest_val = agg_df.max()

        lowest_cat = agg_df.idxmin()
        lowest_val = agg_df.min()

        stats_text = (
            f"Unique Categories: {unique_categories}\n"
            f"Highest Sum:\n"
            f"{highest_cat} ({highest_val:g})\n"
            f"Lowest Sum:\n"
            f"{lowest_cat} ({lowest_val:g})"
        )

        props = dict(
            boxstyle='round',
            facecolor=bg_color,
            alpha=0.9,
            edgecolor=grid_color
        )

        ax.text(
            0.95,
            0.95,
            stats_text,
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=props,
            color=text_color
        )

    fig.tight_layout()
    return FigureCanvas(fig)


def create_cat_v_cat(
    df: pd.DataFrame,
    cat_col1: str,
    cat_col2: str,
    is_dark_mode: bool = False,
    max_categories: int = 15,  # Slightly lower default to prevent clustered overlapping 
    stacked: bool = False      # Set to True for overlayed (stacked), False for grouped
) -> FigureCanvas:
    
    # Define theme colors
    bg_color = "#1E1E1E" if is_dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if is_dark_mode else "#000000"
    grid_color = "#444444" if is_dark_mode else "#DDDDDD"

    # Setup figure and axes
    fig = Figure(figsize=(8, 5), dpi=100)
    fig.patch.set_facecolor(bg_color)

    ax = fig.add_subplot(111)
    ax.set_facecolor(bg_color)

    # Determine top categories for the primary x-axis to prevent clutter
    top_cats = df[cat_col1].value_counts().head(max_categories).index
    filtered_df = df[df[cat_col1].isin(top_cats)]

    # Create cross-tabulation
    crosstab = pd.crosstab(filtered_df[cat_col1], filtered_df[cat_col2])

    # Sort by total frequency for better readability
    crosstab['Total'] = crosstab.sum(axis=1)
    crosstab = crosstab.sort_values('Total', ascending=False).drop('Total', axis=1)

    labels = crosstab.index.astype(str).tolist()
    sub_categories = crosstab.columns.tolist()

    # Create plotting variables
    x = np.arange(len(labels))
    width = 0.8
    num_subcats = len(sub_categories)

    # Use a built-in colormap for distinct sub-category colors
    colors = cm.get_cmap('tab10').colors

    # Plot Logic: Stacked vs Grouped
    if stacked:
        bottoms = np.zeros(len(labels))
        for i, sub_cat in enumerate(sub_categories):
            values = crosstab[sub_cat].values
            ax.bar(
                x,
                values,
                width=width,
                label=str(sub_cat),
                bottom=bottoms,
                color=colors[i % len(colors)],
                edgecolor=text_color,
                alpha=0.8
            )
            bottoms += values
    else:
        bar_width = width / num_subcats
        for i, sub_cat in enumerate(sub_categories):
            # Calculate offset for grouped bars
            offset = (i - num_subcats / 2) * bar_width + bar_width / 2
            ax.bar(
                x + offset,
                crosstab[sub_cat].values,
                width=bar_width,
                label=str(sub_cat),
                color=colors[i % len(colors)],
                edgecolor=text_color,
                alpha=0.8
            )

    # Styling
    ax.set_title(f"Comparison of {cat_col1} by {cat_col2}", color=text_color)
    ax.set_xlabel(cat_col1, color=text_color)
    ax.set_ylabel("Frequency", color=text_color)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.tick_params(axis='x', colors=text_color, rotation=45)
    ax.tick_params(axis='y', colors=text_color)

    for spine in ax.spines.values():
        spine.set_color(text_color)

    ax.grid(True, axis='y', linestyle='--', alpha=0.5, color=grid_color)

    # Ensure legend respects dark mode styling
    legend = ax.legend(title=cat_col2, facecolor=bg_color, edgecolor=grid_color, labelcolor=text_color)
    legend.get_title().set_color(text_color)

    # Statistics Box
    if not crosstab.empty:
        # Find the most common combination overall in the crosstab matrix
        max_idx = crosstab.values.argmax()
        row_idx, col_idx = np.unravel_index(max_idx, crosstab.values.shape)
        top_row = crosstab.index[row_idx]
        top_col = crosstab.columns[col_idx]
        top_val = crosstab.values[row_idx, col_idx]

        stats_text = (
            f"Top X-Axis Cat: {len(labels)}\n"
            f"Sub-categories: {num_subcats}\n"
            f"Most Frequent Combo:\n"
            f"{top_row} & {top_col} ({top_val})"
        )

        props = dict(
            boxstyle='round',
            facecolor=bg_color,
            alpha=0.9,
            edgecolor=grid_color
        )

        ax.text(
            0.95,
            0.95,
            stats_text,
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=props,
            color=text_color
        )

    fig.tight_layout()
    return FigureCanvas(fig)