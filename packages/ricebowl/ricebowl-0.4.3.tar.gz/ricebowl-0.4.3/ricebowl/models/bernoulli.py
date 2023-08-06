from sklearn.naive_bayes import BernoulliNB


def classifier(**params):
    model = BernoulliNB(**params)
    return model


def classifier_params():
    params = BernoulliNB().get_params()
    return params
