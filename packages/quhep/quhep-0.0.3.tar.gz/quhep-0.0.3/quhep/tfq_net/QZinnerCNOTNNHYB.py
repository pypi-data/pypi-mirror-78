#!/usr/bin/env python
# Rui Zhang 7.2020
# rui.zhang@cern.ch

import logging

import tensorflow as tf
import tensorflow_quantum as tfq
import sympy
import cirq

import quple

def add_output_layer(circuit, output, gate, prefix):
    for i, qubit in enumerate(circuit.all_qubits()):
        if output == qubit:
            continue
        symbol = sympy.Symbol(prefix + '-' + str(i))
        circuit.append(gate(qubit, output)**symbol)

class CircuitLayerBuilder():
    def __init__(self, data_qubits, readout):
        self.data_qubits = data_qubits
        self.readout = readout
    
    def add_layer(self, circuit, gate, prefix):
        for i, qubit in enumerate(self.data_qubits):
            symbol = sympy.Symbol(prefix + '-' + str(i))
            circuit.append(gate(qubit, self.readout)**symbol)
'''
Develop your own Quantum Neural Network and make a link to the class at the bottom:
QuantumNeuralNetwork = YourClassName
'''
class QZinnerCNOTNNHYB(object):
    def describe(self): return self.__class__.__name__
    def __init__(self, **kargs):
        
        self.m_nqubits = kargs['nqubits']
        self.m_loss = kargs['loss']
        self.m_use_quple = kargs['use_quple']
        self.m_nlayers = kargs['nlayers']

        logging.getLogger(__name__)

    # Now build a two-layered model, matching the data-circuit size, and include the preparation and readout operations.
    def create_quantum_model(self, size):
        circuit, readout = None, None
        '''Create a QNN model circuit and readout operation to go along with it.'''
        cq_1 = quple.ParameterisedCircuit(n_qubit=self.m_nqubits, rotation_blocks=['RY','RZ'], copies=1, entanglement_blocks=['CNOT'], final_rotation_layer=False, entangle_strategy='nearest_neighbor')
        cq_2 = quple.ParameterisedCircuit(n_qubit=self.m_nqubits, rotation_blocks=['RX','RY','RZ'], copies=self.m_nlayers, entanglement_blocks=['CNOT'], final_rotation_layer=False, entangle_strategy='nearest_neighbor')
        cq_3 = quple.ParameterisedCircuit(n_qubit=self.m_nqubits, rotation_blocks=['RY'], copies=1, final_rotation_layer=False, entangle_strategy='nearest_neighbor')
        circuit = quple.merge_pqc([cq_1,cq_2,cq_3])

        # # Finally, prepare the readout qubit.
        # readout = cirq.GridQubit(-1, -1) # a single qubit at [-1,-1]
        # circuit.append(cirq.H(readout))
        # add_output_layer(circuit, readout, cirq.ZZ, 'zz')
        # circuit.append(cirq.H(readout))
        # return circuit, cirq.Z(readout)
        return circuit, [cirq.Z(i) for i in circuit.all_qubits()]

    def get_quantum_model(self, input_size):
        # Build the model circuit
        model_circuit, model_readout = self.create_quantum_model(size=(1, input_size))
        self.m_circuit = cirq.Circuit()
        self.m_circuit.append([model_circuit, model_readout])
        # SVGCircuit(model_circuit)
        logging.info(f'model circuit:\n{model_circuit}')

        # Build the Keras model
        model = tf.keras.Sequential(
            [
                # The input is the data-circuit, encoded as a tf.string
                tf.keras.layers.Input(shape=(), dtype=tf.string),
                # The PQC layer returns the expected value of the readout gate, range [-1,1].
                tfq.layers.PQC(model_circuit, model_readout),
                tf.keras.layers.Dense(1, activation='sigmoid', name='output'),
            ]
        )
        print('zhangr self.m_loss', self.m_loss)

        starter_learning_rate = 0.02
        end_learning_rate = 0.005
        decay_steps = 1000
        learning_rate_fn = tf.keras.optimizers.schedules.PolynomialDecay(
            starter_learning_rate,
            decay_steps,
            end_learning_rate,
            power=0.5)
            
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
                optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate_fn, ),
                metrics=['accuracy',tf.keras.metrics.AUC()])
        model.summary(print_fn=logging.getLogger(__name__).info)

        return model

QuantumNeuralNetwork = QZinnerCNOTNNHYB
