import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, normalize

from alcloud.model_updating.hierarchy import OVRModel

# from model_updating.multi_class import LogisticRegression, SVC, KNeighborsClassifier, \
#     DecisionTreeClassifier, RandomForestClassifier, AdaBoostClassifier, XGBClassifier
# from model_updating.multi_label import DecisionTreeClassifier, KNeighborsClassifier, RandomForestClassifier,\
#     MLPClassifier, LabelRankingModel
# from model_updating.regression import SVR, LogisticRegression, RandomForestRegressor, MLPRegressor

X, y = load_iris(return_X_y=True)
X = normalize(X, norm='l2')
mlb = OneHotEncoder()
mult_y = mlb.fit_transform(y.reshape((-1, 1)))
mult_y = np.asarray(mult_y.todense())
mult_y_for_metric = mult_y.copy()


def test_ovr():
    lr = LogisticRegression()
    ovr_model = OVRModel(lr)
    ovr_model.fit(X, mult_y)
    res = ovr_model.predict(X)
    print(res)

    # svc
    ovr_model = OVRModel()
    ovr_model.fit(X, mult_y)
    res = ovr_model.predict(X)
    print(res)


test_ovr()
