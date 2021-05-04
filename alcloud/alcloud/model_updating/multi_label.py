# model = ['decision trees', 'knn', 'rf', 'mlp', 'label ranking']

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from ..AL_query.alipy_rank.query_strategy.multi_label import LabelRankingModel
