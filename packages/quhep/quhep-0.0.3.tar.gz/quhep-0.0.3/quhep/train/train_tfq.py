#!/usr/bin/env python
# Rui Zhang 6.2020
# rui.zhang@cern.ch

import logging
import importlib

import tensorflow as tf
import tensorflow_quantum as tfq
import sympy
import cirq
from cirq.contrib.svg import SVGCircuit

from quple.trial_wavefunction.real_amplitudes import RealAmplitudes
from quhep.train.train import _train, add_options

class Train(_train):
    def describe(self): return self.__class__.__name__
    def __init__(self, **kargs):
        self.m_use_quple = kargs['use_quple']
        self.m_nlayers = kargs['nlayers'] if self.m_use_quple else None
        self.m_ndepths = kargs['ndepths'] if self.m_use_quple else None
        self.m_encoder_type = kargs['encoder_type'] if self.m_use_quple else None
        self.m_Qnetwork = kargs['Qnetwork']
        self.m_loss = kargs['loss']
        quple_par = f'{self.m_use_quple}-enc{self.m_encoder_type}-Dep{self.m_ndepths}-QNN{self.m_Qnetwork}-L{self.m_nlayers}-l{self.m_loss}' if self.m_use_quple else 'False'
        super().__init__(additional_log=quple_par, **kargs)

    def convert_to_circuit(self, event):
        '''
        Encode variables into quantum datapoint
        Return:
            circuit of the event with qubit number of variable number
        '''
        qubits = cirq.GridQubit.rect(1, len(event))
        circuit = cirq.Circuit()
        for i, variable in enumerate(event):
            circuit.append(cirq.H(qubits[i]))
            circuit.append(cirq.rz(variable)(qubits[i]))
        return circuit

    def convert_to_circuit_with_entangle(self, event, entangle, copies=1):
        '''
        Encode variables into quantum datapoint
        Return:
            circuit of the event with qubit number of variable number
        '''
        qubits = cirq.GridQubit.rect(1, len(event))
        circuit = cirq.Circuit()
        entangle_qubits4 = list(range(4, 10))
        entangle_qubits7 = list(range(7, 10))
        entangle_qubits6r = list(range(6, -1, -1))
        entangle_qubits9r = list(range(9, -1, -1))
        entangle_qubits1r = list(range(1, -1, -1))
        for i, variable in enumerate(event):
            circuit.append(cirq.H(qubits[i]))
            circuit.append(cirq.rz(variable)(qubits[i]))
            # circuit.append(cirq.H(qubits[i]))
        for i, variable in enumerate(event):
            if i < len(entangle):
                if self.m_entangle_gate == 'ry7':
                    circuit.append(cirq.ry(entangle[i])(qubits[entangle_qubits7[i]]))
                elif self.m_entangle_gate == 'rx7':
                    circuit.append(cirq.rx(entangle[i])(qubits[entangle_qubits7[i]]))
                elif self.m_entangle_gate == 'ry4':
                    circuit.append(cirq.ry(entangle[i])(qubits[entangle_qubits4[i]]))
                elif self.m_entangle_gate == 'rx4':
                    circuit.append(cirq.rx(entangle[i])(qubits[entangle_qubits4[i]]))
                elif self.m_entangle_gate == 'ry6r':
                    circuit.append(cirq.ry(entangle[i])(qubits[entangle_qubits6r[i]]))
                elif self.m_entangle_gate == 'rx6r':
                    circuit.append(cirq.rx(entangle[i])(qubits[entangle_qubits6r[i]]))
                elif self.m_entangle_gate == 'ry9r':
                    circuit.append(cirq.ry(entangle[i])(qubits[entangle_qubits9r[i]]))
                elif self.m_entangle_gate == 'rx9r':
                    circuit.append(cirq.rx(entangle[i])(qubits[entangle_qubits9r[i]]))
                elif self.m_entangle_gate == 'ry1r':
                    circuit.append(cirq.ry(entangle[i])(qubits[entangle_qubits1r[i]]))
                elif self.m_entangle_gate == 'rx1r':
                    circuit.append(cirq.rx(entangle[i])(qubits[entangle_qubits1r[i]]))
                elif self.m_entangle_gate == 'ry':
                    circuit.append(cirq.ry(entangle[i])(qubits[i]))
                elif self.m_entangle_gate == 'rx':
                    circuit.append(cirq.rx(entangle[i])(qubits[i]))
        for i, variable in enumerate(event):
            for j in range(copies-1):
                circuit.append(cirq.rz(variable)(qubits[i]))
            circuit.append(cirq.H(qubits[i]))
        return circuit

    def convert_X_to_quantum(self, x_train, x_test, x_val):
        x_train_circ, x_test_circ, x_val_circ = None, None, None
        logging.info(f'Start data encoding')
        if (self.m_use_quple and (not self.m_entangle)):
            # define encoding circuit
            if self.m_encoder_type == 'FirstOrderExpansion':
                encoder = importlib.import_module(f'quple.data_encoding.first_order_expansion')
                cq = encoder.FirstOrderExpansion(feature_dimension=self.m_nqubits, parameter_symbol='data', copies=self.m_ndepths)
            elif self.m_encoder_type == 'SecondOrderExpansion':
                encoder = importlib.import_module('quple.data_encoding.second_order_expansion')
                cq = encoder.SecondOrderExpansion(feature_dimension=self.m_nqubits, parameter_symbol='data', copies=self.m_ndepths)
            else:
                logging.fatal(f'{self.m_encoder_type} is not supported')

            # get resolved circuits for input dataset
            x_train_circ = cq.resolve_parameters(x_train)
            x_test_circ = cq.resolve_parameters(x_test)
            x_val_circ = cq.resolve_parameters(x_val)
            
        else:
            x_train_circ = [self.convert_to_circuit_with_entangle(x[:self.m_nqubits], x[self.m_nqubits:], copies=self.m_ndepths) for x in x_train]
            x_test_circ = [self.convert_to_circuit_with_entangle(x[:self.m_nqubits], x[self.m_nqubits:], copies=self.m_ndepths) for x in x_test]
            x_val_circ = [self.convert_to_circuit_with_entangle(x[:self.m_nqubits], x[self.m_nqubits:], copies=self.m_ndepths) for x in x_val]

        logging.info(f'Finish data encoding. One example training event:\n{x_train_circ[0]}')
        x_train_tfcirc = tfq.convert_to_tensor(x_train_circ)
        x_test_tfcirc = tfq.convert_to_tensor(x_test_circ)
        x_val_tfcirc = tfq.convert_to_tensor(x_val_circ)
        logging.debug(tfq.from_tensor(x_train_tfcirc)[0])

        return x_train_tfcirc, x_test_tfcirc, x_val_tfcirc

    def train_quantum_model(self):
        x_train_tfcirc, x_test_tfcirc, x_val_tfcirc = self.convert_X_to_quantum(self.m_data.x_train, self.m_data.x_test, self.m_data.x_val)

        num_var = len(self.m_data.x_train[0])
        logging.info(f'Number of variables: {num_var}')

        try:
            QNN = importlib.import_module(f'quhep.tfq_net.{self.m_Qnetwork}')
        except Exception as e:
            logging.fatal(e)

        qnn = QNN.QuantumNeuralNetwork(nqubits = self.m_nqubits, use_quple = self.m_use_quple, nlayers = self.m_nlayers, ndepths = self.m_ndepths, loss=self.m_loss)
        quantum_model = qnn.get_quantum_model(self.m_nqubits)

        logging.info(f'Train quantum model: epochs: {self.m_epochs}; batch size: {self.m_batch_size}; number of training events (sig + bkg): {x_train_tfcirc.shape[0]}')

        callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        # print_weights = tf.keras.callbacks.LambdaCallback(on_epoch_end=lambda batch, logs: print(quantum_model.layers[-1].get_weights()))
        qnn_history = quantum_model.fit(
            x_train_tfcirc, self.m_data.y_train,
            batch_size=self.m_batch_size,
            epochs=self.m_epochs,
            verbose=1,
            validation_data=(x_val_tfcirc, self.m_data.y_val),
            callbacks=[callback])
        logging.info(f'Total number of QNN epochs: {len(qnn_history.history["loss"])}')

        # quantum_model.save('m.h5')
        logging.info(f'Cannot save quantum model due to a bug in TF: NotImplementedError: Layers with arguments in `__init__` must override `get_config`.')

        with open(f'{self.m_log_dir["result"]}/qnn_history.txt', 'w') as f:
            f.write( str(qnn_history.history) )

        if qnn_history is None:
            with open(f'{self.m_log_dir["result"]}/qnn_history.txt', 'r') as f:
                qnn_history = eval(r.read())

        self.plotLoss(qnn_history, 'QNN')
        qnn_results = quantum_model.evaluate(x_train_tfcirc, self.m_data.y_train)
        logging.info(f'Evaluation of quantum model on train sample: {qnn_results}')
        qnn_results = quantum_model.evaluate(x_val_tfcirc, self.m_data.y_val)
        logging.info(f'Evaluation of quantum model on val sample: {qnn_results}')
        qnn_results = quantum_model.evaluate(x_test_tfcirc, self.m_data.y_test)
        logging.info(f'Evaluation of quantum model on test sample: {qnn_results}')

        self.m_train_predict_QNN = quantum_model.predict(x_train_tfcirc)
        self.m_test_predict_QNN = quantum_model.predict(x_test_tfcirc)
        self.m_val_predict_QNN = quantum_model.predict(x_val_tfcirc)


    def train_classical_model(self):
        num_var = len(self.m_data.x_train[0])
        try:
            DNN = importlib.import_module('quhep.tfq_net.ClassicalNN')
        except Exception as e:
            logging.fatal(e)

        classical_model = DNN.get_classicial_model(num_var)

        logging.info(f'Train classical model: epochs: {self.m_epochs}; batch size: {self.m_batch_size}; number of training events (sig + bkg): {self.m_data.x_train.shape[0]}')
        callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        cnn_history = classical_model.fit(self.m_data.x_train,
                self.m_data.y_train,
                batch_size=self.m_batch_size,
                epochs=self.m_epochs,
                verbose=1,
                validation_data=(self.m_data.x_val, self.m_data.y_val),
                callbacks=[callback])
        classical_model.summary(print_fn=logging.getLogger(__name__).info)
        logging.info(f'Total number of DNN epochs: {len(cnn_history.history["loss"])}')

        classical_model.save(f'{self.m_log_dir["model"]}/classical_model.h5')
        logging.info(f'Save classical model to: {self.m_log_dir["model"]}/classical_model.h5')
        
        with open(f'{self.m_log_dir["result"]}/cnn_history.txt', 'w') as f:
            f.write( str(cnn_history.history) )

        if cnn_history is None:
            with open(f'{self.m_log_dir["result"]}/cnn_history.txt', 'r') as f:
                cnn_history = eval(r.read())

        self.plotLoss(cnn_history, 'DNN')
        cnn_results = classical_model.evaluate(self.m_data.x_test, self.m_data.y_test)
        logging.info(f'Evaluation of classical model on test sample: {cnn_results}')

        self.m_train_predict_DNN = classical_model.predict(self.m_data.x_train)
        self.m_test_predict_DNN = classical_model.predict(self.m_data.x_test)
        self.m_val_predict_DNN = classical_model.predict(self.m_data.x_val)

def main():
    args = add_options()
    print('zhangr', args.skip_quantum)
    if args.fix_seed:
        import numpy as np
        np.random.seed(args.fix_seed + 666)

    trainer = Train(**vars(args))
    trainer.get_classical_data()

    if not args.skip_quantum:
        trainer.train_quantum_model()
    if args.run_classical:
        trainer.train_classical_model()
        trainer.plotROC()
    trainer.plotROC(True)
    logging.info(f'Job finished')


if __name__ == '__main__':
    main()
