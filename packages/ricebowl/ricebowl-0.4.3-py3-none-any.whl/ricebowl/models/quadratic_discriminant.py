from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


def classifier(**params):
    model = QuadraticDiscriminantAnalysis(**params)
    return model


def classifier_params():
    params = QuadraticDiscriminantAnalysis().get_params()
    return params

