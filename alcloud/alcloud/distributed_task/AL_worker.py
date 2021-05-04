"""
TODO:
1. update status after updating rank table
2. read data from local standby postgre server
3. write result to query queue & write logs
"""

import redis
from ..AL_query.alipy_rank.query_strategy import *
from ..utils.proj_info import ProjInfo
from ..utils.data_manipulate import load_feature_label
from .AL_algorithm import *
from ..utils.proj_info import ProjInfo, DataInfo
from ..config import redis_data_prediction_server_args, redis_proj_status_args

proj_status = redis.Redis(**redis_proj_status_args)

def rank_unlab_data(project_id, qs, qs_para, label_index,
                    unlabel_index, unlab_prob_prediction=None,
                    unlab_decval_prediction=None, **kwargs):
    '''The unified functions for invoking all qs.

    :param project_id: str
        Project id.

    :param qs: str
        Name of the query strategy.

    :param qs_para: dict
        Parameters of qs.

    :param label_index: list
        The indexes of labeled data.

    :param unlabel_index: list
        The indexes of unlabeled data.

    :param unlab_prob_prediction: 2D array, optional (default=None)
        The proba prediction for unlabeled data. Should have the same length with unlabel_index.
        Note that, must provide one of {'unlab_prob_prediction', 'unlab_decval_prediction'}.

    :param unlab_decval_prediction: 1D array, optional (default=None)
        The decision value for unlabeled data. Should have the same length with unlabel_index.
        Note that, must provide one of {'unlab_prob_prediction', 'unlab_decval_prediction'}.

    :return:
    '''
    # set status
    proj_status.set(str(project_id) + '_query', 1)
    proj_status.set(str(project_id) + '_busy', 1)

    # check params
    qs_parameters_dict = qs_parameters_requirement
    assert qs in qs_parameters_dict.keys(), "Query strategy {} is not defined".format(qs)
    # assert unlab_prob_prediction or unlab_decval_prediction, "must provide one of {'unlab_prob_prediction', 'unlab_decval_prediction'}."

    # prepare params
    pinfo = ProjInfo(project_id=project_id, type='al')
    requirements = qs_parameters_dict[qs]

    qs_kwargs = dict()
    qs_kwargs['label_index'] = label_index
    qs_kwargs['unlabel_index'] = unlabel_index
    if 'need_feature_mat' in requirements:
        if 'need_label' in requirements:
            X, y = load_feature_label(project_id=project_id, load_label=True, labeled_index=label_index)
            qs_kwargs['y'] = y
        else:
            X, _ = load_feature_label(project_id=project_id)
        qs_kwargs['X'] = X
    qs_kwargs['y_shape'] = pinfo.get_y_shape() if 'need_label_shape' in requirements else None
    qs_kwargs['X_shape'] = pinfo.get_X_shape() if 'need_feature_shape' in requirements else None
    qs_kwargs['label_tree'] = pinfo.get_label_tree() if 'need_hierarchy_tree' in requirements else None
    qs_kwargs['model'] = pinfo.get_model() if 'need_model' in requirements else None
    if 'need_prediction' in requirements:
        qs_kwargs['unlab_prob_prediction'] = unlab_prob_prediction if unlab_prob_prediction else unlab_decval_prediction
    else:
        qs_kwargs['unlab_prob_prediction'] = None
    qs_kwargs.update(pinfo.get_qs_param())

    # if cost sensitive
    if 'budget' in requirements:
        pinfo.fetch_hierarchy_info()
        qs_kwargs['budget'] = pinfo.get_budget()
        qs_kwargs['label_tree'] = pinfo.get_label_tree()
        qs_kwargs['hierarchy_costs'] = pinfo.get_hierarchy_costs()

    # invoke
    ranked_index = eval(qs + '(**qs_kwargs)')
    # update prediction when training finished.
    # unlab_prediction = dict(zip(ranked_index, unlab_prob_prediction if unlab_prob_prediction else unlab_decval_prediction))

    # update redis table

    # set status
    proj_status.set(str(project_id) + '_query', 0)
    proj_status.set(str(project_id) + '_busy', 0)


def sequential_rank_unlab_data():
    """return a subset of unlab data at each iteration (not rank all unlab data). 
    Should append them to the cache list instead of replacing.
    """
    pass


def incre_rank_unlab_data():
    """These methods will save/load some specified data for incremental querying. 
    (the latest query depends on the intermediate results of the previous iterations.)
    """
    pass
