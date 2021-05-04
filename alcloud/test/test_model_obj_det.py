# from alcloud.model_updating.deep_obj_det import _init_yolov3, _init_faster_rcnn
# print(_init_yolov3())
# print(_init_faster_rcnn())

import os
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from alcloud.config import TEST_RES_DIR
from alcloud.model_updating.deep_obj_det import AlCloudPytorchObjDetModel


data_dir = os.path.join(TEST_RES_DIR, 'object_detection', 'val2014_train')
with open(os.path.join(TEST_RES_DIR, 'object_detection', 'label_dict.pkl'), 'rb') as f:
    label_dict = pickle.load(f)

def construct_label_dict():
    # construct label dict for labeled set
    lab_dir = os.path.join(TEST_RES_DIR, 'object_detection', 'val2014_labels')
    files = os.listdir(lab_dir)
    file_base = [os.path.splitext(file)[0] for file in files]
    # split train/test
    train, test = train_test_split(file_base)
    # construct label dict
    train_label_dict = dict()
    for train_img in train:
        with open(os.path.join(lab_dir, train_img+'.txt'), 'r') as f:
            bboxes = np.loadtxt(f)
            if bboxes.ndim == 1:
                bboxes = bboxes.reshape((1, -1))
            train_label_dict[train_img+'.jpg'] = bboxes
    test_label_dict = dict()
    for test_img in test:
        with open(os.path.join(lab_dir, test_img+'.txt'), 'r') as f:
            bboxes = np.loadtxt(f)
            if bboxes.ndim == 1:
                bboxes = bboxes.reshape((1, -1))
            test_label_dict[test_img+'.jpg'] = bboxes

    print(train_label_dict)

    with open(os.path.join(TEST_RES_DIR, 'object_detection', 'train_label_dict.pkl'), 'wb') as f:
        pickle.dump(train_label_dict, f)
    with open(os.path.join(TEST_RES_DIR, 'object_detection', 'test_label_dict.pkl'), 'wb') as f:
        pickle.dump(test_label_dict, f)

def test_yolov3():
    # for model_name in ['Faster_RCNN', 'Yolov3']:
    model_name = 'Yolov3'
    obj_det_model = AlCloudPytorchObjDetModel('1234', model_name, num_classes=91)
    obj_det_model.fit(data_dir=data_dir, label=label_dict, batch_size=4, model_type=model_name)
    print("Training finish.")
    # eval
    print(obj_det_model.predict(data_dir=data_dir, data_names=list(label_dict.keys()), model_type=model_name))
    print(obj_det_model.predict_proba(data_dir=data_dir, data_names=list(label_dict.keys()), model_type=model_name))

def test_faser_rcnn():
    """"""
    # for model_name in ['Faster_RCNN', 'Yolov3']:
    model_name = 'Faster_RCNN'
    obj_det_model = AlCloudPytorchObjDetModel('1234', model_name, num_classes=91)
    obj_det_model.fit(data_dir=data_dir, label=label_dict, batch_size=2, model_type=model_name, optimize_param={'lr': 0.00001})
    print("Training finish.")
    # eval
    print(obj_det_model.predict(data_dir=data_dir, data_names=list(label_dict.keys()), model_type=model_name))
    print(obj_det_model.predict_proba(data_dir=data_dir, data_names=list(label_dict.keys()), model_type=model_name))


test_faser_rcnn()
