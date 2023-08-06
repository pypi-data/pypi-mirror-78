from sklearn.linear_model import LogisticRegression


def classifier(**params):
    model = LogisticRegression(**params)
    return model


def classifier_params():
    params = LogisticRegression().get_params()
    return params
