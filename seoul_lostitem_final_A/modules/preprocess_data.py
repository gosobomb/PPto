
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(df_raw):
    df = df_raw.dropna().reset_index(drop=True)

    if 'reg_date' in df.columns:
        df['reg_date'] = pd.to_datetime(df['reg_date'], format="%Y/%m/%d", errors="coerce")
        df['reg_date'] = df['reg_date'].astype('int64', errors='ignore')

    if 'rcv_date' in df.columns:
        df['rcv_date'] = pd.to_datetime(df['rcv_date'], format="%Y/%m/%d", errors="coerce")
        df['rcv_date'] = df['rcv_date'].astype('int64', errors='ignore')

    for col in df.columns:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

    return df
