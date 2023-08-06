from sklearn.linear_model import LinearRegression


def regression(**params):
    model = LinearRegression(**params)
    return model


def regression_params():
    params = LinearRegression().get_params()
    return params
