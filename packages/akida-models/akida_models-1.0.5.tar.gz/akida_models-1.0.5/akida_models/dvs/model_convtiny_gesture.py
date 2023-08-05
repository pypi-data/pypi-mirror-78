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

# System imports
import os
import warnings

# Tensorflow/Keras Imports
from tensorflow.keras.utils import get_file
from tensorflow.keras import backend, Model
from tensorflow.keras.layers import (Input, BatchNormalization, MaxPool2D,
                                     GlobalAvgPool2D, Reshape, Dropout,
                                     Activation)

# cnn2snn Imports
from cnn2snn import load_quantized_model
from cnn2snn.quantization_layers import dense

# Local utils
from ..quantization_blocks import (_add_activation_layer, _get_weight_quantizer,
                                   conv_block, separable_conv_block)

# Locally fixed config options
# The number of neurons in the penultimate dense layer
# This layer has binary output spikes, and could be a bottleneck
# if care isn't taken to ensure enough info capacity
NUM_SPIKING_NEURONS = 256

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/convtiny/'


def convtiny_dvs_gesture(input_shape,
                         weights=None,
                         classes=None,
                         weight_quantization=0,
                         activ_quantization=0):
    """Instantiates a CNN for the "IBM DVS Gesture" example.

    Args:
        input_shape (tuple): input shape tuple of the model
        weights (str): one of `None` (random initialization) or the path to the
             pretrained weights or the path to the weights file to be loaded.
        classes (int): number of classes to classify images into.
        weight_quantization (int): sets all weights in the model to have
            a particular quantization bitwidth except for the weights in the
            first layer.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization: sets all activations in the model to have a
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '1' through '8' implements n-bit weights where n is from 1-8 bits.

    Returns:
        tf.keras.Model: a quantized Keras convolutional model for DVS Gesture.
    """

    img_input = Input(input_shape)

    x = conv_block(img_input,
                   filters=16,
                   kernel_size=(3, 3),
                   name='conv_01',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='max',
                   pool_size=(3, 3),
                   weight_quantization=weight_quantization,
                   activ_quantization=activ_quantization,
                   strides=(1, 1))

    x = conv_block(x,
                   filters=32,
                   kernel_size=(3, 3),
                   name='conv_02',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='max',
                   pool_size=(3, 3),
                   weight_quantization=weight_quantization,
                   activ_quantization=activ_quantization,
                   strides=(1, 1))

    x = conv_block(x,
                   filters=64,
                   kernel_size=(3, 3),
                   name='conv_03',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='max',
                   pool_size=(2, 2),
                   weight_quantization=weight_quantization,
                   activ_quantization=activ_quantization,
                   strides=(1, 1))

    x = conv_block(x,
                   filters=128,
                   kernel_size=(3, 3),
                   name='conv_04',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='global_avg',
                   pool_size=(2, 2),
                   weight_quantization=weight_quantization,
                   activ_quantization=activ_quantization,
                   strides=(1, 1))

    bm_outshape = (1, 1, 128)

    x = Reshape(bm_outshape, name='reshape_1')(x)
    x = Dropout(1e-3, name='dropout')(x)

    aq = 0
    if weight_quantization > 0:
        # Assume that if we're quantizing weights, we want the Spiking Layer to
        # generate spikes
        aq = 1
        # Assume that if we're quantizing weights, we want the Dense layer to
        # be HW compatible, => WQ=2
        fc_weight_quantizer = _get_weight_quantizer(2)
    else:
        aq = activ_quantization
        fc_weight_quantizer = _get_weight_quantizer(weight_quantization)

    x = separable_conv_block(x,
                             filters=NUM_SPIKING_NEURONS,
                             kernel_size=(3, 3),
                             use_bias=False,
                             padding='same',
                             name='spiking_layer',
                             add_batchnorm=True,
                             weight_quantization=weight_quantization,
                             activ_quantization=aq,
                             pooling=None)

    x = dense(classes, modifier=fc_weight_quantizer, use_bias=False)(x)
    x = Activation('softmax', name='act_softmax')(x)
    x = Reshape((classes,), name='reshape_2')(x)

    model = Model(inputs=img_input, outputs=x, name='dvs_network')

    # Load weights
    if weights is not None:
        model.load_weights(weights, by_name=True)

    return model


def convtiny_gesture_pretrained():
    model_name = 'convtiny_dvs_gesture_wq2_aq4.h5'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          cache_subdir='models')
    return load_quantized_model(model_path)
