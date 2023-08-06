from sklearn.linear_model import SGDClassifier, SGDRegressor


def classifier(**params):
    model = SGDClassifier(**params)
    return model


def classifier_params():
    params = SGDClassifier().get_params()
    return params


def regression(**params):
    model = SGDRegressor(**params)
    return model


def regression_params():
    params = SGDRegressor().get_params()
    return params
