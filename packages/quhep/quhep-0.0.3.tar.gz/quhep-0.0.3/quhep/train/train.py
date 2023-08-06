#!/usr/bin/env python
# Rui Zhang 8.2020
# rui.zhang@cern.ch

import logging
import os
import numpy as np
from argparse import ArgumentParser

from datetime import datetime
import collections
import json, pickle
from importlib import reload
import importlib

from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

class AutoVivification(dict):
    '''Implementation of perl's autovivification feature.'''
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class _train(object):
    def describe(self): return self.__class__.__name__
    def __init__(self, **kargs):
        self.m_input_file = kargs['input_file']
        self.m_output_folder = kargs['output_folder']
        self.m_log_file = kargs['log_file']
        self.m_training_size = kargs['training_size']
        self.m_test_size = kargs['test_size']
        self.m_val_size = kargs['val_size']
        self.m_nqubits = kargs['nqubits']
        self.m_epochs = kargs['epochs']
        self.m_batch_size = kargs['batch_size']
        self.m_fix_seed = kargs['fix_seed']
        self.m_test_predict_QNN = None
        self.m_test_predict_DNN = None
        self.m_train_predict_QNN = None
        self.m_train_predict_DNN = None
        self.m_val_predict_QNN = None
        self.m_val_predict_DNN = None
        self.padding = kargs['padding']
        self.m_plot_input = kargs['plot_input']
        self.m_plot_input_only = kargs['plot_input_only']
        self.m_reducer = 'PCA'
        self.m_loss = kargs['loss']
        self.m_large_pca = kargs['large_pca']
        self.m_entangle = kargs['entangle']
        self.m_entangle_gate = kargs['entangle_gate']
        self.m_additional_log = kargs['additional_log']
        self.m_encoding = kargs['encoding']

        
        self.m_log_dir = {}
        self.m_log_dir['base'] = os.path.join(self.m_output_folder, 'logs_' + self.m_log_file, f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}-{self.m_fix_seed}-{os.uname()[1]}-bs{self.m_batch_size}-qu{self.m_nqubits}-lpca{self.m_large_pca}-train{self.m_training_size}-red{self.m_reducer}-entgate{self.m_entangle_gate}-ent{self.m_entangle}-{self.m_additional_log}')
        if self.m_plot_input or self.m_plot_input_only:
            self.m_log_dir['input'] = os.path.join(self.m_log_dir['base'], 'input')
        if not self.m_plot_input_only:
            self.m_log_dir['result'] = os.path.join(self.m_log_dir['base'], 'result')
        self.m_log_dir['model'] = os.path.join(self.m_log_dir['base'], 'model')

        for folder in self.m_log_dir.values():
            if not os.path.exists(folder):
                os.makedirs(folder)

        logging.info(f'Logger folder is: {self.m_log_dir["base"]}')
        self.config_logging()
        logging.info(f'Train option {vars(self)}')

        if self.m_encoding == 'rotation':
            self.m_scale_range = (-1, 1)
        elif self.m_encoding == 'prob':
            self.m_scale_range = (0, 1)
        
    def config_logging(self):
        log_filename = f'train{self.m_training_size}_val{self.m_val_size}_test{self.m_test_size}_bs{self.m_batch_size}.log'
        self.m_log_filename = os.path.join(self.m_log_dir["base"], log_filename)

        reload(logging)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.FileHandler("{0}".format(self.m_log_filename)),
                logging.StreamHandler()
            ])

    def plot_input(self, training_signal, training_backgd, test_signal = None, test_backgd = None, column = 0, name = 'var', norm = False):
        _, nbins, _ = plt.hist(training_signal[:, column], histtype='step', bins = 100, linewidth=2, alpha=0.9, label='Train Signal', density=norm)
        plt.hist(training_backgd[:, column], histtype='step', bins = nbins, linewidth=2, alpha=0.9, label='Train Backgd', density=norm)
        if test_signal is not None and test_signal.shape[0]: plt.hist(test_signal[:, column], histtype='step', bins = nbins, linewidth=2, alpha=0.9, label='Test Signal', linestyle = 'dashed')
        if test_backgd is not None and test_backgd.shape[0]: plt.hist(test_backgd[:, column], histtype='step', bins = nbins, linewidth=2, alpha=0.9, label='Test Backgd', linestyle = 'dashed')

        plt.ylabel('Events')
        plt.xlabel(name)
        plt.legend(loc='best')
        plt.tight_layout(pad=0)
        plt.savefig(f'{self.m_log_dir["input"]}/{name}.pdf')
        logging.debug(f'Save column {column} to {self.m_log_dir["input"]}/{name}.pdf')
        plt.clf()

    def load_npz_data(self):
        '''
        load npz data

        :Returns:
            training_input, test_input, each of which is a dictionary.
            keys = 'A', 'B'
            values = nEvent x nVariable
        ''' 
        data = np.load(self.m_input_file, allow_pickle=True)
        if isinstance(data, np.lib.npyio.NpzFile):
            training_input = {'input':v for k,v in np.ndenumerate(data['training_input'])}['input']
            test_input = {'input':v for k,v in np.ndenumerate(data['test_input'])}['input']
            if self.m_training_size:
                training_input = {key: training_input[key][:self.m_training_size] for key in training_input.keys()}
            if self.m_test_size:
                test_input = {key: test_input[key][:self.m_test_size] for key in test_input.keys()}
            val_input = None
        elif isinstance(data, np.ndarray):
            if self.padding != -999:
                data[data == -999] = self.padding
                logging.info(f'Change padding to {self.padding} from default -999.')

            signal_array = data[data[:, -1] > 0.5][:, :-1]
            backgd_array = data[data[:, -1] < 0.5][:, :-1]
            np.random.shuffle(signal_array)
            np.random.shuffle(backgd_array)

            # If not specified, 1/2 training, 1/4 for val and 1/4 for test
            if not self.m_training_size and not self.m_test_size and not self.m_val_size:
                self.m_training_size = int(signal_array.shape[0] / 2)
                self.m_test_size = int(signal_array.shape[0] / 4)
                self.m_val_size = self.m_test_size
            # If training specified, 1/2 for val and 1/2 for test
            elif self.m_training_size and not self.m_test_size and not self.m_val_size:
                self.m_test_size = int((signal_array.shape[0] - self.m_training_size) / 2)
                self.m_val_size = self.m_test_size
            # If training & test specified, val = min(rest, test)
            elif self.m_training_size and self.m_test_size and not self.m_val_size:
                self.m_val_size = min([m_test_size, signal_array.shape[0] - self.m_training_size - self.m_val_size])
            # If training & val specified, test = rest
            elif self.m_training_size and not self.m_test_size and self.m_val_size:
                self.m_test_size = signal_array.shape[0] - self.m_training_size - self.m_val_size
            elif self.m_training_size and self.m_val_size and self.m_test_size:
                pass
            else:
                logging.fatal(f'Request of training size {self.m_training_size}, test size {self.m_test_size} and val size {self.m_val_size} from {len(signal_array)} signal or {len(backgd_array)} bkg events do NOT make sense.')
                assert(False)
            if self.m_training_size + self.m_test_size + self.m_val_size > signal_array.shape[0]:
                logging.fatal(f'Request of training size {self.m_training_size}, test size {self.m_test_size} and val size {self.m_val_size} from {len(signal_array)} signal or {len(backgd_array)} bkg events do NOT make sense.')
                assert(False)

            logging.info(f'Request of training size {self.m_training_size}, test size {self.m_test_size} and val size {self.m_val_size} from {len(signal_array)} signal or {len(backgd_array)} bkg events make sense.')
            training_input, test_input, val_input = {}, {}, {}
            pca_input = {}
            training_input['1'], training_input['0'] = signal_array[:self.m_training_size], backgd_array[:self.m_training_size]
            test_input['1'], test_input['0'] = signal_array[self.m_training_size:self.m_training_size+self.m_test_size], backgd_array[self.m_training_size:self.m_training_size+self.m_test_size]
            if self.m_val_size == 0:
                val_input = None
            else:
                val_input['1'], val_input['0'] = signal_array[self.m_training_size+self.m_test_size:self.m_training_size+self.m_test_size+self.m_val_size], backgd_array[self.m_training_size+self.m_test_size:self.m_training_size+self.m_test_size+self.m_val_size]
            pca_input['1'], pca_input['0'] = signal_array, backgd_array
        
        name = 'BeforeDimRed_{}'
        if self.m_plot_input:
            for column in range(training_input['0'].shape[1]):
                self.plot_input(training_input['1'], training_input['0'], test_input['1'], test_input['0'], column = column, name = name.format(str(column)))
            logging.info(f'Save {training_input["0"].shape[1]} input columns to {name.format("*")}.pdf')
        elif self.m_plot_input_only:
            for column in range(training_input['0'].shape[1]):
                self.plot_input(signal_array, backgd_array, column = column, name = name.format(str(column)), norm = True)
            logging.info(f'Save {training_input["0"].shape[1]} input columns to {name.format("*")}.pdf')
        else:
            logging.info(f'Save not {training_input["0"].shape[1]} input columns to {name.format("*")}.pdf')

        logging.info(f'Signal: {training_input["1"][:3]}')
        logging.info(f'Backgd: {training_input["0"][:3]}')

        return training_input, test_input, val_input, pca_input

    def process_npz_data(self, dictAB, training=False):
        '''
        Process dictionary from npz file:
            - merge and shuffle training data in two classes
            - MinMax scale X
        '''
        target = {'1': 1, '0': -1} if self.m_loss == 'hinge' else {'1': 1, '0': 0} # 1=signal; 0=backgd
        X = np.concatenate((dictAB['0'], dictAB['1']), axis=0)
        y = np.array([target['0']]*dictAB['0'].shape[0] + [target['1']]*dictAB['0'].shape[0])

        dimension = self.m_nqubits + self.m_entangle
        if self.m_nqubits <= X[0].shape[0]:
            ''' Do Dimension Reduction '''
            reducer_file = f'{self.m_log_dir["model"]}/reducer_{self.m_reducer}.pkl'
            if training:
                ''' Perform Dimension Reduction '''
                module = importlib.import_module(f'sklearn.decomposition')
                reducer = module.PCA(n_components=dimension).fit(X)
                X = reducer.transform(X)
                pickle.dump(reducer, open(reducer_file, 'wb'))
                logging.info(f'Write reducer to: {reducer_file}, with dimension {dimension}, X shape is {X.shape}')
            else:
                ''' Apply Dimension Reduction '''
                reducer = pickle.load(open(reducer_file,'rb'))
                X = reducer.transform(X)
            ''' Plot input '''
            name = 'AfterDimRed_' + self.m_reducer + '_{}_' + ('training' if training else 'test')
            if self.m_plot_input or self.m_plot_input_only:
                for column in range(X.shape[1]):
                    self.plot_input(X[y == target['1']], X[y == target['0']], column = column, name = name.format(str(column)))
                logging.info(f'Save {X.shape[1]} input columns to {name.format("*")}.pdf')
            else:
                logging.info(f'Save not {X.shape[1]} input columns to {name.format("*")}.pdf')

        elif self.m_nqubits == X[0].shape[0]:
            ''' No Dimension Reduction '''
            logging.info(f'No Dimension Reduction needed as dimension {self.m_nqubits} is same as input.')
        else:
            logging.fatal(f'Request of Dimension Reduction dimension {self.m_nqubits} is greater than input dimension {X[0].shape[0]}.')

        scaler_file = f'{self.m_log_dir["model"]}/scaler.pkl'
        X, y = shuffle(X, y)
        if training:
            scaler = MinMaxScaler(feature_range=(self.m_scale_range))
            scaler.fit_transform(X, y)
            X = scaler.transform(X)
            pickle.dump(scaler, open(scaler_file, 'wb'))
            logging.info(f'Write scalar to: {scaler_file} with range {self.m_scale_range}')
        else:
            scaler = pickle.load(open(scaler_file, 'rb'))
            logging.info(f'Load scalar from: {scaler_file}')
            X = scaler.transform(X)

        if self.m_encoding == 'prob':
            X = 2*np.arccos(np.sqrt(X))

        name = 'AfterTransf_{}' + ('_training' if training else '_test')
        if self.m_plot_input or self.m_plot_input_only:
            from matplotlib.colors import LogNorm
            Z = np.corrcoef(X.T)
            np.fill_diagonal(Z, 0)
            logging.info(f'Highest correlation happens in {Z.argmax(axis=0)}')
            plt.matshow(Z, norm=LogNorm())
            plt.colorbar()
            plt.savefig(f'{self.m_log_dir["input"]}/correlation.pdf')
            logging.info(f'Save correlation to {self.m_log_dir["input"]}/correlation.pdf')
            plt.clf()
            for column in range(X.shape[1]):
                self.plot_input(X[y == target['1']], X[y == target['0']], column = column, name = name.format(str(column)))
            logging.info(f'Save {X.shape[1]} input columns to {name.format("*")}.pdf')
            if self.m_plot_input_only:
                exit(0)
        else:
            logging.info(f'Save not {X.shape[1]} input columns to {name.format("*")}.pdf')

        return X, y

    def get_classical_data(self):
        training_input, test_input, val_input, pca_input = self.load_npz_data()
        if self.m_large_pca:
            _, _ = self.process_npz_data(pca_input, training = True)
            x_train, y_train = self.process_npz_data(training_input)
        else:
            x_train, y_train = self.process_npz_data(training_input, training = True)
        x_test, y_test = self.process_npz_data(test_input)
        x_val, y_val = self.process_npz_data(val_input) if val_input else (x_test, y_test)

        logging.info(f'Training size: {len(x_train)}, target: {y_train[:10]}...')
        logging.info(f'Testing size: {len(x_test)}, target: {y_test[:10]}...')

        self.m_data = collections.namedtuple('data', ['x_train', 'y_train', 'x_test', 'y_test', 'x_val', 'y_val'])(x_train, y_train, x_test, y_test, x_val, y_val)


    def plotLoss(self, history, title):
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title(title)
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend(['train', 'val'], loc='upper right')
        plt.savefig(f'{self.m_log_dir["result"]}/loss_{title}.pdf', format='pdf')
        plt.clf()

    def getAUC(self, y_test, weight, score):
        fpr, tpr, _ = roc_curve(y_test, score, sample_weight=weight)
        roc_auc = auc(fpr, tpr)
        return fpr, tpr, roc_auc

    def plotROC(self, excludeDNN=False):
        plt.figure()
        plt.grid(color='gray', linestyle='--', linewidth=1)
        
        curves = []
        Curve = collections.namedtuple('Curve', ['y', 'predict', 'NNtype', 'Traintype', 'Linestyle'])
        if self.m_test_predict_QNN is not None:  curves.append(Curve(y=self.m_data.y_test, predict=self.m_test_predict_QNN, NNtype='QNN', Traintype='Test', Linestyle='solid'))
        if self.m_train_predict_QNN is not None: curves.append(Curve(y=self.m_data.y_train, predict=self.m_train_predict_QNN, NNtype='QNN', Traintype='Train', Linestyle='dashed'))
        if self.m_val_predict_QNN is not None: curves.append(Curve(y=self.m_data.y_val, predict=self.m_val_predict_QNN, NNtype='QNN', Traintype='Val', Linestyle='dashed'))
        
        if not excludeDNN:
            if self.m_test_predict_DNN is not None:  curves.append(Curve(y=self.m_data.y_test, predict=self.m_test_predict_DNN, NNtype='DNN', Traintype='Test', Linestyle='solid'))
            if self.m_train_predict_DNN is not None: curves.append(Curve(y=self.m_data.y_train, predict=self.m_train_predict_DNN, NNtype='DNN', Traintype='Train', Linestyle='dashed'))
            if self.m_val_predict_DNN is not None: curves.append(Curve(y=self.m_data.y_val, predict=self.m_val_predict_DNN, NNtype='DNN', Traintype='Val', Linestyle='dashed'))

        logging.info(f'ROC curves: {len(curves)}.')

        roc_curves_to_save = AutoVivification()
        for curve in curves:
            fpr_test, tpr_test, roc_auc_test = self.getAUC(curve.y, None, curve.predict)
            roc_curves_to_save[curve.NNtype][curve.Traintype] = (fpr_test.tolist(), tpr_test.tolist(), roc_auc_test.tolist())
            fpr_test = 1.0 - fpr_test
            plt.plot(tpr_test, fpr_test, label=f'{curve.Traintype} {curve.NNtype} AUC: {roc_auc_test: 0.3f}', linestyle=curve.Linestyle)
            logging.info(f'{curve.Traintype} {curve.NNtype} AUC values: {roc_auc_test} from {len(curves)} curves.')
        
        with open(f'{self.m_log_dir["result"]}/roc{len(curves)}_train{len(self.m_data.y_train)}_val{len(self.m_data.y_val)}_test{len(self.m_data.y_test)}.json', 'w') as f:
            json.dump(roc_curves_to_save, f)

        plt.plot([0, 1], [1, 0], linestyle='--', color='black', label='Luck')
        plt.xlim([-0.,1.])
        plt.ylim([-0.,1.])
        plt.xlabel('Signal acceptance')
        plt.ylabel('Background rejection')
        plt.legend(loc='lower left')
        roc_file = f'{self.m_log_dir["result"]}/roc{len(curves)}_train{len(self.m_data.y_train)}_val{len(self.m_data.y_val)}_test{len(self.m_data.y_test)}.pdf'
        plt.savefig(roc_file, format='pdf')
        plt.clf()

