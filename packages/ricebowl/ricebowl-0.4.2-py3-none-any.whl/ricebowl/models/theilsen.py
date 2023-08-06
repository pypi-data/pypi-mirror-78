from sklearn.linear_model import TheilSenRegressor


def regression(**params):
    model = TheilSenRegressor(**params)
    return model


def regression_params():
    params = TheilSenRegressor().get_params()
    return params
