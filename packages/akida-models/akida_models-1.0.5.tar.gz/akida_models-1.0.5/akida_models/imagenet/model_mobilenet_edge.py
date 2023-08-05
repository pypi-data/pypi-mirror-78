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
"""
This model is an adaptation of the `mobilenet_imagenet` model for edge
applications. It is based on MobileNetBC with top layers replaced by a quantized
spike extractor and a classification layer.

It comes with a `mobilenet_edge_imagenet_pretrained` helper method that loads a
set of pretrained weights on a Mobilenet 0.5 that can be run on Akida hardware.

The following tables describes the expected results using the provided weights:
-----------------------------------------------------
            Model           | Top 1 Acc | Top 5 Acc
-----------------------------------------------------
|  Keras 0.5 MobileNet-224  |   51.5 %  |   76.2 %  |
|  Akida 0.5 MobileNet-224  |   52.0 %  |   76.4 %  |

# Reference

- [MobileNets: Efficient Convolutional Neural Networks for
   Mobile Vision Applications](https://arxiv.org/pdf/1704.04861.pdf))

"""
import os

# Tensorflow/Keras imports
from tensorflow.keras import Model
from tensorflow.keras.utils import get_file
from tensorflow.keras.layers import Reshape, Dropout, Activation

# CNN2SNN imports
from cnn2snn import load_quantized_model

# Local utils
from .model_mobilenet import mobilenet_imagenet
from ..quantization_blocks import separable_conv_block, dense_block

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/mobilenet_edge/'


def mobilenet_edge_imagenet(input_shape=None,
                            alpha=1.0,
                            dropout=1e-3,
                            weights=None,
                            classes=1000,
                            weight_quantization=0,
                            activ_quantization=0,
                            input_weight_quantization=None):
    """Instantiates a MobileNet-edge architecture.

    Args:
        input_shape (tuple): optional shape tuple.
        alpha (float): controls the width of the model.

            * If `alpha` < 1.0, proportionally decreases the number of filters
              in each layer.
            * If `alpha` > 1.0, proportionally increases the number of filters
              in each layer.
            * If `alpha` = 1, default number of filters from the paper are used
              at each layer.
        weights (str): one of `None` (random initialization) or the path to the
            weights file to be loaded.
        classes (int): optional number of classes to classify images
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
    # check if overrides have been provided and override
    if input_weight_quantization is None:
        input_weight_quantization = weight_quantization

    # Create a MobileNetBC network without top layers
    base_model = mobilenet_imagenet(
        input_shape=input_shape,
        alpha=alpha,
        dropout=dropout,
        include_top=False,
        weights=None,
        pooling='avg',
        classes=classes,
        weight_quantization=weight_quantization,
        activ_quantization=activ_quantization,
        input_weight_quantization=input_weight_quantization)

    input_shape = base_model.input_shape

    # Prepare the model for adding a new end layer
    x = base_model.layers[-1].output
    x = Reshape((1, 1, int(1024 * alpha)), name='reshape_1')(x)
    x = Dropout(dropout, name='dropout')(x)

    # Add the new end layer with kernel_size (3, 3) instead of (1,1) for
    # hardware compatibility reasons
    x = separable_conv_block(x,
                             filters=2048,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             name='spike_generator',
                             weight_quantization=weight_quantization,
                             activ_quantization=1)

    # Then add the Akida edge learning layer that will be dropped after
    # NOTE: weight_quantization set to 2 here, to be as close as
    # possible to the Akida native layer that will replace this one,
    # with binary weights.
    x = dense_block(x,
                    classes,
                    name="classification_layer",
                    weight_quantization=2,
                    activ_quantization=None,
                    add_batchnorm=False,
                    use_bias=False)
    x = Activation('softmax', name='act_softmax')(x)
    x = Reshape((classes,), name='reshape_2')(x)

    # Create model
    model = Model(inputs=base_model.input,
                  outputs=x,
                  name='mobilenet_edge_%0.2f_%s' % (alpha, input_shape[0]))

    # Load weights
    if weights is not None:
        model.load_weights(weights, by_name=True)

    return model


def mobilenet_edge_imagenet_pretrained():
    model_name = 'mobilenet_imagenet_edge_wq4_aq4.h5'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          cache_subdir='models')
    return load_quantized_model(model_path)
