from sklearn import svm


def classifier(**params):
    model = svm.SVC(**params)
    return model


def classifier_params():
    params = svm.SVC().get_params()
    return params


def regression(**params):
    model = svm.SVR(**params)
    return model


def regression_params():
    params = svm.SVR().get_params()
    return params
