#!/usr/bin/env python
# Rui Zhang 8.2020
# rui.zhang@cern.ch

import numpy as np
import torch.nn as nn
import qiskit
import torch
from torch.autograd import Function

class QuantumCircuit:
    """ 
    This class provides a simple interface for interaction 
    with the quantum circuit 
    """
    
    def __init__(self, n_qubits, backend, shots):
        # --- Circuit definition ---
        print('zhangr QuantumCircuit init')
        self._circuit = qiskit.QuantumCircuit(n_qubits)
        
        all_qubits = [i for i in range(n_qubits)]
        self.parameters = [qiskit.circuit.Parameter(f'θ_{i}') for i in range(n_qubits)]
        # self.parameters = [qiskit.circuit.Parameter(f'θ_0'), qiskit.circuit.Parameter(f'θ_1')]
        print('zhangr self.parameters', self.parameters[0], n_qubits)
        
        self._circuit.h(all_qubits)
        self._circuit.barrier()
        for theta, qubit in zip(self.parameters, all_qubits):
            self._circuit.ry(theta, qubit)
        # self._circuit.ry(self.parameters[0], all_qubits[0])
        # self._circuit.ry(self.parameters[1], all_qubits[1])
        
        self._circuit.measure_all()
        # ---------------------------

        self.backend = backend
        self.shots = shots
    
    def run(self, thetas):
        print('zhangr self.parameters', self.parameters[0])
        print('zhangr thetas', thetas)
        print('zhangr dict(zip(self.parameters, thetas)))', [{self.parameters[i]: thetas[0][i]} for i in range(2)])

        total_results = {}
        for theta_event in thetas:
            print('zhangr theta_event', theta_event)
            job = qiskit.execute(self._circuit, 
                                self.backend, 
                                shots = self.shots,
                                parameter_binds = [dict(zip(self.parameters, theta_event)) ])
            result = job.result().get_counts(self._circuit)
            total_results = {x: total_results.get(x, 0) + result.get(x, 0) for x in set(total_results).union(result)}
            print('zhangr result', result)
            print('zhangr total_results', total_results)
        
        counts = np.array(list(result.values()))
        states = np.array(list(result.keys())).astype(float)
        
        # Compute probabilities for each state
        probabilities = counts / self.shots
        # Get state expectation
        print('zhangr states', states)
        print('zhangr probabilities', probabilities)
        expectation = np.sum(states * probabilities)
        
        return np.array([expectation])

class HybridFunction(Function):
    """ Hybrid quantum - classical function definition """
    
    @staticmethod
    def forward(ctx, input, quantum_circuit, shift):
        """ Forward pass computation """
        ctx.shift = shift
        ctx.quantum_circuit = quantum_circuit

        print('zhangr input forward', input, input.tolist())
        expectation_z = ctx.quantum_circuit.run(input.tolist())
        print('zhangr expectation_z', expectation_z)
        result = torch.tensor([expectation_z])
        ctx.save_for_backward(input, result)

        return result
        
    @staticmethod
    def backward(ctx, grad_output):
        """ Backward pass computation """
        input, expectation_z = ctx.saved_tensors
        input_list = np.array(input.tolist())
        
        shift_right = input_list + np.ones(input_list.shape) * ctx.shift
        shift_left = input_list - np.ones(input_list.shape) * ctx.shift
        
        gradients = []
        for i in range(len(input_list)):
            expectation_right = ctx.quantum_circuit.run(shift_right[i]) / (2 * ctx.shift)
            expectation_left  = ctx.quantum_circuit.run(shift_left[i]) / (2 * ctx.shift)
            
            gradient = torch.tensor([expectation_right]) - torch.tensor([expectation_left])
            gradients.append(gradient)
        gradients = np.array([gradients]).T
        return torch.tensor([gradients]).float() * grad_output.float(), None, None


class Hybrid(nn.Module):
    """ Hybrid quantum - classical layer definition """
    
    def __init__(self, nqubits, backend, shots, shift):
        super(Hybrid, self).__init__()
        # module = importlib.import_module(f'quhep.qsk_circ.QuantumCircuit')
        self.quantum_circuit = QuantumCircuit(nqubits, backend, shots)
        self.shift = shift
        
    def forward(self, input):
        # module = importlib.import_module(f'quhep.qsk_prop.HybridFunction')
        return HybridFunction.apply(input, self.quantum_circuit, self.shift)

    def circuit(self):
        return self.quantum_circuit

    def plot_circuit(self, filename):
        if filename.endswith('.pdf') or filename.endswith('.txt'):
            filename = filename[:-4]
        circuit_drawer(self.quantum_circuit._circuit, filename=f'{filename}.pdf', output='mpl')
        logging.info(f'\n{self.quantum_circuit._circuit.draw()}')
        logging.info(f'Circuits stored in: f"{filename}.pdf"')

class Net(nn.Module):
    def __init__(self, nqubits, shots = 1000, shift = 0.05):
        super(Net, self).__init__()
        self.m_nqubits = nqubits
        self.input = nn.Linear(self.m_nqubits, self.m_nqubits)
        self.hybrid = Hybrid(self.m_nqubits, qiskit.Aer.get_backend('qasm_simulator'), shots, shift)
        self.output = nn.Linear(self.m_nqubits, 1)

    def forward(self, x):
        print('zhangr ax input', x.shape, x)
        x = self.input(x)
        print('zhangr bx after input', x.shape, x)
        x = self.hybrid(x)
        print('zhangr cx after hybrid', x.shape, x)
        # x = self.output(x.float())
        # print('zhangr dx after output', x.shape, x)
        x = torch.sigmoid(x)
        return x
