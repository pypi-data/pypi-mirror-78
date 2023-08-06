from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor


def classifier(**params):
    model = KNeighborsClassifier(**params)
    return model


def classifier_params():
    params = KNeighborsClassifier().get_params()
    return params


def regression(**params):
    model = KNeighborsRegressor(**params)
    return model


def regression_params():
    params = KNeighborsRegressor().get_params()
    return params
