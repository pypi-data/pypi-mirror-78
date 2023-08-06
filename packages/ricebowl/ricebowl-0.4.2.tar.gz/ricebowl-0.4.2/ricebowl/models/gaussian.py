from sklearn.naive_bayes import GaussianNB


def classifier(**params):
    model = GaussianNB(**params)
    return model


def classifier_params():
    params = GaussianNB().get_params()
    return params
