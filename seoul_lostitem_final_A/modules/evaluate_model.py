
from sklearn.metrics import accuracy_score

def evaluate_model(test_target, test_pred):
    acc = accuracy_score(test_target, test_pred)
    return {'accuracy': acc}
