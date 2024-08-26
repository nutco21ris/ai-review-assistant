import pandas as pd

def load_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please use CSV or Excel.")

def preprocess_data(df):
    if 'review' not in df.columns:
        raise ValueError("The dataset must contain a 'review' column.")
    return df[['review']].copy()