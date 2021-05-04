# All available requirements are:
# need_feature_mat: feature matrix
# need_label: label matrix of labeled set
# need_prediction: probability prediction result of unlabeled data
# need_label_shape: shape of label matrix of whole dataset
# need_feature_shape: shape of feature matrix of whole dataset
# need_hierarchy_tree: label hierarchy tree
# need_model: base model (str)

# X, y, label_index, unlabel_index, unlab_prob_prediction, model, y_shape

qs_parameters_requirement = {
    # query instance
    'QueryInstanceUncertainty': ('need_prediction', ),  # class or proba output
    'QueryInstanceRandom': tuple(),
    'QueryInstanceQBC': ('need_qbc_prediction',),   # a list of class or proba output
    'QueryExpectedErrorReduction': ('need_feature_mat', 'need_label', 'need_model'),    # sklearn model with proba output
    'QueryInstanceQUIRE': ('need_feature_mat', 'need_label'),
    'QueryInstanceBMDR': ('need_feature_mat', 'need_label'),
    'QueryInstanceSPAL': ('need_feature_mat', 'need_label'),
    # query type
    'QueryTypeAURO': ('need_label', 'need_prediction', 'need_label_shape'), # prediction of label ranking model
    # multi label
    'QueryMultiLabelQUIRE': ('need_feature_mat', 'need_label'),
    'QueryMultiLabelAUDI': ('need_prediction', 'need_label'),   # prediction of label ranking model
    'QueryMultiLabelMMC': ('need_feature_mat', 'need_label', 'need_model'), # sklearn model with proba output
    'QueryMultiLabelAdaptive': ('need_feature_mat', 'need_label', 'need_model'),    # sklearn model with proba output
    'QueryMultiLabelRandom': tuple(),
    # cost sensitive
    'QueryCostSensitiveHALC': ('need_feature_mat', 'need_label', 'need_model', 'budget', 'label_tree', 'hierarchy_costs'),
    'QueryCostSensitiveRandom': ('budget', 'hierarchy_costs'),
    'QueryCostSensitivePerformance': ('need_feature_mat', 'need_label', 'need_model', 'budget', 'hierarchy_costs'),
    # query features
    # can not be deployed to a distributed system (need to record the results of history matrix completion)
    # and must be computed iteratively
}

# need_qbc_prediction: multiple prediction matrix provided from different models
qs_default_model_parameters_requirement={
    # query instance
    'QueryInstanceUncertainty': ('need_prediction',),
    'QueryInstanceRandom': tuple(),
    'QueryInstanceQBC': ('need_feature_mat', 'need_label'),
    'QueryExpectedErrorReduction': ('need_feature_mat', 'need_label'),
    'QueryInstanceQUIRE': ('need_feature_mat', 'need_label'),
    'QueryInstanceBMDR': ('need_feature_mat', 'need_label'),
    'QueryInstanceSPAL': ('need_feature_mat', 'need_label'),
    # query type
    'QueryTypeAURO': ('need_label', 'need_prediction', 'need_label_shape'), # prediction of label ranking model
    # multi label
    'QueryMultiLabelQUIRE': ('need_feature_mat', 'need_label'),
    'QueryMultiLabelAUDI': ('need_prediction', 'need_label'),   # prediction of label ranking model
    'QueryMultiLabelMMC': ('need_feature_mat', 'need_label'),
    'QueryMultiLabelAdaptive': ('need_feature_mat', 'need_label'),
    'QueryMultiLabelRandom': tuple(),
    # cost sensitive
    'QueryCostSensitiveHALC': ('need_feature_mat', 'need_label', 'budget', 'label_tree', 'hierarchy_costs'),
    'QueryCostSensitiveRandom': ('budget', 'hierarchy_costs'),
    'QueryCostSensitivePerformance': ('need_feature_mat', 'need_label', 'budget', 'hierarchy_costs'),
    # query features
}

qs_params={
    'QueryInstanceUncertainty': ('measure',),
    'QueryInstanceQBC': ('disagreement',),
    'QueryInstanceQUIRE': ('kernel'),
    'QueryInstanceBMDR': ('kernel', 'beta', 'gamma', 'rho'),
    'QueryInstanceSPAL': ('kernel', 'mu', 'gamma', 'rho', 'lambda_init', 'lambda_pace'),
    'QueryMultiLabelRandom': ('select_type'),
}
