import pandas as pd
from io import BytesIO

def load_data(uploaded_file):
    file_name = uploaded_file.name
    file_content = uploaded_file.read()
    file_buffer = BytesIO(file_content)
    
    if file_name.endswith('.csv'):
        return pd.read_csv(file_buffer)
    elif file_name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_buffer)
    else:
        raise ValueError("Unsupported file format. Please use CSV or Excel.")

def preprocess_data(df, review_column=None):
    if review_column is None:
        possible_review_columns = ['review', 'comment', 'feedback', 'text', 'content']
        for col in possible_review_columns:
            if col in df.columns:
                review_column = col
                break
        if review_column is None:
            text_columns = df.select_dtypes(include=['object']).columns
            if len(text_columns) > 0:
                review_column = max(text_columns, key=lambda x: df[x].str.len().mean())
    
    if review_column is None or review_column not in df.columns:
        raise ValueError("Could not identify a suitable review column. Please specify the column name.")
    
    return df[[review_column]].rename(columns={review_column: 'review'})

def get_column_names(df):
    return df.columns.tolist()