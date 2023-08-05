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

from tensorflow.keras import Model
from tensorflow.keras.utils import get_file

# CNN2SNN imports
from cnn2snn import load_quantized_model

from .preprocessing import load_labels_mapping, load_columns_type
from ..tabular_data.tabular_data import create_tse, create_mlp

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/tse_mlp/'


def tse_mlp_cse2018(numerical_columns=None,
                    categorical_columns=None,
                    weights=None,
                    weight_quantization=0,
                    activ_quantization=0,
                    input_weight_quantization=None):
    """Instantiates a model composed of a trainable spike encoder and a
    multilayer perceptron for the tabular data example on CSE-CIC-IDS-2018
    dataset.

    Args:
        numerical_columns (list): list of numerical column names. Will use
            preprocessed data when set to `None`.
        categorical_columns (dict): dictionary of categorical column names
            indexing the list of vocabulary for the column. Will use
            preprocessed data when set to `None`.
        weights (str): one of `None` (random initialization) or the path to the
            weights file to be loaded.
        weight_quantization (int): sets MLP weights in the model to have a
            particular quantization bitwidth

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization: sets all activations in the model to have a
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '1' through '8' implements n-bit weights where n is from 1-8 bits.
        input_weight_quantization: sets weight quantization in the TSE last
            layer. Defaults to weight_quantization value.

            * 'None' implements the same bitwidth as the other weights.
            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
    Returns:
        tf.keras.Model: a Keras model for tabular data on CSE-CIC-IDS-2018
    """
    # Overrides input weight quantization if None
    if input_weight_quantization is None:
        input_weight_quantization = weight_quantization

    labels_mappings = load_labels_mapping()
    n_classes = len(labels_mappings)

    if numerical_columns == None or categorical_columns == None:
        preprocessed_numerical_columns, preprocessed_categorical_columns = load_columns_type(
        )

    if numerical_columns == None:
        numerical_columns = preprocessed_numerical_columns
    if categorical_columns == None:
        categorical_columns = preprocessed_categorical_columns

    mlp_units_list = [128, 128]

    inputs, tse_output = create_tse(
        numerical_columns,
        categorical_columns,
        units=256,
        input_weight_quantization=input_weight_quantization,
        activ_quantization=activ_quantization)
    mlp_output = create_mlp(tse_output,
                            mlp_units_list,
                            n_classes,
                            weight_quantization=weight_quantization,
                            activ_quantization=activ_quantization)
    model = Model(inputs=inputs, outputs=mlp_output)

    # Load weights
    if weights is not None:
        model.load_weights(weights, by_name=True)

    return model


def tse_mlp_cse2018_pretrained():
    model_name = 'tse_mlp_cse2018_wq2_aq4_iq0.tar.gz'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          cache_subdir='models',
                          extract=True)
    file_path = os.path.join(os.path.dirname(model_path),
                             "tse_mlp_cse2018_wq2_aq4_iq0")
    return load_quantized_model(file_path)
