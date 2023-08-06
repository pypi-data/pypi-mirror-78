from xgboost import XGBClassifier,XGBRegressor


def classifier(**params):
    model = XGBClassifier(**params)
    return model


def classifier_params():
    params = XGBClassifier().get_params()
    return params


def regression(**params):
    model = XGBRegressor(**params)
    return model


def regression_params():
    params = XGBRegressor().get_params()
    return params
