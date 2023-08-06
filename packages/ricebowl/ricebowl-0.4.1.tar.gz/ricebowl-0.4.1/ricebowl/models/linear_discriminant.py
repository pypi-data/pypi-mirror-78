from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def classifier(**params):
    model = LinearDiscriminantAnalysis(**params)
    return model


def classifier_params():
    params = LinearDiscriminantAnalysis().get_params()
    return params

