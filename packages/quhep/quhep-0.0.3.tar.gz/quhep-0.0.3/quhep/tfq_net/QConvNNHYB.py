#!/usr/bin/env python
# Rui Zhang 8.2020
# rui.zhang@cern.ch

import logging
import numpy as np
from math import ceil
import tensorflow as tf
import tensorflow_quantum as tfq
import sympy
import cirq

'''
Develop your own Quantum Neural Network and make a link to the class at the bottom:
QuantumNeuralNetwork = YourClassName
'''
class QConvNNHYB(object):
    def describe(self): return self.__class__.__name__
    def __init__(self, **kargs):
        
        self.m_nqubits = kargs['nqubits']
        self.m_single_gates = [cirq.X, cirq.Y, cirq.Z]
        self.m_double_gates = [cirq.ZZ, cirq.YY, cirq.XX]
        self.m_use_quple = kargs['use_quple']
        if self.m_use_quple:
            self.m_nlayers = kargs['nlayers']

        logging.getLogger(__name__)

    def cluster_state_circuit(self, bits):
        """Return a cluster state on the qubits in `bits`."""
        circuit = cirq.Circuit()
        circuit.append(cirq.H.on_each(bits))
        for this_bit, next_bit in zip(bits, bits[1:] + [bits[0]]):
            circuit.append(cirq.CZ(this_bit, next_bit))
        return circuit

    def one_qubit_unitary(self, bit, symbol):
        """Make a Cirq circuit enacting a rotation of the bloch sphere about the X,
        Y and Z axis, that depends on the values in `symbols`.
        """
        return cirq.Circuit([gate(bit)**sympy.Symbol(symbol + '_gate' + str(i)) for i, gate in enumerate(self.m_single_gates)])

    def two_qubit_unitary(self, bits, symbol):
        """Make a Cirq circuit that creates an arbitrary two qubit unitary."""
        circuit = cirq.Circuit()
        circuit += [self.one_qubit_unitary(bits[i], symbol+'_before'+str(i)) for i in range(2)]
        circuit += [gate(*bits)**sympy.Symbol(symbol+'_gate'+str(i)) for i, gate in enumerate(self.m_double_gates)]
        circuit += [self.one_qubit_unitary(bits[i], symbol+'_after'+str(i)) for i in range(2)]
        return circuit

    def two_qubit_pool(self, source_qubit, sink_qubit, symbol):
        """Make a Cirq circuit to do a parameterized 'pooling' operation, which
        attempts to reduce entanglement down from two qubits to just one."""
        pool_circuit = cirq.Circuit()
        sink_basis_selector = self.one_qubit_unitary(sink_qubit, symbol+'_sink')
        source_basis_selector = self.one_qubit_unitary(source_qubit, symbol+'_sour')
        pool_circuit.append(sink_basis_selector)
        pool_circuit.append(source_basis_selector)
        pool_circuit.append(cirq.CNOT(control=source_qubit, target=sink_qubit))
        pool_circuit.append(sink_basis_selector**-1)
        return pool_circuit

    def quantum_conv_circuit(self, bits, symbol):
        """Quantum Convolution Layer following the above diagram.
        Return a Cirq circuit with the cascade of `two_qubit_unitary` applied
        to all pairs of qubits in `bits` as in the diagram above.
        """
        circuit = cirq.Circuit()
        for adjacence in zip(bits[0::2], bits[1::2] + [bits[0]]):
            circuit += self.two_qubit_unitary(adjacence, symbol)
        for adjacence in zip(bits[1::2], bits[2::2] + [bits[0]]):
            circuit += self.two_qubit_unitary(adjacence, symbol)
        return circuit

    def quantum_pool_circuit(self, bits, symbol):
        """A layer that specifies a quantum pooling operation.
        A Quantum pool tries to learn to pool the relevant information from two
        qubits onto 1.
        """
        circuit = cirq.Circuit()
        length = len(bits)
        for source, sink in zip(bits[:int(length/2)], bits[ceil(length/2):]):
            circuit += self.two_qubit_pool(source, sink, symbol)
        return circuit, bits[ceil(length/2):]

    def create_quantum_model(self, qubits):
        """Create sequence of alternating convolution and pooling operators 
        which gradually shrink over time."""
        model_circuit = cirq.Circuit()
        # Cirq uses sympy.Symbols to map learnable variables. TensorFlow Quantum
        # scans incoming circuits and replaces these with TensorFlow variables.
        for i in range(self.m_nlayers):
            model_circuit += self.quantum_conv_circuit(qubits, 'clay'+str(i))
            if i==1: break
            circuit, qubits = self.quantum_pool_circuit(qubits, 'play'+str(i))
            model_circuit += circuit
        # Create our qubits and readout operators in Cirq.
        readout = qubits[-1]
        return model_circuit, cirq.Z(readout)


    def get_quantum_model(self, size):

        # Build a sequential model enacting the logic in 1.3 of this notebook.
        # Here you are making the static cluster state prep as a part of the AddCircuit and the
        # "quantum datapoints" are coming in the form of excitation
        cluster_state_bits = cirq.GridQubit.rect(1, size)
        excitation_input = tf.keras.Input(shape=(), dtype=tf.dtypes.string)
        cluster_state = tfq.layers.AddCircuit()(excitation_input, prepend=self.cluster_state_circuit(cluster_state_bits))
        
        # Build the model circuit
        model_circuit, model_readout = self.create_quantum_model(cluster_state_bits)
        self.m_circuit = cirq.Circuit()
        self.m_circuit.append([model_circuit, model_readout])
        logging.info(f'model circuit:\n{model_circuit}')

        quantum_model = tfq.layers.PQC(model_circuit, model_readout)(cluster_state)
        # qcnn_model = tf.keras.Model(inputs=[excitation_input], outputs=[quantum_model])

        dense = tf.keras.layers.Dense(1)(quantum_model)
        qcnn_model = tf.keras.Model(inputs=[excitation_input], outputs=[dense])

        # Custom accuracy metric.
        @tf.function
        def custom_accuracy(y_true, y_pred):
            y_true = tf.squeeze(y_true)
            y_pred = tf.map_fn(lambda x: 1.0 if x >= 0 else -1.0, y_pred)
            return tf.keras.backend.mean(tf.keras.backend.equal(y_true, y_pred))

        qcnn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01, ), loss=tf.losses.mse, metrics=[custom_accuracy]) #TODO zhangr lr
        qcnn_model.summary(print_fn=logging.getLogger(__name__).info)
        return qcnn_model

    def generate_data(self, qubits):
        """Generate training and testing data."""
        n_rounds = 20  # Produces n_rounds * n_qubits datapoints.
        excitations = []
        labels = []
        for n in range(n_rounds):
            for bit in qubits:
                rng = np.random.uniform(-np.pi, np.pi)
                excitations.append(cirq.Circuit(cirq.rx(rng)(bit)))
                labels.append(1 if (-np.pi / 2) <= rng <= (np.pi / 2) else -1)

        split_ind = int(len(excitations) * 0.7)
        train_excitations = excitations[:split_ind]
        test_excitations = excitations[split_ind:]

        train_labels = labels[:split_ind]
        test_labels = labels[split_ind:]

        return tfq.convert_to_tensor(train_excitations), np.array(train_labels), tfq.convert_to_tensor(test_excitations), np.array(test_labels)

QuantumNeuralNetwork = QConvNNHYB
