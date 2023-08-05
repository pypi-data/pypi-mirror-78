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
 akida_models main command-line interface

 This package entry-point allows akida models to be instantiated and saved at a
 specified location.

"""

import argparse

from .cifar10.model_ds_cnn import ds_cnn_cifar10
from .cifar10.model_vgg import vgg_cifar10


def main():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest="action")
    c_parser = sp.add_parser("create", help="Create an akida Keras model")
    c_parser.add_argument("-s",
                          "--save_model",
                          type=str,
                          default=None,
                          help="The path/name to use to save the model")
    csp = c_parser.add_subparsers(dest="model",
                                  help="The type of model to be instantiated")
    csp.add_parser(
        "ds_cnn_cifar10",
        help="A Depthwise Separable CIFAR10 model inspired by MobileNet")
    csp.add_parser("vgg_cifar10", help="A VGG-like CIFAR10 model")
    args = parser.parse_args()
    if args.action == "create":
        # Check extension
        if args.model == "ds_cnn_cifar10":
            model = ds_cnn_cifar10()
        elif args.model == "vgg_cifar10":
            model = vgg_cifar10()
        # No need for default behaviour as the command-line parser only accepts
        # valid model types
        if args.save_model is None:
            model_path = f"{args.model}.h5"
        else:
            model_path = args.save_model
            # If needed, add the extension
            if not model_path.endswith(".h5"):
                model_path = f"{model_path}.h5"
        model.save(model_path, include_optimizer=False)
        print(f"Model saved as {model_path}")
