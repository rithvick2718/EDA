# bivariate.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def numerical_vs_numerical(df, col1, col2):

    x = df[col1]
    y = df[col2]

    corr = x.corr(y)

    print("\n" + "=" * 50)
    print(f"{col1} vs {col2}")
    print("=" * 50)
    print(f"Correlation : {corr:.3f}")

    plt.figure(figsize=(8, 6))

    sns.scatterplot(
        data=df,
        x=col1,
        y=col2
    )

    plt.title(
        f"{col1} vs {col2}\nCorrelation = {corr:.3f}"
    )

    plt.tight_layout()
    plt.show()


def numerical_vs_categorical(df, num_col, cat_col):

    print("\n" + "=" * 50)
    print(f"{num_col} vs {cat_col}")
    print("=" * 50)

    grouped = (
        df.groupby(cat_col)[num_col]
        .agg(["count", "mean", "median", "std"])
        .round(2)
    )

    print(grouped)

    plt.figure(figsize=(10, 6))

    sns.boxplot(
        data=df,
        x=cat_col,
        y=num_col
    )

    plt.title(f"{num_col} by {cat_col}")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def categorical_vs_categorical(df, col1, col2):

    print("\n" + "=" * 50)
    print(f"{col1} vs {col2}")
    print("=" * 50)

    crosstab = pd.crosstab(
        df[col1],
        df[col2]
    )

    print("\nContingency Table\n")
    print(crosstab)

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        crosstab,
        annot=True,
        fmt="d",
        cmap="Blues"
    )

    plt.title(f"{col1} vs {col2}")

    plt.tight_layout()
    plt.show()


def run_bivariate(df, profile):

    columns = list(profile.keys())

    print("\nSelect First Column\n")

    for idx, col in enumerate(columns, start=1):
        print(f"{idx}. {col} ({profile[col]['type']})")

    while True:

        try:
            choice1 = int(input("\nChoice: "))

            if 1 <= choice1 <= len(columns):
                break

        except ValueError:
            pass

        print("Invalid choice.")

    print("\nSelect Second Column\n")

    for idx, col in enumerate(columns, start=1):
        print(f"{idx}. {col} ({profile[col]['type']})")

    while True:

        try:
            choice2 = int(input("\nChoice: "))

            if (
                1 <= choice2 <= len(columns)
                and choice2 != choice1
            ):
                break

        except ValueError:
            pass

        print("Invalid choice.")

    col1 = columns[choice1 - 1]
    col2 = columns[choice2 - 1]

    type1 = profile[col1]["type"]
    type2 = profile[col2]["type"]

    if (
        type1 == "Numerical"
        and type2 == "Numerical"
    ):

        numerical_vs_numerical(
            df,
            col1,
            col2
        )

    elif (
        type1 == "Numerical"
        and type2 in ["Categorical", "Ordinal"]
    ):

        numerical_vs_categorical(
            df,
            col1,
            col2
        )

    elif (
        type2 == "Numerical"
        and type1 in ["Categorical", "Ordinal"]
    ):

        numerical_vs_categorical(
            df,
            col2,
            col1
        )

    else:

        categorical_vs_categorical(
            df,
            col1,
            col2
        )