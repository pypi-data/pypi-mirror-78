from tpot import TPOTClassifier
from sklearn.datasets import load_iris
from processing import splitting
# Overview
# This library is providing us with the best model and optimized parameters along with the accuracy score.

def t_pot(ver,time):
    tpot= TPOTClassifier(verbosity=ver,max_time_mins=time)
    tpot.fit(x_train,y_train)
    print(tpot.score(x_test,y_test))

if __name__ == '__main__':
    data = load_iris().data
    label = load_iris().target
    x_train, x_test, y_train, y_test = splitting.split_data(data, label)
    t_pot(2,2)





                                                                                                                                                                                                                                                                                                                                                                                                                                                                    



