from sklearn.ensemble import BaggingClassifier, BaggingRegressor


def classifier(**params):
    model = BaggingClassifier(**params)
    return model


def classifier_params():
    params = BaggingClassifier().get_params()
    return params


def regression(**params):
    model = BaggingRegressor(**params)
    return model


def regression_params():
    params = BaggingRegressor().get_params()
    return params
