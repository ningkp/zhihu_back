#################DIR#########
import os

file_dir = os.path.dirname(__file__)
TEST_RES_DIR = os.path.join(os.path.dirname(file_dir), './../Public/Img Sel Data/')
PRETRAINED_DEEP_MODEL_DIR = os.path.join(TEST_RES_DIR, 'pre_trained_models')
TRAINED_DEEP_MODEL_DIR = os.path.join(TEST_RES_DIR, 'trained_models')


RAW_DATA_DIR = None
DATA_FEATURE_DIR = None
FEATURE_DICT = None     # row - file name
LABEL_DICT = None       # class name - int

INCRE_MODEL_SAVE_DIR = None
INCRE_AL_DATA_DIR = None

DEEP_MODEL_TRAIN_URL = None
TRAD_MODEL_TRAIN_URL = None
AL_URL = None

##############################

#待请求的容器
# AL query
# projectID : list of indexes
redis_query_queue_server_args = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

#上传的容器
# labelArrivalProject : List or Set of project ids
# projectID : list of json str
redis_latest_label_cache_server_args = {
    'host': 'localhost',
    'port': 6379,
    'db': 1
}

# projectID_dataIndex : labelJsonStr
redis_data_prediction_server_args = {
    'host': 'localhost',
    'port': 6379,
    'db': 2
}

# whether the model is training, the AL algorithm is running
# projectID_query : bool
# projectID_train : bool
# projectID_busy : bool
redis_proj_status_args = {
    'host':'localhost',
    'port':6379,
    'db':3
}

status_keys = {
    'is_calculating_AL': 'query',
    'is_training_model': 'train',
    'is_busy': 'busy',
}

SQL_proj_data_status_args = {
    'host': 'localhost',
    'port': 6379,
    'db': 4
}

SQL_proj_settings_args = {
    'host': 'localhost',
    'port': 6379,
    'db': 4
}



