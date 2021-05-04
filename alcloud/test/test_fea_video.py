from alcloud.third_party.pytorch_3d_cnn.ext_fea import *
from alcloud.config import TEST_RES_DIR
import os

model, opt = init_3d_resnext_feature_extractor()
print(model, opt)
print(extract_video_feature_from_frames(os.path.join(TEST_RES_DIR, 'video', 'video_frames'), model, opt))
