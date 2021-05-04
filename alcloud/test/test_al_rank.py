import copy
import warnings
from sklearn.datasets import make_classification
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from alcloud.AL_query.alipy_rank import ToolBox
from alcloud.AL_query.alipy_rank.query_strategy.multi_label import LabelRankingModel, get_Xy_in_multilabel
from alcloud.AL_query.alipy_rank.query_strategy import *
from alcloud.model_updating.deep import AlCloudPytorchImgClaModel

def test_rank(model):
    X, y = make_classification(n_samples=500, n_features=20, n_informative=2, n_redundant=2,
                               n_repeated=0, n_classes=2, n_clusters_per_class=2, weights=None, flip_y=0.2,
                               class_sep=1.0,
                               hypercube=True, shift=0.0, scale=1.0, shuffle=True, random_state=None)

    alibox = ToolBox(X=X, y=y, query_type='AllLabels', saving_path='.')

    # Split data
    alibox.split_AL(test_ratio=0.3, initial_label_rate=0.1, split_count=10)

    train_idx, test_idx, label_ind, unlab_ind = alibox.get_split(0)

    model.fit(X=X[label_ind], y=y[label_ind])

    prob_prediction = model.predict_proba(X[unlab_ind])
    bagging = BaggingClassifier(model)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        bagging.fit(X[label_ind], y[label_ind])
    est_arr = bagging.estimators_
    qbc_prediction = [estimator.predict_proba(X[unlab_ind]) for estimator in est_arr]

    # instance
    print('unc',QueryInstanceUncertainty.rank_unlabeled_data(unlabel_index=unlab_ind, unlab_prob_prediction=prob_prediction))
    print('rand',QueryInstanceRandom.rank_unlabeled_data(unlabel_index=unlab_ind))
    print('qbc',QueryInstanceQBC.rank_unlabeled_data(unlabel_index=unlab_ind, unlab_prob_prediction=qbc_prediction, disagreement='KL_divergence'))
    print('eer',QueryExpectedErrorReduction.rank_unlabeled_data(X=X, y=y, label_index=label_ind, unlabel_index=unlab_ind, model=model))
    print('quire',QueryInstanceQUIRE.rank_unlabeled_data(X=X, y=y, label_index=label_ind, unlabel_index=unlab_ind))
    print('bmdr',QueryInstanceBMDR.rank_unlabeled_data(X=X, y=y, label_index=label_ind, unlabel_index=unlab_ind))
    print('spal',QueryInstanceSPAL.rank_unlabeled_data(X=X, y=y, label_index=label_ind, unlabel_index=unlab_ind))

    # multi label
    import numpy as np
    import copy
    from sklearn.preprocessing import OneHotEncoder, normalize

    X = normalize(X, norm='l2')
    mlb = OneHotEncoder()
    mult_y = mlb.fit_transform(y.reshape((-1, 1)))
    mult_y = np.asarray(mult_y.todense())
    mult_y_for_metric = mult_y.copy()

    # Or generate a dataset with any sizes
    # X, mult_y = make_multilabel_classification(n_samples=5000, n_features=20, n_classes=5, length=5)

    # Since we are using the label ranking model, the label 0 means unknown. we need to
    # set the 0 entries to -1 which means irrelevant.
    mult_y[mult_y == 0] = -1
    alibox = ToolBox(X=X, y=mult_y, query_type='PartLabels')
    alibox.split_AL(test_ratio=0.2, initial_label_rate=0.05, all_class=False)
    train_idx, test_idx, label_ind, unlab_ind = alibox.get_split(0)
    model_lr_ml = LabelRankingModel() # base model
    X_tr, y_tr, _ = get_Xy_in_multilabel(label_ind, X=X, y=mult_y, unknown_element=0)
    model_lr_ml.fit(X=X_tr, y=y_tr)
    X_unlab, _, _ = get_Xy_in_multilabel(unlab_ind, X=X, y=mult_y, unknown_element=0)
    pres,pred = model_lr_ml.predict(X_unlab)

    print('quire',QueryMultiLabelQUIRE.rank_unlabeled_data(X=X,y=mult_y, label_index=label_ind, unlabel_index=unlab_ind))
    print('audi', QueryMultiLabelAUDI.rank_unlabeled_data(y=mult_y, label_index=label_ind, unlabel_index=copy.deepcopy(unlab_ind), unlab_prob_prediction=pres))
    print('MMC',QueryMultiLabelMMC.rank_unlabeled_data(X=X,y=mult_y, label_index=label_ind, unlabel_index=unlab_ind, model=model))
    print('Adaptive',QueryMultiLabelAdaptive.rank_unlabeled_data(X=X,y=mult_y, label_index=label_ind, unlabel_index=unlab_ind, model=model))
    print('random',QueryMultiLabelRandom.rank_unlabeled_data(unlabel_index=unlab_ind, select_type='ins'))
    print('random2',QueryMultiLabelRandom.rank_unlabeled_data(unlabel_index=unlab_ind, select_type='ins-lab'))

    # query type
    print('auro', QueryTypeAURO.rank_unlabeled_data(label_index=label_ind, unlabel_index=copy.deepcopy(unlab_ind), unlab_prob_prediction=pres, y_shape=mult_y.shape))

    # feature

model = DecisionTreeClassifier()
test_rank(model)
# model = AlCloudPytorchImgClaModel(project_id='123test', model_name='GoogleNet', num_classes=2)
# test_rank(model)
