from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


def classifier(**params):
    model = RandomForestClassifier(**params)
    return model


def classifier_params():
    params = RandomForestClassifier().get_params()
    return params


def regression(**params):
    model = RandomForestRegressor(**params)
    return model


def regression_params():
    params = RandomForestRegressor().get_params()
    return params
