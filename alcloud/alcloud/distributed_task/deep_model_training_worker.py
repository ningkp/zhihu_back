"""
TODO:
1. read features and labels from local server (receive latest cached labels)
*. read existed model if incremental training
2. train model
*. write result to disk if incremental training
3. predict & test if needed
4. gathering params and invoke AL function

5. Logging
"""

import redis
import os
import pickle
from ..config import TRAINED_DEEP_MODEL_DIR
from ..model_updating.deep import *
from ..AL_query.alipy_rank.query_strategy.multi_label import LabelRankingModel
from ..utils.data_manipulate import create_img_dataloader
from ..utils.proj_info import ProjInfo, DataInfo
from ..config import redis_data_prediction_server_args, redis_proj_status_args, redis_latest_label_cache_server_args

__all__ = ['icre_train_model',
           ]

proj_status = redis.Redis(**redis_proj_status_args)

def icre_train_model(project_id, qs, model, label_type, cached_label, **kwargs):
    '''
    project_id: str,
    qs: str(receive from browser), name of the AL query strategy
    model: str(receive from browser)
    label_type: str(receive from browser)
    cahche_label: json
    '''
    # set status
    proj_status.set(str(project_id) + '_train', 1)
    proj_status.set(str(project_id) + '_busy', 1)

    # fetch project info from db here
    pinfo = ProjInfo(project_id=project_id, type='model')

    # load existed model here
    if model == 'LabelRanking':
        if os.path.exists(os.path.join(TRAINED_DEEP_MODEL_DIR, project_id + '_model.pkl')):
            with open(os.path.join(TRAINED_DEEP_MODEL_DIR, project_id + '_model.pkl'), 'rb') as f:
                base_clf = pickle.load(f)

        # load training data here
        # Use cached label and request training data

        # train/test/save

    else:
        base_clf = AlCloudPytorchImgClaModel(project_id=project_id)

        # load training data here

        # train/test/save

    # invoke qs (project_id, qs, label_index, unlabel_index, unlab_prob_prediction, unlab_decval_prediction)

    proj_status.set(str(project_id) + '_train', 0)
