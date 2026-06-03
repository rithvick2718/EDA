# utils.py

import os


def clear_screen():
    """
    Clear terminal screen.
    """

    os.system("cls" if os.name == "nt" else "clear")


def separator(length=60):
    """
    Print a separator line.
    """

    print("-" * length)


def title(text, length=60):
    """
    Print a section title.
    """

    print("=" * length)
    print(text.upper())
    print("=" * length)


def pause():
    """
    Wait for user input.
    """

    input("\nPress Enter to continue...")


def get_choice(prompt, valid_choices):
    """
    Repeatedly ask user for a valid choice.

    Example:
        choice = get_choice(
            "Enter option: ",
            ["1", "2", "3"]
        )
    """

    while True:

        choice = input(prompt).strip()

        if choice in valid_choices:
            return choice

        print("Invalid choice. Try again.")