METHODS = ['3D_ResNet']

from ..third_party.pytorch_3d_cnn.ext_fea import *

__all__ = [
    'init_3d_resnext_feature_extractor',
    'init_3d_resnext',
    'extract_video_feature_from_frames',
    'extract_video_feature',
    'extract_frames',
]
