#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
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

from tensorflow.keras.layers import Input, Flatten
from tensorflow.keras import Model
from tensorflow.keras.utils import get_file

# CNN2SNN imports
from cnn2snn import load_quantized_model, quantize

from ..layer_blocks import conv_block, dense_block

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/vgg/'


def vgg_cifar10(input_shape=(32, 32, 3),
                classes=10,
                weights=None,
                weight_quantization=0,
                activ_quantization=0,
                input_weight_quantization=None):
    """Instantiates a vgg-like model for the "Cifar-10" example.
    This model is based on the vgg architecture, mainly with fewer layers.
    The weights and activations are quantized such that it can be converted into
    an Akida model.
    This architecture is inspired by vgg.

    Args:
        input_shape (tuple): input shape tuple of the model
        classes (int): number of classes to classify images into
        weights (str): one of `None` (random initialization) or the path to the
            weights file to be loaded.
        weight_quantization (int): sets all weights in the model to have
            a particular quantization bitwidth except for the weights in the
            first layer.

            * '0' implements floating point 32-bit weights
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization (int): sets all activations in the model to have a.
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        input_weight_quantization (int): sets weight quantization in the first
            layer. Defaults to weight_quantization value.

            * 'None' implements the same bitwidth as the other weights.
            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.

    Returns:
        tf.keras.Model: a quantized Keras model for vgg/cifar10
    """
    # Overrides input weight quantization if None
    if input_weight_quantization is None:
        input_weight_quantization = weight_quantization

    img_input = Input(shape=input_shape)

    x = conv_block(img_input,
                   filters=128,
                   kernel_size=(3, 3),
                   name='conv_0',
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True)

    x = conv_block(x,
                   filters=128,
                   kernel_size=(3, 3),
                   name='conv_1',
                   padding='same',
                   use_bias=False,
                   pooling='max',
                   add_batchnorm=True,
                   add_activation=True)

    x = conv_block(x,
                   filters=256,
                   kernel_size=(3, 3),
                   name='conv_2',
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True)

    x = conv_block(x,
                   filters=256,
                   kernel_size=(3, 3),
                   name='conv_3',
                   padding='same',
                   use_bias=False,
                   pooling='max',
                   add_batchnorm=True,
                   add_activation=True)

    x = conv_block(x,
                   filters=512,
                   name='conv_4',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True)

    x = conv_block(x,
                   filters=512,
                   kernel_size=(3, 3),
                   name='conv_5',
                   padding='same',
                   use_bias=False,
                   pooling='max',
                   add_batchnorm=True,
                   add_activation=True)

    x = conv_block(x,
                   filters=1024,
                   kernel_size=(1, 1),
                   name='conv_6',
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True)

    x = Flatten()(x)

    x = dense_block(x,
                    units=1024,
                    name='dense_7',
                    use_bias=False,
                    add_batchnorm=True,
                    add_activation=True)

    x = dense_block(x,
                    units=classes,
                    name='dense_8',
                    use_bias=False,
                    add_batchnorm=False,
                    add_activation=False)

    model = Model(img_input, x, name='vgg_cifar10')

    # Load weights
    if weights is not None:
        model.load_weights(weights, by_name=True)

    if ((weight_quantization != 0) or (activ_quantization != 0) or
        (input_weight_quantization != 0)):
        return quantize(model, weight_quantization, activ_quantization,
                        input_weight_quantization)
    else:
        return model


def vgg_cifar10_pretrained():
    model_name = 'vgg_cifar10_wq2_aq2.hdf5'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          cache_subdir='models')
    return load_quantized_model(model_path)
