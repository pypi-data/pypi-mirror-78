from sklearn.linear_model import LogisticRegressionCV


def classifier(**params):
    model = LogisticRegressionCV(**params)
    return model


def classifier_params():
    params = LogisticRegressionCV().get_params()
    return params
