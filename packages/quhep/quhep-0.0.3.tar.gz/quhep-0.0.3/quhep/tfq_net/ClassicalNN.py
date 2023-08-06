#!/usr/bin/env python
# Rui Zhang 7.2020
# rui.zhang@cern.ch

import tensorflow as tf

def get_classicial_model(num_var):
    # A simple model based off LeNet from https://keras.io/examples/mnist_cnn/
    cmodel = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(num_var, activation='relu'),
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(10, activation='relu'),
            # tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(1, activation='sigmoid'),
        ]
    )

    cmodel.compile(loss='mse',
        optimizer=tf.keras.optimizers.Adam(),
        metrics=['accuracy',tf.keras.metrics.AUC()]
        )
    
    return cmodel
