#!/usr/bin/env python
# Rui Zhang 7.2020
# rui.zhang@cern.ch

import logging

import tensorflow as tf
import tensorflow_quantum as tfq
import numpy as np
import sympy
import cirq

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
class QEfficientSU2NNQNN(object):
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
        num_parameters = (size[1]+1)*size[1]*2

        symb = sympy.symbols('θ_0:'+str(num_parameters))
        symbols = np.array(symb)
        symbols = symbols.reshape(size[1]+1, size[1], 2)

        for i, qubit in enumerate(data_qubits):
            circuit.append(cirq.ry(symbols[0][i][0])(qubit))
            circuit.append(cirq.rz(symbols[0][i][1])(qubit))
            param_idx += 2

        for d in range(self.m_nlayers):
            for src, targ in entangler_map:
                circuit.append(cirq.CNOT(data_qubits[src],data_qubits[targ]))
            for i, qubit in enumerate(data_qubits):
                circuit.append(cirq.ry(symbols[d+1][i][0])(qubit))
                circuit.append(cirq.rz(symbols[d+1][i][1])(qubit))
                param_idx += 2

        readout = cirq.GridQubit(-1, -1) # a single qubit at [-1,-1]
        circuit.append(cirq.H(readout))
        add_output_layer(circuit, readout, cirq.YY, 'yy')
        add_output_layer(circuit, readout, cirq.ZZ, 'zz')
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
    
        if self.m_loss == 'hinge':
            def hinge_accuracy(y_true, y_pred):
                y_true = tf.squeeze(y_true) > 0.0
                y_pred = tf.squeeze(y_pred) > 0.0
                result = tf.cast(y_true == y_pred, tf.float32)
                return tf.reduce_mean(result)
                
            model.compile(loss=tf.keras.losses.Hinge(),
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.01, ),
                metrics=[hinge_accuracy],
                )
            
        model.summary(print_fn=logging.getLogger(__name__).info)

        return model

QuantumNeuralNetwork = QEfficientSU2NNQNN