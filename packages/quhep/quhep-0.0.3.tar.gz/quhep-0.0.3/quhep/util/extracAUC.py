#!/usr/bin/env python
# Rui Zhang 7.2020
# rui.zhang@cern.ch

import os
import re
from argparse import ArgumentParser
import glob
from math import ceil

import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
plt.rcParams["figure.figsize"] = (15,10)
import seaborn as sns
import datetime

process_map = {
    'hmumu': r'$H  \rightarrow \mu \mu$',
    'ttH': r'$t\bar{t}H$',
}
Encoder_map = {
    'FirstOrderExpansion': '1st-Order',
    'SecondOrderExpansion': '2nd-Order',
}

def extractJobFeatures(sub_folders):
    group_folders = {}
    for sub_folder in sub_folders:
        names = sub_folder.split('-')
        bs = [name for name in names if name.startswith('bs')][0][2:]
        qu = [name for name in names if name.startswith('qu')][0][2:]
        lpca = [name for name in names if name.startswith('lpca')][0][4:]
        train = [name for name in names if name.startswith('train')][0][5:]
        encode = [name for name in names if name.startswith('enc')][0][3:]
        depths = [name for name in names if name.startswith('Dep')][0][3:]
        QNNname = [name for name in names if name.startswith('QNN')][0][3:]
        layers = [name for name in names if name.startswith('L')][0][1:]
        loss = [name for name in names if name.startswith('l')][1][1:]
        group_name = f'{bs}-{qu}-{lpca}-{train}-{encode}-{depths}-{QNNname}-{layers}-{loss}'
        if group_name in group_folders:
            group_folders[group_name].append(sub_folder)
        else:
            group_folders[group_name] = [sub_folder]

    pprint(group_folders)
    print('\n\n')
    return group_folders

def extractAUCvalues(group_folders, catagories, skip=True):
    rows_list = []
    
    keywords = '{} {} AUC values'
    for jobfeature in sorted(group_folders):
        folders = group_folders[jobfeature]
        jobfeature = jobfeature.split('-')
        for folder in folders:
            logfile = glob.glob(f'{folder}/*log')[0]
            if skip and os.stat(logfile).st_size == 0:
                print(f'\n\033[91mNo log in: {logfile}\033[0m')
                continue
            with open(logfile) as f:
                for (i, j) in catagories:
                    dic = {
                        'batchsize': int(jobfeature[0]),
                        'Nqubits': int(jobfeature[1]),
                        'Ntrain': int(jobfeature[2]),
                        'encoder': str(Encoder_map[jobfeature[3]]),
                        'Ndepths': int(jobfeature[4]),
                        'QNNname': str(jobfeature[5]),
                        'Nlayers': int(jobfeature[6]),
                        'Events': None,
                        'AUC':  0,
                        'TimeEncode': 0,
                        'TimeTrain': 0,
                    }
                    # fill AUC value to dic
                    dic['Events'] = f'{j} {i}'
                    try:
                        f.seek(0)
                        dic['AUC'] = float(([line for line in f if keywords.format(i, j) in line][0]).split(' ')[12])

                        f.seek(0)
                        startencoding = datetime.datetime.strptime(([line for line in f if 'Start data encoding' in line][0]).split(',')[0], '%Y-%m-%d %H:%M:%S')
                        f.seek(0)
                        stopencoding = datetime.datetime.strptime(([line for line in f if 'Finish data encoding' in line][0]).split(',')[0], '%Y-%m-%d %H:%M:%S')
                        dic['TimeEncode'] = int((stopencoding-startencoding).total_seconds())

                        f.seek(0)
                        starttraining = datetime.datetime.strptime(([line for line in f if 'Train quantum model' in line][0]).split(',')[0], '%Y-%m-%d %H:%M:%S')
                        f.seek(0)
                        stoptraining = datetime.datetime.strptime(([line for line in f if 'Evaluation of quantum model' in line][0]).split(',')[0], '%Y-%m-%d %H:%M:%S')
                        dic['TimeTrain'] = int((stoptraining-starttraining).total_seconds())
                    except:
                        print(f'\n\033[91mNo AUC for {keywords.format(i, j)} in: {logfile}\033[0m')
                    rows_list.append(dic)
    df = pd.DataFrame(rows_list)
    return df

def main(args):
    input_folder = args.input_folder
    catagory = args.catagory
    catagories = [(i, j) for j in ['QNN', 'DNN'] for i in catagory]
    print(catagories)
    color = 'RdBu'
    sns.set_style('whitegrid')

    for j, top_folder in enumerate(input_folder):
        # extract physics process from top level folder
        process = [name for name in process_map.keys() if name in top_folder][0]
        print(f'\n\033[92mPhysics process: {process} ({process_map[process]})\033[0m')

        # extract all jobs
        sub_folders = glob.glob(f'{top_folder}/2020*')

        # extract job features
        group_folders = extractJobFeatures(sub_folders)

        # extract AUC values to a dataframe
        df = extractAUCvalues(group_folders, catagories)
        xTitle, yTitle, lTitle = 'Architecture', 'AUC', 'Events'
        df[xTitle] = df['encoder'] + ' ' + df['Ndepths'].apply(str) + '-Dep' + '\n' + df['QNNname'] + ' ' + df['Nlayers'].apply(str) + '-Layer'

        # get a list of names
        values=df['Ntrain'].unique().tolist()

        # create different plots for different Ntrain
        for value in values:
            sub_df = df.loc[df['Ntrain']==value]

            # calculate averaged timing
            timedf = sub_df.groupby(xTitle, as_index=False)[['TimeEncode', 'TimeTrain']].mean().set_index(xTitle)
            for i in sub_df.index:
                sub_df.at[i, xTitle] = sub_df.at[i, xTitle] + '\n(' + str(datetime.timedelta(seconds=ceil(timedf.loc[sub_df.at[i, xTitle], 'TimeEncode']))) + ')\n(' + str(datetime.timedelta(seconds=ceil(timedf.loc[sub_df.at[i, xTitle], 'TimeTrain']))) + ')'
            print(f'Ntrain {value}:')
            print(sub_df)

            fig, ax = plt.subplots(tight_layout=True)
            plt.title(f'{process_map[process]} ({value} sig {value} bkg training Events, {sub_df["Nqubits"].iloc[0]} Qubits)')
            chart = sns.boxplot(x=xTitle, y=yTitle, hue=lTitle, data=sub_df, palette=color, fliersize=0)
            chart.set_xticklabels(chart.get_xticklabels(), rotation=60)
            # jitter plot overlay
            sns.stripplot(x=xTitle, y=yTitle, hue=lTitle, data=sub_df, jitter=True, palette=color, alpha=0.8, dodge=True, linewidth=1, edgecolor='gray')
            handles, labels = ax.get_legend_handles_labels()
            plt.legend(handles[0:int(len(handles)/2)], labels[0:int(len(handles)/2)], framealpha=0.5)
            plt.ylim(0.4, 0.9)

            filename = f'{top_folder}/{yTitle}_{value}Events_{"".join(catagory)}_{process}.pdf'
            plt.savefig(filename)
            print(f'\n\033[92mSave file: {filename}\033[0m')


if __name__ == '__main__':

    """Get arguments from command line."""
    parser = ArgumentParser(description="Plot AUC information.")

    parser.add_argument('-i', '--input-folder', action='store', nargs='+', default=[], help='Folder of the log files (default: %(default)s)')
    parser.add_argument('-c', '--catagory', action='store', nargs='+', default=['Test'], help='Events to plot (default: %(default)s)')
    
    main(parser.parse_args())
