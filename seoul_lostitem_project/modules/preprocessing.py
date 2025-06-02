import pandas as pd

def preprocess_data(df):
    df = df.dropna()
    df = df.reset_index(drop=True)
    if 'reg_date' in df.columns:
        df['reg_date'] = pd.to_datetime(df['reg_date'], format="%Y/%m/%d", errors="coerce")
    return df