#!/usr/bin/env python
# Rui Zhang 7.2020
# rui.zhang@cern.ch

import logging

import tensorflow as tf
import tensorflow_quantum as tfq
import numpy as np
import sympy
import cirq

'''
Develop your own Quantum Neural Network and make a link to the class at the bottom:
QuantumNeuralNetwork = YourClassName
'''
class QEfficientSU2NNHYB(object):
    def describe(self): return self.__class__.__name__
    def __init__(self, **kargs):
        
        self.m_nqubits = kargs['nqubits']
        self.m_loss = kargs['loss']
        self.m_use_quple = kargs['use_quple']
        self.m_nlayers = kargs['nlayers']

        logging.getLogger(__name__)

    def create_quantum_model(self, size):
        """Create a QNN model circuit and readout operation to go along with it."""
        data_qubits = cirq.GridQubit.rect(size[0], size[1]) 
        circuit = cirq.Circuit()

        entangler_map= [[i, i + 1] for i in range(size[1] - 1)]

        param_idx = 0
        num_parameters = (self.m_nlayers+1)*size[1]*2

        symb = sympy.symbols('θ_0:'+str(num_parameters))
        symbols = np.array(symb)
        symbols = symbols.reshape(self.m_nlayers+1, size[1], 2)

        for i, qubit in enumerate(data_qubits):
            circuit.append(cirq.rz(symbols[0][i][1])(qubit))
            circuit.append(cirq.ry(symbols[0][i][0])(qubit))
            param_idx += 2

        for d in range(self.m_nlayers):
            for src, targ in entangler_map:
                circuit.append(cirq.CNOT(data_qubits[src],data_qubits[targ]))
            for i, qubit in enumerate(data_qubits):
                circuit.append(cirq.rz(symbols[d+1][i][1])(qubit))
                circuit.append(cirq.ry(symbols[d+1][i][0])(qubit))
                param_idx += 2
        return circuit, [cirq.Z(i) for i in circuit.all_qubits()]

    def get_quantum_model(self, input_size):
        # Build the model circuit
        model_circuit, model_readout = self.create_quantum_model(size=(1, input_size))
        self.m_circuit = cirq.Circuit()
        self.m_circuit.append([model_circuit, model_readout])
        # SVGCircuit(model_circuit)
        logging.info(f'model circuit:\n{model_circuit}')

        # Build the Keras model
        # initializer = tf.keras.initializers.Constant(1. / input_size)
        import tensorflow_core.python.keras as keras
        model = tf.keras.Sequential(
            [
                # The input is the data-circuit, encoded as a tf.string
                tf.keras.layers.Input(shape=(), dtype=tf.string),
                # The PQC layer returns the expected value of the readout gate, range [-1,1].
                tfq.layers.PQC(model_circuit, model_readout, regularizer=keras.regularizers.l2(0.0001)),
                # tf.keras.layers.Dense(1, activation='sigmoid', kernel_initializer=initializer, name='output'),
                tf.keras.layers.Dense(1, activation='sigmoid', name='output'),
            ]
        )
        logging.info(f'PQC regularizer is l2')
        # model.layers[-1].trainable = False

        starter_learning_rate = 0.02
        end_learning_rate = 0.005
        decay_steps = 1000
        learning_rate_fn = tf.keras.optimizers.schedules.PolynomialDecay(
            starter_learning_rate,
            decay_steps,
            end_learning_rate,
            power=0.5)


        # step = tf.Variable(0, trainable=False)
        # boundaries = [100, 250]
        # values = [0.02, 0.01, 0.005]
        # learning_rate_fn = tf.keras.optimizers.schedules.PiecewiseConstantDecay(
        #     boundaries, values)

        if self.m_loss == 'hinge':
            def hinge_accuracy(y_true, y_pred):
                y_true = tf.squeeze(y_true) > 0.0
                y_pred = tf.squeeze(y_pred) > 0.0
                result = tf.cast(y_true == y_pred, tf.float32)
                return tf.reduce_mean(result)
                
            model.compile(loss=tf.keras.losses.Hinge(),
                optimizer=tf.keras.optimizers.Adam(),
                metrics=[hinge_accuracy],
                )
        elif self.m_loss == 'mse':
            model.compile(
                loss='mse',
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.01, ),
                metrics=['accuracy',tf.keras.metrics.AUC()])
        elif self.m_loss == 'mse2':
            model.compile(
                loss='mse',
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.02, ),
                metrics=['accuracy',tf.keras.metrics.AUC()])
        elif self.m_loss == 'mse_Adam':
            model.compile(
                loss='mse',
                optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate_fn, ),
                metrics=['accuracy',tf.keras.metrics.AUC()])
        elif self.m_loss == 'mse_Adadelta':
            model.compile(
                loss='mse',
                optimizer=tf.keras.optimizers.Adadelta(),
                metrics=['accuracy',tf.keras.metrics.AUC()])
        elif self.m_loss == 'mse_Adamax':
            model.compile(
                loss='mse',
                optimizer=tf.keras.optimizers.Adamax(),
                metrics=['accuracy',tf.keras.metrics.AUC()])
        elif self.m_loss == 'mse_Nadam':
            model.compile(
                loss='mse',
                optimizer=tf.keras.optimizers.Nadam(),
                metrics=['accuracy',tf.keras.metrics.AUC()])
        elif self.m_loss == 'mse_SGD':
            model.compile(
                loss='mse',
                optimizer=tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.3, nesterov=False),
                metrics=['accuracy',tf.keras.metrics.AUC()])
        elif self.m_loss == 'mse_SGD_PolynomialDecay':
            model.compile(
                loss='mse',
                optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate_fn),
                metrics=['accuracy',tf.keras.metrics.AUC()])
        elif self.m_loss == 'mse_RMSprop':
            model.compile(
                loss='mse',
                optimizer=tf.keras.optimizers.RMSprop(),
                metrics=['accuracy',tf.keras.metrics.AUC()])

                
        logging.info(f'model loss is {self.m_loss}')
          
        model.summary(print_fn=logging.getLogger(__name__).info)

        return model

QuantumNeuralNetwork = QEfficientSU2NNHYB
