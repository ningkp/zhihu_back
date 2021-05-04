import os
from alcloud.config import TEST_RES_DIR
from alcloud.model_updating.deep import AlCloudPytorchImgClaModel

TEST_DATA_DIR = os.path.join(TEST_RES_DIR, 'images')
test_labels = {
    'n01774384_3.JPEG': 1,
    'n01774384_7.JPEG': 0,
    'n01774384_21.JPEG': 2,
    'n01774384_54.JPEG': 3,
    'n01774384_74.JPEG': 4,
}

for model in ['GoogleNet', 'DenseNet', 'AlexNet', 'ResNet', 'VGG', '']:
    model = AlCloudPytorchImgClaModel(project_id='123test', model_name=model, num_classes=5)
    model.fit(data_dir=TEST_DATA_DIR, label=test_labels, optimize_param={'lr': 0.01}, save_model=False)

    proba_result = model.predict_proba(data_dir=TEST_DATA_DIR)
    print(proba_result)
    print(proba_result.shape)
    print(model.predict(data_dir=TEST_DATA_DIR))


model = AlCloudPytorchImgClaModel(project_id='123test', model_name='GoogleNet', num_classes=5)
for optimize_method in ['Adadelta', 'Adagrad', 'Adam', 'SparseAdam', 'Adamax',
                       'ASGD', 'SGD', 'Rprop', 'RMSprop', 'LBFGS']:
    model.fit(data_dir=TEST_DATA_DIR, label=test_labels, optimize_method=optimize_method, save_model=False)

    proba_result = model.predict_proba(data_dir=TEST_DATA_DIR)
    print(proba_result)
    print(proba_result.shape)
    print(model.predict(data_dir=TEST_DATA_DIR))


for loss in ['L1Loss', 'NLLLoss', 'KLDivLoss', 'MSELoss', 'BCELoss',
           'BCEWithLogitsLoss', 'NLLLoss2d','CosineEmbeddingLoss', 'CTCLoss',
           'HingeEmbeddingLoss', 'MarginRankingLoss','MultiLabelMarginLoss',
           'MultiLabelSoftMarginLoss', 'MultiMarginLoss', 'SmoothL1Loss',
           'SoftMarginLoss', 'CrossEntropyLoss', 'TripletMarginLoss', 'PoissonNLLLoss']:
    model.fit(data_dir=TEST_DATA_DIR, label=test_labels, loss=loss, save_model=False)

    proba_result = model.predict_proba(data_dir=TEST_DATA_DIR)
    print(proba_result)
    print(proba_result.shape)
    print(model.predict(data_dir=TEST_DATA_DIR))

