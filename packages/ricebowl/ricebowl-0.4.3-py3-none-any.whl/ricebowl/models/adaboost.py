from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor


def classifier(**params):
    model = AdaBoostClassifier(**params)
    return model


def classifier_params():
    params = AdaBoostClassifier().get_params()
    return params


def regression(**params):
    model = AdaBoostRegressor(**params)
    return model


def regression_params():
    params = AdaBoostRegressor().get_params()
    return params
