# Imports models
from .dvs.model_convtiny_gesture import (convtiny_dvs_gesture,
                                         convtiny_gesture_pretrained)
from .dvs.model_convtiny_handy import (convtiny_dvs_handy,
                                       convtiny_handy_pretrained)
from .cifar10.model_ds_cnn import ds_cnn_cifar10, ds_cnn_cifar10_pretrained
from .cifar10.model_vgg import vgg_cifar10, vgg_cifar10_pretrained
from .imagenet.model_mobilenet import (mobilenet_imagenet,
                                       mobilenet_imagenet_pretrained,
                                       mobilenet_cats_vs_dogs_pretrained)
from .imagenet.model_mobilenet_edge import (mobilenet_edge_imagenet,
                                            mobilenet_edge_imagenet_pretrained)
from .kws.model_ds_cnn import ds_cnn_kws, ds_cnn_kws_pretrained
from .kws.model_ds_cnn_edge import (ds_cnn_edge_kws, ds_cnn_edge_kws_pretrained)
from .utk_face.model_vgg import vgg_utk_face, vgg_utk_face_pretrained
from .cse2018.model_tse import tse_mlp_cse2018, tse_mlp_cse2018_pretrained
from .tabular_data import tabular_data
from .detection.model_yolo import yolo_base, yolo_widerface_pretrained
