
def is_model_passed(metrics, accuracy_threshold=0.8):
    return metrics['accuracy'] >= accuracy_threshold
