import numpy as np
from sklearn.datasets import make_classification, make_multilabel_classification
from sklearn.svm import SVC
from alcloud.AL_query.alipy_rank import ToolBox
from alcloud.AL_query.alipy_rank.query_strategy import *

X, y = make_multilabel_classification(n_samples=2000, n_features=20, n_classes=5,
                                   n_labels=3, length=50, allow_unlabeled=True,
                                   sparse=False, return_indicator='dense',
                                   return_distributions=False,
                                   random_state=None)

y[y == 0] = -1  # -1 irrelevant, 0 unknown

# the cost of each class
cost = [1, 3, 3, 7, 10]

# if node_i is the parent of node_j , then label_tree(i,j)=1 else 0
label_tree = np.zeros((5,5),dtype=np.int)
label_tree[0, 1] = 1
label_tree[0, 2] = 1
label_tree[1, 3] = 1
label_tree[2, 4] = 1

alibox = ToolBox(X=X, y=y, query_type='PartLabels', saving_path='.')

# Split data
alibox.split_AL(test_ratio=0.3, initial_label_rate=0.1, split_count=10)

train_idx, test_idx, label_ind, unlab_ind = alibox.get_split(0)

model = SVC()

# The budget of query
budget = 40

select_ind = QueryCostSensitiveHALC.rank_unlabeled_data(X, y, label_index=label_ind, unlabel_index=unlab_ind, budget=budget, label_tree=label_tree, hierarchy_costs=cost, model=model)
# select_ind = hierarchical_multilabel_mark(select_ind, label_ind, label_tree, y)
print(select_ind)
select_ind = QueryCostSensitiveRandom.rank_unlabeled_data(X=X, y=y, label_index=label_ind, unlabel_index=unlab_ind, budget=budget, label_tree=label_tree, hierarchy_costs=cost, model=model)
# select_ind = hierarchical_multilabel_mark(select_ind, label_ind, label_tree, y)
print(select_ind)
select_ind = QueryCostSensitivePerformance.rank_unlabeled_data(X=X, y=y, label_index=label_ind, unlabel_index=unlab_ind, budget=budget, label_tree=label_tree, hierarchy_costs=cost, model=model)
# select_ind = hierarchical_multilabel_mark(select_ind, label_ind, label_tree, y)
print(select_ind)


