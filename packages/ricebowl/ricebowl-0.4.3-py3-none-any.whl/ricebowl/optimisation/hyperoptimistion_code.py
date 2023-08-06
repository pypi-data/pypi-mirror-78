from models import light_gbm, random_forest, support_vector_machine
from sklearn.datasets import load_iris
from hyperopt import fmin, tpe, hp, Trials,space_eval
from processing import splitting
from sklearn.model_selection import KFold, cross_val_score


def changeme(changes, col_types):
    for k1, v1 in changes.items():
        for k2, v2 in col_types.items():
            if k1 == k2:
                for i in range(len(v1)):
                    v1[i] = v2(v1[i])
    return changes


def optimised(changes):
    model = model_name.classifier(**params)
    score = cross_val_score(model, x_train, y_train, cv=fold(), scoring="neg_mean_squared_error",
                            n_jobs=-1).mean()
    return score


def fold():
    num_folds = 5
    kf = KFold(n_splits=num_folds, random_state=7)
    return kf


def light_gb():
    col_types = {'max_depth': int, 'lambda_l2': float,
                 'lambda_l1': float, 'min_child_samples': int, 'min_data_in_leaf': int,
                 'verbose': int,
                 'n_estimators': int}
    params = {'max_depth': [5, 63], 'lambda_l2': [0.0, 0.05], 'lambda_l1': [0.0, 0.05],
              'min_child_samples': [50, 10000], 'min_data_in_leaf': [100, 2000], 'verbose': [2, 5],
              'n_estimators': [100, 2000]}
    return col_types, params


def rf():
    col_types = {'max_leaf_nodes': int, 'max_depth': int, 'min_samples_split': int}
    change_params = {'max_leaf_nodes': [1, 5], 'max_depth': [1, 5], 'min_samples_split': [1, 5]}
    return col_types, change_params


def sv_classifier():
    col_types = { 'kernel': str, 'degree': int, 'cache_size': int,'verbose': str }
    params = { 'kernel': ['rbf', 'Sigmoid','linear'], 'degree': [3, 7], 'cache_size': [200, 400],  'verbose':['True','False']}
    return col_types, params


def make_dict(changes):

    space = {}
    for k, v in changes.items():
        if type(v[0]) == int and type(v[1]) == int:
            space[k] = hp.quniform(str(k), v[0], v[1], 1)
        elif type(v[0]) == str:
            space[k] = hp.choice(str(k), v)
        elif type(v[0]) == float or type(v[1]) == float:
            space[k] = hp.lognormal(str(k), v[0], v[1])
        else:
            space[k] = hp.loguniform(str(k), v[0], v[1])
    return space


if __name__ == '__main__':
    n_iter = 50
    model_name = support_vector_machine
    data = load_iris().data
    target = load_iris().target
    x_train, x_test, y_train, y_test = splitting.split_data(data, target)
    params = model_name.classifier_params()  ## for regression and classification change params here
    col_types, change_params = sv_classifier()
    change_params = changeme(change_params, col_types)
    space = make_dict(change_params)
    trials = Trials()
    best = fmin(fn=optimised,  # function to optimize
                space=space,
                algo=tpe.suggest,
                max_evals=n_iter,  # maximum number of iterations
                trials=trials  # logging
                )

    hyp= space_eval(space,best)
    print(hyp)





