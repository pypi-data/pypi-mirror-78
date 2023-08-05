#!/usr/bin/env python
# ******************************************************************************
# Copyright 2019 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

import os
import pickle

import numpy as np

from tensorflow.keras import Model
from tensorflow.keras.layers import Reshape
from tensorflow.keras.utils import get_file

from ..quantization_blocks import separable_conv_block
from ..imagenet.model_mobilenet import mobilenet_imagenet

# CNN2SNN imports
from cnn2snn import load_quantized_model


def yolo_base(input_shape,
              classes,
              nb_box=5,
              grid_size=(7, 7),
              alpha=1.0,
              dropout=1e-3,
              weights=None,
              weight_quantization=0,
              activ_quantization=0,
              input_weight_quantization=None):
    """" Instantiates the YOLOv2 architecture.

    Args:
        input_shape (tuple): input shape tuple
        classes (int): number of classes to classify images into
        nb_box (int): number of anchors boxes to use
        grid_size (tuple): YOLO grid size tuple
        alpha (float): controls the width of the model
        dropout (float): dropout rate
        weights (str): `None` (random initialization) or the path to the weights
         file to be loaded.
        weight_quantization (int): sets all weights in the model to have
            a particular quantization bitwidth except for the weights in the
            first layer.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization: sets all activations in the model to have a
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        input_weight_quantization: sets weight quantization in the first layer.
            Defaults to weight_quantization value.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.

    Returns:
        tf.keras.Model: a Keras Model instance.

    """
    # Overrides input weight quantization if None
    if input_weight_quantization is None:
        input_weight_quantization = weight_quantization

    # Create a MobileNet network without top layers
    base_model = mobilenet_imagenet(
        input_shape=input_shape,
        alpha=alpha,
        dropout=dropout,
        include_top=False,
        weights=None,
        weight_quantization=weight_quantization,
        activ_quantization=activ_quantization,
        input_weight_quantization=input_weight_quantization)

    # Add YOLO top layers to the base model
    input_shape = base_model.input_shape
    x = base_model.layers[-1].output
    x = separable_conv_block(x,
                             filters=1024,
                             name='1conv',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             activ_quantization=activ_quantization,
                             weight_quantization=weight_quantization,
                             add_batchnorm=True)
    x = separable_conv_block(x,
                             filters=1024,
                             name='2conv',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             activ_quantization=activ_quantization,
                             weight_quantization=weight_quantization,
                             add_batchnorm=True)
    x = separable_conv_block(x,
                             filters=1024,
                             name='3conv',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             activ_quantization=activ_quantization,
                             weight_quantization=weight_quantization,
                             add_batchnorm=True)
    x = separable_conv_block(x,
                             filters=(nb_box * (4 + 1 + classes)),
                             name='detection_layer',
                             kernel_size=(1, 1),
                             padding='same',
                             use_bias=True,
                             activ_quantization=None,
                             weight_quantization=weight_quantization,
                             add_batchnorm=False)

    model = Model(inputs=base_model.input, outputs=x, name='yolo_base')

    # Initialize detection layer weights
    layer = model.get_layer("detection_layer")
    detection_weights = layer.get_weights()

    mu, sigma = 0, 0.1
    grid_area = grid_size[0] * grid_size[1]

    dw_kernel = np.random.normal(mu, sigma,
                                 size=detection_weights[0].shape) / grid_area
    pw_kernel = np.random.normal(mu, sigma,
                                 size=detection_weights[1].shape) / grid_area
    bias = np.random.normal(mu, sigma,
                            size=detection_weights[2].shape) / grid_area

    layer.set_weights([dw_kernel, pw_kernel, bias])

    # Load weights
    if weights is not None:
        model.load_weights(weights, by_name=True)

    return model


def yolo_widerface_pretrained():
    """
    Helper method to retrieve a `yolo_base` model that was trained on WiderFace
    dataset and the anchors that are needed to interpet the model output.

    Returns:
        tf.keras.Model, list: a Keras Model instance and a list of anchors.

    """
    anchors_name = 'widerface_anchors.pkl'
    anchors_path = get_file(
        fname=anchors_name,
        origin='http://data.brainchip.com/dataset-mirror/widerface/' +
        anchors_name,
        cache_subdir='datasets/widerface')
    with open(anchors_path, 'rb') as handle:
        anchors = pickle.load(handle)

    model_name = 'yolo_widerface_wq4_aq4.h5'
    model_path = get_file(fname=model_name,
                          origin='http://data.brainchip.com/models/yolo/' +
                          model_name,
                          cache_subdir='models')

    return load_quantized_model(model_path), anchors


def yolo_voc_pretrained():
    """
    Helper method to retrieve a `yolo_base` model that was trained on PASCAL
    VOC2012 dataset for 'person' and 'car' classes only, and the anchors that
    are needed to interpet the model output.

    Returns:
        tf.keras.Model, list: a Keras Model instance and a list of anchors.

    """
    anchors_name = 'voc_anchors.pkl'
    anchors_path = get_file(
        fname=anchors_name,
        origin='http://data.brainchip.com/dataset-mirror/voc/' + anchors_name,
        cache_subdir='datasets/voc')
    with open(anchors_path, 'rb') as handle:
        anchors = pickle.load(handle)

    model_name = 'yolo_voc_wq4_aq4.h5'
    model_path = get_file(fname=model_name,
                          origin='http://data.brainchip.com/models/yolo/' +
                          model_name,
                          cache_subdir='models')

    return load_quantized_model(model_path), anchors