def add_options():
    """Get arguments from command line."""
    parser = ArgumentParser(description="Tensorflow Quantum model training.")

    parser.add_argument('--batch-size', action='store', type=int, default=10, help='Training batch size type (default: %(default)s)')
    parser.add_argument('--run-classical', action='store_true', default=False, help='Train classical NN (default: %(default)s)')
    parser.add_argument('--entangle', action='store', type=int, default=0, help='Additinal dimension used for entanglement encoder (default: %(default)s)')
    parser.add_argument('--entangle-gate', action='store', type=str, default='rx', choices=['rx', 'ry', 'rx4', 'ry4', 'rx7', 'ry7', 'rx6r', 'ry6r', 'rx9r', 'ry9r', 'rx1r', 'ry1r'], help='Additinal dimension used for entanglement encoder (default: %(default)s)')
    parser.add_argument('--encoding', action='store', type=str, default='rotation', choices=['rotation', 'prob'], help='Type of encoding (default: %(default)s)')
    parser.add_argument('--epochs', action='store', type=int, default=200, help='Training epochs (default: %(default)s)')
    parser.add_argument('--fix-seed', action='store', type=int, default=None, help='Fix random seed (default: %(default)s)')
    parser.add_argument('-i', '--input-file', action='store', default='data/qml/hmumu_twojet_0719.npy', help='Input data (.npz) (default: %(default)s)')
    parser.add_argument('--large-pca', action='store_true', default=True, help='Use more events for PCA (default: %(default)s)')
    parser.add_argument('--log-file', action='store', default='QNN', help='Directory name to store logs (default: %(default)s)')
    parser.add_argument('--loss', action='store', default='hinge', help='Loss for QEfficientSU2NNHYB (default: %(default)s)')
    parser.add_argument('--nqubits', action='store', type=int, default=None, required=True, help='Number of qubits / varibles (default: %(default)s)')
    parser.add_argument('--output-folder', action='store', default='../output', help='Output folder for logs (default: %(default)s)')
    parser.add_argument('--padding', action='store', type=float, choices=[-999, 0], default=-999, help='Padding of non-existing (default: %(default)s)')
    parser.add_argument('--plot-input', action='store_true', default=False, help='Plotting before and after Dimension Reduction (default: %(default)s)')
    parser.add_argument('--plot-input-only', action='store_true', default=False, help='Inspect inputs (default: %(default)s)')
    parser.add_argument('--skip-quantum', action='store_true', default=False, help='Skip Quantum NN (default: %(default)s)')
    parser.add_argument('--training-size', action='store', type=int, default=50, help='Number of events for training (default: %(default)s)')
    parser.add_argument('--test-size', action='store', type=int, default=None, help='Number of events for test (default: %(default)s)')
    parser.add_argument('--val-size', action='store', type=int, default=50, help='Number of events for val (default: %(default)s)')
    parser.add_argument('--Qnetwork', type=str, choices=['QDensNN', 'QConvNN', 'QConvNNHYB', 'QZinnerCNOTNN', 'QZinnerCNOTNNHYB', 'QEfficientSU2NNHYB', 'QEfficientSU2NNHYB2', 'QEfficientSU2NNQNN', 'QMNISTNN'], help='Quantum network type (default: %(default)s)')
    
    subparsers = parser.add_subparsers(dest='use_quple', help='Use quple encoder')
    parser_quple = subparsers.add_parser('use_quple')
    parser_quple.add_argument('--encoder-type', type=str, default=None, choices=['FirstOrderExpansion', 'SecondOrderExpansion'], help='Data encoder depths (default: %(default)s)')
    parser_quple.add_argument('--ndepths', type=int, default=1, help='Data encoder depths (default: %(default)s)')
    parser_quple.add_argument('--nlayers', type=int, default=1, help='Number of layers for quantum model (default: %(default)s)')

    args = parser.parse_args()
    options = vars(args)
    logging.info(f'Argument option {options}')
    return args
