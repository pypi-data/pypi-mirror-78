from sklearn.linear_model import ARDRegression


def regression(**params):
    model = ARDRegression(**params)
    return model


def regression_params():
    params = ARDRegression().get_params()
    return params
