import warnings
from models import support_vector_machine, light_gbm, decision_tree, random_forest
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from bayes_opt import BayesianOptimization
from processing import splitting

warnings.filterwarnings("ignore")


## Overview:
# This code contains a generalised code for Bayesian Optimization.
# The user needs to send the parameter names with range of values and data types
# in the form of a dictionary. The output of this code are optimized parameters.

# General function to be passed in BayesianOptimization.
# Input: Parameters selected by user
# Output: Cross validation score
# Dependencies: col_types
def optimise(**changes):
    for key1, value1 in changes.items():
        for key2, value2 in col_types.items():
            if key1 == key2:
                params[key1] = value2(value1)
                break
    model = model_name.classifier(**params)
    score = cross_val_score(model, x_train, y_train)
    for i in score:
        if str(i) == 'nan':
            val = 0
        else:
            val = score.mean()
    return val


# All the val_{} functions are defining col_types and changed parameters.
# These need to be set by the user or can be taken in the form of json.
def val_light_gbm():
    col_types = {'num_leaves': int, 'max_depth': int, 'lambda_l2': float,
                 'lambda_l1': float,
                 'min_child_samples': int,
                 'min_data_in_leaf': int
        , 'verbose': int
                 }
    change_params = {'num_leaves': (25, 4000),
                     'max_depth': (5, 63),
                     'lambda_l2': (0.0, 0.05),
                     'lambda_l1': (0.0, 0.05),
                     'min_child_samples': (50, 10000),
                     'min_data_in_leaf': (100, 2000),
                     'verbose': (2, 5)
                     }
    return col_types, change_params


def val_svm():
    col_types = {'degree': float, 'tol': float, 'max_iter': int}
    change_params = {'degree': (1, 5), 'tot': (0.001, 0.005), 'max_iter': (1, 3)}
    return col_types, change_params


def val_rf():
    col_types = {'max_leaf_nodes': int, 'max_depth': int, 'min_samples_split': int}
    change_params = {'max_leaf_nodes': (1, 5), 'max_depth': (1, 5), 'min_samples_split': (1, 5)}
    return col_types, change_params


def val_dec_tree():
    col_types = {'max_leaf_nodes': int, 'max_depth': int, 'min_samples_split': int}
    change_params = {'max_leaf_nodes': (1, 5), 'max_depth': (1, 5), 'min_samples_split': (1, 5)}
    return col_types, change_params


if __name__ == '__main__':
    model_name = random_forest  # set this
    data = load_iris().data
    label = load_iris().target
    x_train, x_test, y_train, y_test = splitting.split_data(data, label)
    params = model_name.classifier_params()
    print(params)
    col_types, change_params = val_rf()  # set this
    opt = BayesianOptimization(optimise, change_params)
    opt.maximize(n_iter=3, init_points=2)  # set this
    print(opt.max)
