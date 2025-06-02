
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def improve_model(X_train, y_train):
    param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [5, 10, 20]}
    grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_
