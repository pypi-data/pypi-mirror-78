from sklearn.linear_model import PassiveAggressiveClassifier, PassiveAggressiveRegressor


def classifier(**params):
    model = PassiveAggressiveClassifier(**params)
    return model


def classifier_params():
    params = PassiveAggressiveClassifier().get_params()
    return params


def regression(**params):
    model = PassiveAggressiveRegressor(**params)
    return model


def regression_params():
    params = PassiveAggressiveRegressor().get_params()
    return params
