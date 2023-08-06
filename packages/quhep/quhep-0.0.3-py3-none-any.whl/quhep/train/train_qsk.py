#!/usr/bin/env python
# Rui Zhang 8.2020
# rui.zhang@cern.ch

import logging
import numpy as np
import matplotlib.pyplot as plt
import importlib

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms
import torch.optim as optim
import torch.nn as nn
# from torchviz import make_dot
from torchsummary import summary
import qiskit
from qiskit.visualization import circuit_drawer

from quhep.train.train import _train, add_options


# https://discuss.pytorch.org/t/input-numpy-ndarray-instead-of-images-in-a-cnn/18797/2
class MyDataset(Dataset):
    ''' Transform numpy array to pyTorch Dataset '''
    def __init__(self, data, target, transform=None):
        self.data = torch.from_numpy(data).float()
        self.target = torch.from_numpy(target).long()
        self.transform = transform
        
    def __getitem__(self, index):
        x = self.data[index]
        y = self.target[index]
        
        if self.transform:
            x = self.transform(x)
        
        return x, y

    def __len__(self):
        return len(self.data)


class Train(_train):
    def describe(self): return self.__class__.__name__
    def __init__(self, **kargs):
        self.m_use_quple = kargs['use_quple']
        self.m_nlayers = kargs['nlayers']
        self.m_ndepths = kargs['ndepths']
        self.m_encoder_type = kargs['encoder_type']
        self.m_Qnetwork = kargs['Qnetwork']
        self.m_loss = kargs['loss']
        quple_par = f'use_qsk-enc{self.m_encoder_type}-Dep{self.m_ndepths}-QNN{self.m_Qnetwork}-L{self.m_nlayers}-l{self.m_loss}'
        super().__init__(additional_log=quple_par, **kargs)

        self.m_scale_range = (0, 1)

    def train_quantum_model(self):
        dataset_train = MyDataset(self.m_data.x_train, self.m_data.y_train)
        dataset_test = MyDataset(self.m_data.x_test, self.m_data.y_test)
        dataset_val = MyDataset(self.m_data.x_val, self.m_data.y_val)
        loader_train = DataLoader(dataset_train, batch_size = self.m_batch_size, shuffle = False, num_workers = 0, pin_memory = torch.cuda.is_available())
        loader_test = DataLoader(dataset_test, batch_size = self.m_batch_size, shuffle = False, num_workers = 0, pin_memory = torch.cuda.is_available())

        module = importlib.import_module(f'quhep.qsk_circ.QuantumCircuit')
        model = module.Net(self.m_nqubits)
        # model.hybrid.plot_circuit(f'{self.m_log_dir["model"]}/circuit') #TODO
        # summary(model, input_size=(self.m_nqubits, 1))
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        loss_func = nn.NLLLoss()

        loss_list = []

        model.train()
        for epoch in range(self.m_epochs):
            total_loss = []
            for batch_idx, (data, target) in enumerate(loader_train):
                optimizer.zero_grad()
                # Forward pass
                output = model(data)
                # Calculating loss
                loss = loss_func(output, target)
                # Backward pass
                loss.backward()
                # Optimize the weights
                optimizer.step()
                
                total_loss.append(loss.item())
            loss_list.append(sum(total_loss)/len(total_loss))
            print('Training [{:.0f}%]\tLoss: {:.4f}'.format(100. * (epoch + 1) / self.m_epochs, loss_list[-1]))

        plt.plot(loss_list)
        plt.title('Hybrid NN Training Convergence')
        plt.xlabel('Training Iterations')
        plt.ylabel('Neg Log Likelihood Loss')


        model.eval()
        with torch.no_grad():
            correct = 0
            for batch_idx, (data, target) in enumerate(loader_test):
                output = model(data)
            
                pred = output.argmax(dim=1, keepdim=True) 
                correct += pred.eq(target.view_as(pred)).sum().item()
            
                loss = loss_func(output, target)
                total_loss.append(loss.item())
            
            print('Performance on test data:\n\tLoss: {:.4f}\n\tAccuracy: {:.1f}%'.format(sum(total_loss) / len(total_loss), correct / len(loader_test) * 100))


def main():
    args = add_options()
    if args.fix_seed:
        import numpy as np
        np.random.seed(args.fix_seed + 666)

    trainer = Train(**vars(args))
    trainer.get_classical_data()

    trainer.train_quantum_model()
    if args.run_classical:
        trainer.train_classical_model()
        trainer.plotROC()
    trainer.plotROC(True)
    logging.info(f'Job finished')


if __name__ == '__main__':
    main()
