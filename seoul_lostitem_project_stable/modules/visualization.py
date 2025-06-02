
import matplotlib.pyplot as plt
import seaborn as sns

def plot_feature_importances(model, feature_names):
    importances = model.feature_importances_
    sns.barplot(x=importances, y=feature_names)
    plt.title("Feature Importances")
    plt.show()
