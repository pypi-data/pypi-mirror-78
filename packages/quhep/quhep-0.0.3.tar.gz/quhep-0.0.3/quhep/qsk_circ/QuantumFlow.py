#!/usr/bin/env python
# Rui Zhang 8.2020
# rui.zhang@cern.ch

import math
import torch
import torch.nn as nn
from torch.nn.parameter import Parameter
from torch.autograd import Function

class BinarizeF(Function):
    @staticmethod
    def forward(cxt, input):
        output = input.new(input.size())
        output[input >= 0] = 1
        output[input < 0] = -1
        return output
    @staticmethod
    def backward(cxt, grad_output):
        grad_input = grad_output.clone()
        return grad_input

class ClipF(Function):
    @staticmethod
    def forward(ctx, input):
        output = input.clone().detach()
        output[input >= 1] = 1
        output[input <= 0] = 0
        ctx.save_for_backward(input)
        return output

    @staticmethod
    def backward(ctx, grad_output):
        input, = ctx.saved_tensors
        grad_input = grad_output.clone()
        grad_input[input >= 1] = 0
        grad_input[input <= 0] = 0
        return grad_input
class QF_FB_NC(nn.Linear):
    def sim_neural_comp(self, input_ori, w_ori):
        p = input_ori
        d = 4 * p * (1 - p)
        e = (2 * p - 1)
        w = w_ori
        sum_of_sq = (d + e.pow(2)).sum(-1)
        #sum_of_sq = (e.pow(2)).sum(-1)
        sum_of_sq = sum_of_sq.unsqueeze(-1)
        sum_of_sq = sum_of_sq.expand(p.shape[0], w.shape[0])
        diag_p = torch.diag_embed(e)
        p_w = torch.matmul(w, diag_p)
        z_p_w = torch.zeros_like(p_w)
        shft_p_w = torch.cat((p_w, z_p_w), -1)
        sum_of_cross = torch.zeros_like(p_w)
        length = p.shape[1]
        for shft in range(1, length):
            sum_of_cross += shft_p_w[:, :, 0:length] * shft_p_w[:, :, shft:length + shft]
        sum_of_cross = sum_of_cross.sum(-1)
        result = (sum_of_sq + 2 * sum_of_cross) / (length ** 2) # Equation (4)
        return result

    def forward(self, input):
        binarize = BinarizeF.apply
        binary_weight = binarize(self.weight)
        if self.bias is None:
            return self.sim_neural_comp(input, binary_weight)
        else:
            print("Bias is not supported at current version")
            sys.exit(0)

    def reset_parameters(self):
        in_features, out_features = self.weight.size()
        stdv = math.sqrt(1.5 / (in_features + out_features))
        self.weight.data.uniform_(-stdv, stdv)
        if self.bias is not None:
            self.bias.data.zero_()
        self.weight.lr_scale = 1. / stdv

class QF_FB_BN_IAdj(nn.Module):
    def __init__(self, num_features, init_ang_inc=1, momentum=0.1,training = False):
        super(QF_FB_BN_IAdj, self).__init__()

        self.x_running_rot = Parameter(torch.zeros((num_features)), requires_grad=False)
        self.ang_inc = Parameter(torch.tensor(init_ang_inc,dtype=torch.float32),requires_grad=True)
        self.momentum = momentum

        self.printed = False
        self.x_mean_ancle = 0
        self.x_mean_rote = 0
        self.input = 0
        self.output = 0

    def forward(self, x, training=True):
        if not training:
            if not self.printed:
                self.printed = True
            x_1 = (self.x_running_rot * x)

        else:
            self.printed = False
            x = x.transpose(0, 1)
            x_sum = x.sum(-1).unsqueeze(-1).expand(x.shape)
            x_lack_sum = x_sum + x
            x_mean = x_lack_sum / x.shape[-1]
            ang_inc = (self.ang_inc > 0).float() * self.ang_inc + 1
            y = 0.5 / x_mean
            y = y.transpose(0, 1)
            y = y / ang_inc
            y = y.transpose(0, 1)
            x_moving_rot = (y.sum(-1) / x.shape[-1])
            self.x_running_rot[:] = self.momentum * self.x_running_rot + \
                                    (1 - self.momentum) * x_moving_rot
            x_1 = y * x
            x_1 = x_1.transpose(0, 1)
        return x_1

    def reset_parameters(self):
        self.reset_running_stats()
        self.ang_inc.data.zeros_()


