
from sklearn.ensemble import RandomForestClassifier

def train_model(train_input, train_target):
    model = RandomForestClassifier(random_state=42)
    model.fit(train_input, train_target)
    return model
