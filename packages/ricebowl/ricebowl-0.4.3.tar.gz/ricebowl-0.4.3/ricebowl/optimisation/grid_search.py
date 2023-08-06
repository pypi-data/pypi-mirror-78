from sklearn.metrics import make_scorer, r2_score
from math import sqrt
from sklearn.model_selection import GridSearchCV
import warnings
from models import support_vector_machine, light_gbm, decision_tree, random_forest
from sklearn.datasets import load_iris
from processing import splitting

warnings.filterwarnings("ignore")


## Overview:
# This code contains a generalised code for grid search optimization.
# In the main, add your data,target,model name and
# changed params(dictionary with possible values for each key).
# Using grid search you will be able to see the optimized parameters.

# Defining our custom loss func for R2
def my_custom_loss_func(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    return r2


# Function to search for best parameters based on R2 scoring
def grid_search(x_train, y_train, model, params):
    score = make_scorer(my_custom_loss_func, greater_is_better=False)
    # Using grid search for best parameters
    grid = GridSearchCV(model, param_grid=params, scoring=score, n_jobs=None, cv=5)
    grid_result = grid.fit(x_train, y_train)
    return grid_result.best_params_


if __name__ == '__main__':
    data = load_iris().data  # set this
    label = load_iris().target  # set this
    model_name = support_vector_machine
    x_train, x_test, y_train, y_test = splitting.split_data(data, label)
    params = support_vector_machine.classifier_params()
    change_params = {'degree': [88, 2222, 8, 2, 4, 111111, 35, 12],
                     'tol': [0.07, 0.010, 0.001, 0.005, 0.09, 0.11, 5],
                     'max_iter': [7.0, 8.0, 11, 15, 20.0, 50.0],
                     'kernel': ['linear', 'poly', 'rbf']}  # set this
    model = model_name.classifier(**params)

    optimized_params = grid_search(x_train, y_train, model, change_params)
    print('-------------Changed Params---------')
    print(change_params)
    print('--------------------Optimised Params----------------')
    print(optimized_params)
