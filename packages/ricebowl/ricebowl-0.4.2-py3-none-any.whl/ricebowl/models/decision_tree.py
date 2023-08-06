from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


def classifier(**params):
    model = DecisionTreeClassifier(**params)
    return model


def classifier_params():
    params = DecisionTreeClassifier().get_params()
    return params


def regression(**params):
    model = DecisionTreeRegressor(**params)
    return model


def regression_params():
    params = DecisionTreeRegressor().get_params()
    return params
