from sklearn.linear_model import RANSACRegressor


def regression(**params):
    model = RANSACRegressor(**params)
    return model


def regression_params():
    params = RANSACRegressor().get_params()
    return params
