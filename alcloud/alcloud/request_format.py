"""
request data for labeling:
project_id: str,
labeler_id: str,
labeler_name: str,
access_key: str,
time_stamp: time,
query_type: str,
data_type: str,
label_type: str,
query_strategy: str,

handling:
return:
=======
data
prediction_value

TODO:
1. set data status
2. log

submit label:
project_id: str,
labeler_id: str,
labeler_name: str,
access_key: str,
time_stamp: time,
time_duration: str,
query_type: str,
data_type: str,
label_type: str,
query_strategy: str,
instance_index: str,
label: json,
prediction_value: json

receive label:
1. save label
2. save labeling info (labeler, time, ...)
3. set data status
"""