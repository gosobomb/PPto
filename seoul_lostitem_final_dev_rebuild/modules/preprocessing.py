import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle

def preprocess_data(df_raw):
    df = df_raw.dropna().reset_index(drop=True)

    # 날짜 형식 처리 (timestamp로 변환)
    if 'reg_date' in df.columns:
        df['reg_date'] = pd.to_datetime(df['reg_date'], format="%Y/%m/%d", errors="coerce")
        df['reg_date'] = df['reg_date'].astype('int64', errors='ignore') // 10**9  # 초단위로 통일

    if 'rcv_date' in df.columns:
        df['rcv_date'] = pd.to_datetime(df['rcv_date'], format="%Y/%m/%d", errors="coerce")
        df['rcv_date'] = df['rcv_date'].astype('int64', errors='ignore') // 10**9

    # 라벨 인코딩 + 저장용 딕셔너리
    label_encoders = {}

    for col in df.columns:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le

    # label_encoders 저장
    with open("label_encoders.pkl", "wb") as f:
        pickle.dump(label_encoders, f)

    return df