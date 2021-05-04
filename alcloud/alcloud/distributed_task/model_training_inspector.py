"""
model update request format:
project_id: str,
qs: str (receive from browser)
model: str (receive from browser)
label_type:str (receive from browser)
cahche_label: json
"""

import redis
import requests
import pickle
import time
from ..config import redis_latest_label_cache_server_args, \
    redis_proj_status_args, status_keys, DEEP_MODEL_TRAIN_URL, TRAD_MODEL_TRAIN_URL

label_cache = redis.Redis(**redis_latest_label_cache_server_args)
proj_status = redis.Redis(**redis_proj_status_args)

non_empty_label_cache_project =  dict()

while 1:
    # check if new labeled data arrives
    if not non_empty_label_cache_project.keys():
        proj_info = label_cache.brpop('labelArrivalProject')
        # dispatch binary object and take the id as the key, the others as the value

        non_empty_label_cache_project[proj_id] = qs
    else:
        proj_info = label_cache.rpop('labelArrivalProject')
        if proj_info:
            # dispatch binary object and take the id as the key, the others as the value

            non_empty_label_cache_project[proj_id] = qs
    
    # check if training
    for k in list(non_empty_label_cache_project.keys()):
        if proj_status.get(k+'_'+status_keys['is_busy']) != '1':
            # update status, send request, clear cache
            # train_md_mq.lpush(MQ_keys['redis_model_training_requests'], k)
            cached_label = label_cache.get(k)
            label_cache.delete(k)

            # call training function
            try:
                requests.post(DEEP_MODEL_TRAIN_URL, timeout=0.0000000001)
            except requests.exceptions.ReadTimeout:
                pass

            non_empty_label_cache_project.pop(k)

    time.sleep(2)
