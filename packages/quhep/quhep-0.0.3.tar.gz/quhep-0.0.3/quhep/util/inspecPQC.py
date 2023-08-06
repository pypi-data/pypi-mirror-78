#!/usr/bin/env python
# Rui Zhang 7.2020
# rui.zhang@cern.ch

import os
from argparse import ArgumentParser
import importlib
import numpy as np
from datetime import datetime
import glob

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import seaborn as sns

import quple

# Expressibility (arXiv: 1905.10876)
def calculate(args):
    nqubits = args.nqubits
    PQCnames = args.PQCs
    output = args.output_folder
    repeats = args.repeats
    plotting = args.plotting
    nbins = args.nbins
    statistics = args.statistics

    rows_list = []
    for nqubit in nqubits:
        for PQCname in PQCnames:
            folder = f'{output}/qu{nqubit}/pqc{PQCname}'
            if not os.path.exists(folder):
                os.makedirs(folder)
            for repeat in repeats:
                print('Evaluate', PQCname, repeat)
                if PQCname == 'FirstOrderExpansion':
                    encoder = importlib.import_module(f'quple.data_encoding.first_order_expansion')
                    cq = encoder.FirstOrderExpansion(feature_dimension=nqubit, parameter_symbol='data', depth=repeat)
                elif PQCname == 'SecondOrderExpansion':
                    encoder = importlib.import_module('quple.data_encoding.second_order_expansion')
                    cq = encoder.SecondOrderExpansion(feature_dimension=nqubit, parameter_symbol='data', depth=repeat)
                elif PQCname == 'QConvNN':
                    QNN = importlib.import_module(PQCname)
                    qnn = QNN.QuantumNeuralNetwork(nqubits = nqubit, use_quple = True, nlayers = repeat)
                    qnn.get_quantum_model(nqubit)
                    cq = qnn.m_circuit
                else:
                    QNN = importlib.import_module(PQCname)
                    qnn = QNN.QuantumNeuralNetwork(nqubits = nqubit, use_quple = True, nlayers = repeat)
                    qnn.get_quantum_model(nqubit)
                    cq = qnn.m_circuit
                print(cq)
                for i in range(statistics):
                    dic = {
                        'Nqubits': nqubit,
                        'PQC': PQCname,
                        'Nrepeat': repeat,
                        'absExpressibility':  0,
                        'relExpressibility':  0,
                        'MeyerWallach': 0,
                        'vonNeumann': 0,
                        'GradientVariance': 0,
                    }
                    dic['absExpressibility'] = quple.circuit_expressibility_measure(cq, samples=1000, bins=nbins)
                    dic['relExpressibility'] = -np.log(dic['absExpressibility'] / ((2**nqubit-1)*(np.log(nbins))))
                    dic['MeyerWallach'] = quple.circuit_entangling_measure(cq, samples=500)
                    dic['vonNeumann'] = quple.circuit_von_neumann_entropy(cq, samples=500)
                    if plotting:
                        plt = quple.circuit_fidelity_plot(cq, samples=3000, bins=nbins)
                        name = f'{folder}/fidelity-repeat{repeat}-bin{nbins}-i{i}.pdf'
                        plt.savefig(name)
                        plt.clf()
                        print(f'\n\033[92m{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")} Save fidelity plot: {name}\033[0m')
                    rows_list.append(dic)
                    df = pd.DataFrame(rows_list)
                    rp = '_'.join([str(i) for i in repeats])
                    name = f'{folder}/inspect-repeat{rp}-bin{nbins}-stat{statistics}.csv'
                    df.to_csv(name, index=False)
                    print(f'\n\033[92m{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")} Save inspect dataframe: {name}\033[0m')
    return df


def main(args):
    if not args.load:
        calculate(args)

    else:
        output = args.load
        nqubits = args.nqubits

        xTitle, yTitles, lTitle = 'PQC', ['absExpressibility', 'relExpressibility', 'MeyerWallach', 'vonNeumann'], 'Nrepeat'
        xName, yNames, lName = 'Parameterised Quantum Circuit', ['Expressibility', 'Relative Expressibility', 'Meyer-Wallach Entanglement', 'von Neumann Entanglement'], 'N depths'

        for nqubit in nqubits:
            # extract all jobs
            sub_folders = glob.glob(f'{output}/qu{nqubit}/pqc*/*.csv')

            frames = []
            for sub_folder in sub_folders:
                print(f'\033[92mRead from: {sub_folder}\033[0m')
                pqc = sub_folder.split('/')[-2]
                names = sub_folder.split('/')[-1].split('-')
                nbin = names[-2][3:]
                statistics = names[-1].split('.')[0][4:]
                frames.append(pd.read_csv(sub_folder))
            df = pd.concat(frames)

            sub_df = df.loc[df['Nqubits']==nqubit]
            sub_df = sub_df.sort_values('PQC')

            color = 'RdBu'
            for yTitle, yName in zip(yTitles, yNames):
                fig, ax = plt.subplots(tight_layout=True)
                chart = sns.boxplot(x=xTitle, y=yTitle, hue=lTitle, data=sub_df, palette=color, fliersize=0)
                chart.set_xticklabels(chart.get_xticklabels(), rotation=10)
                # jitter plot overlay
                sns.stripplot(x=xTitle, y=yTitle, hue=lTitle, data=sub_df, jitter=True, palette=color, alpha=0.8, dodge=True, linewidth=1, edgecolor='gray').set(xlabel=xName, ylabel=yName)
                handles, labels = ax.get_legend_handles_labels()
                plt.legend(handles[0:int(len(handles)/2)], labels[0:int(len(handles)/2)], title = lName, framealpha=0.5)

                filename = f'{output}/qu{nqubit}/{yTitle}.pdf'
                plt.savefig(filename)
                print(f'\n\033[92mSave file: {filename}\033[0m')


if __name__ == '__main__':

    """Get arguments from command line."""
    parser = ArgumentParser(description="Evaluate Parametrised Quantum Circuits.")

    parser.add_argument('--load', action='store', default=None, help='Load dataframe file (default: %(default)s)')
    parser.add_argument('--output-folder', action='store', default='../output/inspect', help='Output folder for logs (default: %(default)s)')
    parser.add_argument('--PQCs', nargs='+', type=str, choices=['FirstOrderExpansion', 'SecondOrderExpansion', 'QConvNN', 'QDensNN', 'QZinnerCNOTNN', 'QEfficientSU2NNQNN', 'QMNISTNN'], help='PQC type')
    parser.add_argument('--repeats', nargs='+', type=int, help='Repeating time (default: %(default)s)')
    parser.add_argument('--nbins', type=int, default=500, help='Number of qubits / varibles (default: %(default)s)')
    parser.add_argument('--nqubits', nargs='+', type=int, help='Number of qubits / varibles (default: %(default)s)')
    parser.add_argument('--plotting', action='store_true', default=False, help='Plotting fidelity (default: %(default)s)')
    parser.add_argument('--statistics', type=int, default=10, help='Number evaluation times (default: %(default)s)')

    main(parser.parse_args())
