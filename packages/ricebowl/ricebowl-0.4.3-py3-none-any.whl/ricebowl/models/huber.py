from sklearn.linear_model import HuberRegressor


def regression(**params):
    model = HuberRegressor(**params)
    return model


def regression_params():
    params = HuberRegressor().get_params()
    return params
