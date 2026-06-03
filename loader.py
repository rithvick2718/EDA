import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


def load_csv():
    while True:
        root = tk.Tk()
        root.withdraw()  # Hide the main Tk window

        path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        root.destroy()

        if not path:
            print("\n❌ No file selected.\n")
            continue

        try:
            df = pd.read_csv(path)

            print(f"\n✓ CSV Loaded Successfully")
            print(f"File: {Path(path).name}\n")

            return df

        except Exception as e:
            print(f"\n❌ Error loading CSV: {e}\n")
def dataset_summary(df):
    rows, cols = df.shape
    summary = {
        "rows": rows,
        "columns": cols,
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_mb": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2),
            2
        )
    }
    return summary
def display_dataset_summary(summary):

    print("=" * 50)
    print("DATASET SUMMARY")
    print("=" * 50)

    print(f"Rows            : {summary['rows']:,}")
    print(f"Columns         : {summary['columns']:,}")
    print(f"Missing Values  : {summary['missing_values']:,}")
    print(f"Duplicate Rows  : {summary['duplicate_rows']:,}")
    print(f"Memory Usage    : {summary['memory_mb']} MB")

    print()