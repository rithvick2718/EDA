# correlation_analysis.py

import matplotlib.pyplot as plt
import seaborn as sns


def correlation_analysis(df, columns):

    corr = df[columns].corr()

    print("\n" + "=" * 60)
    print("CORRELATION MATRIX")
    print("=" * 60)

    print(corr.round(3))

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0
    )

    plt.title("Correlation Heatmap")

    plt.tight_layout()
    plt.show()


def run_correlation(df, profile):

    numeric_cols = [
        col
        for col, info in profile.items()
        if info["type"] == "Numerical"
    ]

    if len(numeric_cols) < 2:
        print(
            "\n❌ Need at least 2 numerical columns "
            "for correlation analysis.\n"
        )
        return

    print("\nNumerical Columns\n")

    for idx, col in enumerate(numeric_cols, start=1):
        print(f"{idx}. {col}")

    print(
        "\nEnter column numbers separated by commas "
        "(e.g. 1,2,3,4)"
    )

    while True:

        try:

            choices = input("\nColumns: ")

            indices = [
                int(x.strip())
                for x in choices.split(",")
            ]

            if len(indices) < 2:
                raise ValueError

            selected_cols = [
                numeric_cols[i - 1]
                for i in indices
            ]

            break

        except (ValueError, IndexError):

            print(
                "Invalid selection. "
                "Choose at least 2 valid columns."
            )

    correlation_analysis(
        df,
        selected_cols
    )