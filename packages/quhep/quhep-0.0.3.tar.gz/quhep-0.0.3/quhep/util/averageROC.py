#!/usr/bin/env python
# Rui Zhang 8.2020
# rui.zhang@cern.ch

from argparse import ArgumentParser
import glob
import numpy as np
import json

from sklearn.metrics import auc
from sklearn.metrics import plot_roc_curve

import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib
rcParams.update({'figure.autolayout': True})
font = {'size': 22}
matplotlib.rc('font', **font)


def averageROC(top_folder, group_folders, catagories, plot_individual=True, skip=True):
    print('catagories', catagories)
    plt.figure()
    for jobfeature in sorted(group_folders):
        folders = group_folders[jobfeature]
        tprs_x = np.linspace(0, 1, 100)
        fprs_y, aucs = [], []
        Traintype, NNtype = catagories[0]
        plt.grid(color='gray', linestyle='--', linewidth=1, alpha=0.3)
        for i, folder in enumerate(folders):
            logfile = glob.glob(f'{folder}/result/roc*.json')[-1]


            with open(logfile, 'r') as json_file:
                print('read', logfile)
                roc_curves_to_save = json.load(json_file)

            fpr, tpr, roc_auc = roc_curves_to_save[NNtype][Traintype]
            fpr_y, tpr_x, roc_auc = 1.0 - np.array(fpr), np.array(tpr), np.array(roc_auc)
            interp_fpr_y = np.interp(tprs_x, tpr_x, fpr_y)
            interp_fpr_y[0] = 1.0
            fprs_y.append(interp_fpr_y)
            aucs.append(roc_auc)

            if plot_individual:
                plt.plot(tpr_x, fpr_y, alpha=0.5, lw=1, label=f'{Traintype} {NNtype} AUC ({i+1}): {roc_auc: 0.3f}')
            
        mean_fprs_y = np.mean(fprs_y, axis=0)
        mean_fprs_y[-1] = 0.
        mean_auc = auc(tprs_x, mean_fprs_y)
        std_auc = np.std(aucs)

        plt.plot(tprs_x, mean_fprs_y, color='b', label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc), lw=2, alpha=.8)

        std_fprs_y = np.std(fprs_y, axis=0)
        fprs_y_upper = np.minimum(mean_fprs_y + std_fprs_y, 1)
        fprs_y_lower = np.maximum(mean_fprs_y - std_fprs_y, 0)
        plt.fill_between(tprs_x, fprs_y_lower, fprs_y_upper, color='grey', alpha=.2, label=r'$\pm$ 1 std. dev.')

        plt.plot([0, 1], [1, 0], linestyle='--', color='black', label='Luck')
        plt.xlim([-0.05,1.05])
        plt.ylim([-0.05,1.05])
        plt.xlabel('Signal acceptance')
        plt.ylabel('Background rejection')
        plt.legend(loc='lower left')
        roc_file = f'{top_folder}/roc_average_{jobfeature}.pdf'
        print('Save', roc_file)
        plt.savefig(roc_file, format='pdf')
        plt.clf()

from extracAUC import extractJobFeatures
def main(args):
    input_folder = args.input_folder
    catagory = args.catagory
    catagories = [(i, j) for j in ['QNN'] for i in catagory]

    for j, top_folder in enumerate(input_folder):
        # extract all jobs
        sub_folders = glob.glob(f'{top_folder}/2020*')

        # extract job features
        group_folders = extractJobFeatures(sub_folders)
        averageROC(top_folder, group_folders, catagories)


if __name__ == '__main__':

    """Get arguments from command line."""
    parser = ArgumentParser(description="Plot AUC information.")

    parser.add_argument('-i', '--input-folder', action='store', nargs='+', default=[], help='Folder of the log files (default: %(default)s)')
    parser.add_argument('-c', '--catagory', action='store', nargs='+', default=['Test'], help='Events to plot (default: %(default)s)')
    
    main(parser.parse_args())
