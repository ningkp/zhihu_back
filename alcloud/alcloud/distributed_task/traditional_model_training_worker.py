"""
TODO:
1. read features and labels from local server (receive latest cached labels)
*. read existed model if incremental training
2. train model
*. write result to db if incremental training
3. predict & test if needed
4. gathering params and invoke AL function

5. Logging
"""

import redis
from ..model_updating.multi_class import *
from ..model_updating.multi_label import *
from ..model_updating.regression import *
from ..utils.data_manipulate import create_img_dataloader, load_feature_label
from ..utils.proj_info import ProjInfo, DataInfo
from ..config import redis_data_prediction_server_args, redis_proj_status_args

__all__ = ['re_train_model',
           ]

proj_status = redis.Redis(**redis_proj_status_args)

def re_train_model(project_id, qs, model, label_type, cached_label, **kwargs):
    '''
    project_id: str,
    qs: str(receive from browser)
    model: str(receive from browser)
    label_type: str(receive from browser)
    cahche_label: json
    '''
    # set status
    proj_status.set(str(project_id) + '_train', 1)
    proj_status.set(str(project_id) + '_busy', 1)

    # fetch project info from db here
    pinfo = ProjInfo(project_id=project_id, type='model')
    dinfo = DataInfo(project_id=project_id)

    # init model
    base_clf = eval(model + '(**pinfo.get_model_param()')

    # fetch indexes here
    label_index = dinfo.get_labeled_indexes()
    unlabel_index = dinfo.get_unlabeled_indexes()

    # load data matrix here
    X, y = load_feature_label(project_id=project_id, load_label=True, labeled_index=label_index)

    # train/test model
    base_clf.fit(X[label_index], y)
    if hasattr(base_clf, 'predict_proba'):
        prediction = base_clf.predict_proba(X[unlabel_index])
    else:
        prediction = base_clf.predict(X[unlabel_index])

    # invoke AL query strategy
    pass

    proj_status.set(str(project_id) + '_train', 0)

