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
class QZinnerCNOTNN(object):
    def describe(self): return self.__class__.__name__
    def __init__(self, **kargs):
        
        self.m_nqubits = kargs['nqubits']
        self.m_use_quple = kargs['use_quple']
        if self.m_use_quple:
            self.m_nlayers = kargs['nlayers']

        logging.getLogger(__name__)

    # Now build a two-layered model, matching the data-circuit size, and include the preparation and readout operations.
    def create_quantum_model(self, size):
        circuit, readout = None, None
        '''Create a QNN model circuit and readout operation to go along with it.'''
        cq_1 = quple.ParameterisedCircuit(n_qubit=self.m_nqubits, rotation_blocks=['RX','RZ'], copies=1, entanglement_blocks=['CNOT'], final_rotation_layer=False, entangle_strategy='nearest_neighbor')
        cq_2 = quple.ParameterisedCircuit(n_qubit=self.m_nqubits, rotation_blocks=['RX','RY','RZ'], copies=self.m_nlayers, entanglement_blocks=['CNOT'], final_rotation_layer=False, entangle_strategy='nearest_neighbor')
        cq_3 = quple.ParameterisedCircuit(n_qubit=self.m_nqubits, rotation_blocks=['RX','RY'], copies=1, final_rotation_layer=False, entangle_strategy='nearest_neighbor')
        circuit = quple.merge_pqc([cq_1,cq_2,cq_3])

        # Finally, prepare the readout qubit.
        readout = cirq.GridQubit(-1, -1) # a single qubit at [-1,-1]
        circuit.append(cirq.H(readout))
        add_output_layer(circuit, readout, cirq.ZZ, 'zz')
        circuit.append(cirq.H(readout))
        return circuit, cirq.Z(readout)

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
            ]
        )

        def hinge_accuracy(y_true, y_pred):
            y_true = tf.squeeze(y_true) > 0.0
            y_pred = tf.squeeze(y_pred) > 0.0
            result = tf.cast(y_true == y_pred, tf.float32)
            return tf.reduce_mean(result)
            
        model.compile(loss=tf.keras.losses.Hinge(),
            optimizer=tf.keras.optimizers.Adam(),
            metrics=[hinge_accuracy],
            )
        model.summary(print_fn=logging.getLogger(__name__).info)

        return model

QuantumNeuralNetwork = QZinnerCNOTNN
