import pandas as pd
import os

def load_csv_data(file_path):
    """
    Attempts to read a CSV file into a pandas DataFrame.
    
    Returns:
        tuple: (DataFrame, error_message)
        If successful, returns (df, None).
        If failed, returns (None, "Error description").
    """
    # 1. Validate the file path
    if not file_path:
        return None, "No file path was provided."

    if not os.path.exists(file_path):
        return None, "The selected file does not exist or was moved."

    if not file_path.lower().endswith('.csv'):
        return None, "Invalid file type. Please ensure you select a .csv file."

    # 2. Attempt to parse the data
    try:
        # Read the CSV into a pandas DataFrame
        df = pd.read_csv(file_path)
        
        # Check if the file has a header but no actual rows of data
        if df.empty:
            return None, "The CSV file was loaded, but it contains no data rows."
            
        return df, None

    # 3. Catch specific pandas and system errors
    except pd.errors.EmptyDataError:
        return None, "The CSV file is completely empty."
    except pd.errors.ParserError:
        return None, "Formatting issue detected. The CSV has irregular columns or malformed rows."
    except UnicodeDecodeError:
        return None, "Encoding error. Please ensure the CSV is saved using UTF-8 encoding."
    except Exception as e:
        return None, f"An unexpected error occurred while loading the file:\n{str(e)}"