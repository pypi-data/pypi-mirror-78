from sklearn.tree import ExtraTreeClassifier,ExtraTreeRegressor


def classifier(**params):
    model = ExtraTreeClassifier(**params)
    return model


def classifier_params():
    params = ExtraTreeClassifier().get_params()
    return params


def regression(**params):
    model = ExtraTreeRegressor(**params)
    return model


def regression_params():
    params = ExtraTreeRegressor().get_params()
    return params
