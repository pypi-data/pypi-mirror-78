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
 CIFAR10 model training script
"""

# System imports
import os
import sys
import argparse

# Keras imports
import tensorflow.keras.backend as K
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import LearningRateScheduler, EarlyStopping
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Akida
from cnn2snn import load_quantized_model


def get_rescaled_data_set(a, b):

    #The data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # Convert class vectors to binary class matrices.
    # For hinge loss, we need to rescale them between -1 and 1
    y_train = to_categorical(y_train, 10) * 2 - 1
    y_labels = y_test
    y_test = to_categorical(y_test, 10) * 2 - 1

    x_train = x_train.reshape(x_train.shape[0], 32, 32, 3)
    x_test = x_test.reshape(x_test.shape[0], 32, 32, 3)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    # Rescale inputs for Keras
    x_train = (x_train - b) / a
    x_test = (x_test - b) / a

    return x_train, y_train, x_test, y_test


def train_model(model,
                x_train,
                y_train,
                x_test,
                y_test,
                batch_size=500,
                epochs=1000):

    callbacks = []

    # Learning rate: be more aggressive at the beginning, and apply decay
    lr_start = 1e-3
    lr_end = 1e-4
    lr_decay = (lr_end / lr_start)**(1. / epochs)

    lr_scheduler = LearningRateScheduler(lambda e: lr_start * lr_decay**e)
    callbacks.append(lr_scheduler)

    # Initialize optimizer
    opt = Adam(lr=lr_start)

    # Compile model
    model.compile(loss='squared_hinge', optimizer=opt, metrics=['accuracy'])

    # Use data augmentation
    datagen_args = {}
    # random hz image shift (fraction of width)
    datagen_args['width_shift_range'] = 0.1
    # random vert image shft (fraction of height)
    datagen_args['height_shift_range'] = 0.1
    # Randomly flip images
    datagen_args['horizontal_flip'] = True

    datagen = ImageDataGenerator(**datagen_args)

    training_data = datagen.flow(x_train, y_train, batch_size=batch_size)

    history = model.fit(training_data,
                        steps_per_epoch=len(x_train) / batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(x_test, y_test),
                        callbacks=callbacks)


def tune_model(model,
               x_train,
               y_train,
               x_test,
               y_test,
               batch_size=500,
               epochs=100):

    # Initialize optimizer
    opt = Adam(lr=1e-4)

    # Compile model
    model.compile(loss='squared_hinge', optimizer=opt, metrics=['accuracy'])

    # Early stop when loss has stopped decreasing
    callbacks = []
    es = EarlyStopping(monitor='loss',
                       mode='min',
                       patience=20,
                       restore_best_weights=True)
    callbacks.append(es)

    history = model.fit(x_train,
                        y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(x_test, y_test),
                        callbacks=callbacks)


def evaluate_model(model, x_test, y_test):

    # Initialize optimizer
    opt = Adam(lr=1e-4)

    # Compile model
    model.compile(loss='squared_hinge', optimizer=opt, metrics=['accuracy'])

    score, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print('Test accuracy:', accuracy)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m",
                        "--model",
                        type=str,
                        required=True,
                        help="Model to be trained or tuned")
    parser.add_argument("-s",
                        "--savemodel",
                        type=str,
                        default=None,
                        help="Save model with the specified name")
    parser.add_argument("-e",
                        "--epochs",
                        type=int,
                        default=0,
                        help="The number of training epochs")
    parser.add_argument("-b",
                        "--batch_size",
                        type=int,
                        default=500,
                        help="The training batch size")

    sp = parser.add_subparsers(dest="action")
    sp.add_parser(
        "train",
        help="Train a Keras model (data augmentation, decreasing learning rate)"
    )
    sp.add_parser(
        "tune",
        help="Tune a pre-trained Keras model (low learning rate, early stop)")

    args = parser.parse_args()

    # Load the source model
    model = load_quantized_model(args.model)

    # Train or tune

    # Akida is configured to take 8-bit inputs without rescaling
    # but for the training, we use float weights between 0 and 1
    x_train, y_train, x_test, y_test = get_rescaled_data_set(255, 0)

    # Training parameters
    epochs = args.epochs

    if epochs > 0:
        if args.action == "train":
            train_model(model,
                        x_train,
                        y_train,
                        x_test,
                        y_test,
                        batch_size=args.batch_size,
                        epochs=epochs)
        else:
            tune_model(model,
                       x_train,
                       y_train,
                       x_test,
                       y_test,
                       batch_size=args.batch_size,
                       epochs=epochs)

    # Save Model in Keras format (hdf5)
    if args.savemodel:
        model.save(args.savemodel, include_optimizer=False)
        print(f"Trained model saved as {args.savemodel}")

    # Evaluate model accuracy
    evaluate_model(model, x_test, y_test)


if __name__ == "__main__":
    main()
