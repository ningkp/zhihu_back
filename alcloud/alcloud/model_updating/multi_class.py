# linear_model = ['logistic regression', 'svm']
# non_linear_model = ['knn', 'decision trees']
# ensemble = ['rf', 'adaboost', 'xgboost']

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBClassifier
