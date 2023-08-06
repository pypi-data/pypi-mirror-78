from sklearn.naive_bayes import MultinomialNB


def classifier(**params):
    model = MultinomialNB(**params)
    return model


def classifier_params():
    params = MultinomialNB().get_params()
    return params
