from lightgbm import LGBMClassifier,LGBMRegressor

def classifier(**params):
    model = LGBMClassifier(**params)
    return model


def classifier_params():
    params = LGBMClassifier().get_params()
    return params


def regression(**params):
    model = LGBMRegressor(**params)
    return model


def regression_params():
    params = LGBMRegressor().get_params()
    return params
