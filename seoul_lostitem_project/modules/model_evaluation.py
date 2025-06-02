
from sklearn.metrics import accuracy_score

def evaluate_model(y_test, predictions):
    acc = accuracy_score(y_test, predictions)
    return {'accuracy': acc}
