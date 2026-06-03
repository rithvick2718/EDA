#univariate.py
import matplotlib.pyplot as plt
import seaborn as sns

def numerical_analysis(df, col):

    x = df[col].dropna()

    print("\n" + "=" * 40)
    print(f"{col} (Numerical)")
    print("=" * 40)

    print(f"Count   : {x.count():,}")
    print(f"Mean    : {x.mean():.2f}")
    print(f"Median  : {x.median():.2f}")
    print(f"Std Dev : {x.std():.2f}")
    print(f"Min     : {x.min():.2f}")
    print(f"Max     : {x.max():.2f}")

    plt.figure(figsize=(8, 5))

    sns.histplot(x=x, kde=True)

    plt.axvline(
        x.mean(),
        linestyle="--",
        label=f"Mean = {x.mean():.2f}"
    )

    plt.axvline(
        x.median(),
        linestyle="-.",
        label=f"Median = {x.median():.2f}"
    )

    plt.title(col)
    plt.legend()

    plt.show()

def categorical_analysis(df, col):

    x = df[col]

    print("\n" + "=" * 40)
    print(f"{col} (Categorical)")
    print("=" * 40)

    counts = x.value_counts(dropna=False)

    for category, count in counts.items():

        pct = count / len(x) * 100

        print(
            f"{str(category):<20}"
            f"{count:>6} "
            f"({pct:.1f}%)"
        )

    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x=col,
        order=x.value_counts().index
    )

    plt.title(col)
    plt.xticks(rotation=45)

    plt.show()

def run_univariate(df, profile):

    print("\nSelect a column:\n")

    columns = list(profile.keys())

    for idx, col in enumerate(columns, start=1):
        print(f"{idx}. {col} ({profile[col]['type']})")

    while True:

        try:
            choice = int(input("\nChoice: "))

            if 1 <= choice <= len(columns):
                break

        except ValueError:
            pass

        print("Invalid choice.")

    selected_col = columns[choice - 1]
    col_type = profile[selected_col]["type"]

    if col_type == "Numerical":
        numerical_analysis(df, selected_col)

    else:
        categorical_analysis(df, selected_col)