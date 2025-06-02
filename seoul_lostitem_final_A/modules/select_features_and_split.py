
from sklearn.model_selection import train_test_split

def select_features_and_split(df_cleansed, target_column='storage', test_size=0.2):
    X = df_cleansed.drop(columns=[target_column])
    y = df_cleansed[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=42)
