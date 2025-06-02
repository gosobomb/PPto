
from sklearn.model_selection import train_test_split

def feature_split(df, target_column, test_size=0.2):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=42)
