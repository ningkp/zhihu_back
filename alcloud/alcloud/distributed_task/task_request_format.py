"""
Model training info (query from db):
model: str,
query_strategy: str,
query_type: str,
label_type: str,
label_index: list,
unlabel_index: list,
qs_need_model: bool
qs_need_feature_mat: bool,
qs_need_label: bool,
qs_need_prediction: bool,
qs_need_hierarchy_tree (hierarchy): bool
qs_need_label_shape (multi_label) :bool
qs_need_feature_shape (feature query) :bool
need_test: bool,
test_index: list,
performance_metric: str
feature_matrix: list (local)
label_matrix: list (local)
cached_labels: list (local)
---------------------------
next version:
qs_need_oracle_info (noisy oracle): bool

training result format:
model, proj_id, worker_id, work_id,
label_type, need_prediction, need_test,
performance_metric, start_time, end_time

AL calc request format:
project_id: str,
qs: str,
query_type: str,
label: dict,
label_type: str,
label_index: list,
unlabel_index: list,
unlab_prob_prediction: list,
unlab_decval_prediction: list,


AL result format:
project_id: str,
qs: str,
query_type: str,
params: dict,
start_time: time,
end_time: time,
work_id: str,
worker_id: str,
status: str,    (Success, Fail)
remark: str,  (Failure info)
query_rank: list,
"""
