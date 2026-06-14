import matplotlib
import pandas as pd

matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def create_bar_plot(
    df: pd.DataFrame,
    column: str,
    is_dark_mode: bool = False,
    max_categories: int = 25,
    bar_color: str = "#4A90E2"
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

    # Get category counts
    counts = df[column].dropna().value_counts()

    # Limit categories if too many
    if len(counts) > max_categories:
        counts = counts.head(max_categories)

    # Create bar plot
    ax.bar(
        counts.index.astype(str),
        counts.values,
        color=bar_color,
        edgecolor=text_color,
        alpha=0.8
    )

    # Styling
    ax.set_title(f"Bar Plot of {column}", color=text_color)
    ax.set_xlabel(column, color=text_color)
    ax.set_ylabel("Count", color=text_color)

    ax.tick_params(axis='x', colors=text_color, rotation=45)
    ax.tick_params(axis='y', colors=text_color)

    for spine in ax.spines.values():
        spine.set_color(text_color)

    ax.grid(True, axis='y', linestyle='--', alpha=0.5, color=grid_color)

    # Statistics
    unique_categories = df[column].nunique(dropna=True)

    if len(counts) > 0:
        most_common = counts.idxmax()
        most_common_count = counts.max()

        least_common = counts.idxmin()
        least_common_count = counts.min()

        stats_text = (
            f"Unique Categories: {unique_categories}\n"
            f"Most Common:\n"
            f"{most_common} ({most_common_count})\n"
            f"Least Common:\n"
            f"{least_common} ({least_common_count})"
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