class QF_FB_BN_BAdj(nn.Module):
    def __init__(self, num_features, momentum=0.1):
        super(QF_FB_BN_BAdj, self).__init__()
        self.x_running_rot = Parameter(torch.zeros(num_features), requires_grad=False)
        self.momentum = momentum
        self.x_l_0_5 = Parameter(torch.zeros(num_features), requires_grad=False)
        self.x_g_0_5 = Parameter(torch.zeros(num_features), requires_grad=False)

    def forward(self, x, training=True):
        if not training:
            x_1 = self.x_l_0_5 * (self.x_running_rot * (1 - x) + x)
            x_1 += self.x_g_0_5 * (self.x_running_rot * x)
        else:
            x = x.transpose(0, 1)
            x_sum = x.sum(-1)
            x_mean = x_sum / x.shape[-1]
            self.x_l_0_5[:] = ((x_mean <= 0.5).float())
            self.x_g_0_5[:] = ((x_mean > 0.5).float())
            y = self.x_l_0_5 * ((0.5 - x_mean) / (1 - x_mean))
            y += self.x_g_0_5 * (0.5 / x_mean)

            self.x_running_rot[:] = self.momentum * self.x_running_rot + \
                                    (1 - self.momentum) * y
            x = x.transpose(0, 1)
            x_1 = self.x_l_0_5 * (y * (1 - x) + x)
            x_1 += self.x_g_0_5 * (y * x)
        return x_1

class Net(nn.Module):
    def __init__(self,in_size,layers=[3],with_norm=True,given_ang=[[-1, 1, 1]],training=False,binary=False,classic=False):
        super(Net, self).__init__()

        self.in_size = in_size
        self.training = training
        self.with_norm = with_norm
        self.layer = len(layers)
        self.binary = binary
        self.classic = classic
        cur_input_size = in_size
        for idx in range(self.layer):
            fc_name = "fc"+str(idx)
            if classic:
                setattr(self, fc_name, MLP(cur_input_size, layers[idx], bias=False))
            else:
                setattr(self, fc_name, QF_FB_NC(cur_input_size, layers[idx], bias=False))
            cur_input_size = layers[idx]

        if self.with_norm:
            for idx in range(self.layer):
                IAdj_name = "IAdj"+str(idx)
                BAdj_name = "BAdj"+str(idx)
                setattr(self, BAdj_name, QF_FB_BN_BAdj(num_features=layers[idx]))
                setattr(self, IAdj_name, QF_FB_BN_IAdj(num_features=layers[idx], init_ang_inc=given_ang[idx], training=training))
            for idx in range(self.layer):
                bn_name = "bn"+str(idx)
                setattr(self, bn_name,nn.BatchNorm1d(num_features=layers[idx]))


    def forward(self, x, training=1):
        binarize = BinarizeF.apply
        clipfunc = ClipF.apply
        x = x.view(-1, self.in_size)
        if self.classic == 1 and self.with_norm==0:
            for layer_idx in range(self.layer):
                if self.binary and layer_idx==0:
                    x = binarize(x-0.5)
                x = getattr(self, "fc" + str(layer_idx))(x)
                x = x.pow(2)
        elif self.classic == 1 and self.with_norm==1:
            for layer_idx in range(self.layer):
                if self.binary and layer_idx==0:
                    x = (binarize(x - 0.5) + 1) / 2
                x = getattr(self, "fc" + str(layer_idx))(x)
                x = x.pow(2)
                x = getattr(self, "bn" + str(layer_idx))(x)
                x = clipfunc(x)

        elif self.classic == 0 and self.with_norm==0:
            for layer_idx in range(self.layer):
                if self.binary and layer_idx==0:
                    x = (binarize(x - 0.5) + 1) / 2
                x = getattr(self, "fc" + str(layer_idx))(x)
        else:   # Quantum Training
            if self.training == 1:
                for layer_idx in range(self.layer):
                    if self.binary and layer_idx==0:
                        x = (binarize(x-0.5)+1)/2
                    x = getattr(self, "fc"+str(layer_idx))(x)
                    x = getattr(self, "BAdj"+str(layer_idx))(x)
                    x = getattr(self, "IAdj"+str(layer_idx))(x)
            else:
                for layer_idx in range(self.layer):
                    if self.binary and layer_idx==0:
                        x = (binarize(x-0.5)+1)/2
                    x = getattr(self, "fc"+str(layer_idx))(x)
                    x = getattr(self, "BAdj"+str(layer_idx))(x, training=False)
                    x = getattr(self, "IAdj"+str(layer_idx))(x, training=False)
        return x

