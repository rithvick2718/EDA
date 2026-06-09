import pandas as pd

def infer_column_type(series, cat_threshold=15):
    non_null = series.dropna()

    if pd.api.types.is_numeric_dtype(non_null):
        return "Numerical"

    n_unique = non_null.nunique()

    if n_unique <= cat_threshold:
        return "Categorical"

    return "Categorical"

def profile_dataset(df):

    profile = {}

    for col in df.columns:

        profile[col] = {
            "type": infer_column_type(df[col]),
            "missing": df[col].isna().sum(),
            "unique": df[col].nunique(dropna=True)
        }

    return profile