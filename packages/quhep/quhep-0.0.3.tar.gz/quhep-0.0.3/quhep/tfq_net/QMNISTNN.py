#!/usr/bin/env python
# Rui Zhang 7.2020
# rui.zhang@cern.ch

import logging

import tensorflow as tf
import tensorflow_quantum as tfq
import sympy
import cirq

from quple.trial_wavefunction.real_amplitudes import RealAmplitudes

def add_output_layer(circuit, output, gate, prefix):
    for i, qubit in enumerate(circuit.qubits):
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
class QMNISTNN(object):
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
        data_qubits = cirq.GridQubit.rect(size[0], size[1])  # match data-circuit defined in `convert_to_circuit`
        readout = cirq.GridQubit(-1, -1) # a single qubit at [-1,-1]
        circuit = cirq.Circuit()
        # Prepare the readout qubit.
        circuit.append(cirq.X(readout))
        circuit.append(cirq.H(readout))
        builder = CircuitLayerBuilder(
            data_qubits = data_qubits,
            readout=readout)
        # Then add layers (experiment by adding more).
        builder.add_layer(circuit, cirq.XX, "xx1")
        builder.add_layer(circuit, cirq.ZZ, "zz1")

        # Finally, prepare the readout qubit.
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

QuantumNeuralNetwork = QMNISTNN