import matplotlib
import pandas as pd

matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def create_pie_chart(
    df: pd.DataFrame,
    column: str,
    is_dark_mode: bool = False,
    max_categories: int = 10,  # Default lowered for pie charts to avoid clutter
) -> FigureCanvas:

    # Define theme colors
    bg_color = "#1E1E1E" if is_dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if is_dark_mode else "#000000"
    grid_color = "#444444" if is_dark_mode else "#DDDDDD"

    # Setup figure and axes
    # Note: dpi=150 is usually sufficient. 1500 can cause severe memory issues in GUIs.
    fig = Figure(figsize=(8, 5), dpi=100)
    fig.patch.set_facecolor(bg_color)

    ax = fig.add_subplot(111)
    ax.set_facecolor(bg_color)

    # Get category counts
    original_counts = df[column].dropna().value_counts()
    counts = original_counts.copy()

    # Limit categories and group remainder into "Other"
    if len(counts) > max_categories:
        top_counts = counts.head(max_categories - 1)
        other_sum = counts.iloc[max_categories - 1:].sum()
        other_series = pd.Series({f"Other ({len(counts) - max_categories + 1})": other_sum})
        counts = pd.concat([top_counts, other_series])

    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index.astype(str),
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={
            'edgecolor': bg_color, # Use bg_color for clean separation between slices
            'linewidth': 1.5,
            'alpha': 0.85
        },
        textprops={'color': text_color}
    )

    # Styling
    ax.set_title(f"Pie Chart of {column}", color=text_color, pad=20)
    
    # Ensure pie is drawn as a circle
    ax.axis('equal')  

    # Statistics (Calculated from original_counts to ensure accuracy)
    unique_categories = df[column].nunique(dropna=True)

    if len(original_counts) > 0:
        most_common = original_counts.idxmax()
        most_common_count = original_counts.max()

        least_common = original_counts.idxmin()
        least_common_count = original_counts.min()

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

        # Adjusted position slightly to not overlap with pie chart labels
        ax.text(
            1.15,
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