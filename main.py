# main.py

from loader import load_csv, dataset_summary, display_dataset_summary
from profiler import profile_dataset, display_profile
from utils import title, pause, clear_screen, get_choice
from univariate import run_univariate
from bivariate import run_bivariate
from correlation_analysis import run_correlation


def main():
    clear_screen()
    title("Terminal EDA Analyzer")

    df = load_csv()
    summary = dataset_summary(df)
    display_dataset_summary(summary)

    profile = profile_dataset(df)
    display_profile(profile)

    while True:
        print("Select an option:\n")
        print("1. Univariate Analysis")
        print("2. Bivariate Analysis")
        print("3. Correlation Analysis")
        print("4. Missing Value Report")
        print("5. Generate Full EDA Report")
        print("6. Exit")

        choice = get_choice("\nChoice: ", ["1", "2", "3", "4", "5", "6"])

        clear_screen()
        title("Terminal EDA Analyzer")

        if choice == "1":
            run_univariate(df, profile)
            pause()

        elif choice == "2":
            run_bivariate(df, profile)
            pause()

        elif choice == "3":
            run_correlation(df, profile)
            pause()

        elif choice == "4":
            print("Missing Value Report not implemented yet.")
            pause()

        elif choice == "5":
            print("Full EDA Report not implemented yet.")
            pause()

        elif choice == "6":
            print("\nGoodbye!")
            break

        clear_screen()
        title("Terminal EDA Analyzer")


if __name__ == "__main__":
    main()