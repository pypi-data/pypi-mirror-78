from sklearn.linear_model import RidgeClassifier


def classifier(**params):
    model = RidgeClassifier(**params)
    return model


def classifier_params():
    params = RidgeClassifier().get_params()
    return params
