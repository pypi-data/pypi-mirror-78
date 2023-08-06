from sklearn.neural_network import MLPClassifier, MLPRegressor


def classifier(**params):
    model = MLPClassifier(**params)
    return model


def classifier_params():
    params = MLPClassifier().get_params()
    return params


def regression(**params):
    model = MLPRegressor(**params)
    return model


def regression_params():
    params = MLPRegressor().get_params()
    return params
