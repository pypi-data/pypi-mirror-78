#!/usr/bin/env python
# Rui Zhang 8.2020
# rui.zhang@cern.ch

# import numpy as np
# import torch
# from torch.autograd import Function

# class HybridFunction(Function):
#     """ Hybrid quantum - classical function definition """
    
#     @staticmethod
#     def forward(ctx, input, quantum_circuit, shift):
#         """ Forward pass computation """
#         ctx.shift = shift
#         ctx.quantum_circuit = quantum_circuit

#         print('zhangr input forward', input, input.tolist())
#         expectation_z = ctx.quantum_circuit.run(input.tolist())
#         print('zhangr expectation_z', expectation_z)
#         result = torch.tensor([expectation_z])
#         ctx.save_for_backward(input, result)

#         return result
        
#     @staticmethod
#     def backward(ctx, grad_output):
#         """ Backward pass computation """
#         input, expectation_z = ctx.saved_tensors
#         input_list = np.array(input.tolist())
        
#         shift_right = input_list + np.ones(input_list.shape) * ctx.shift
#         shift_left = input_list - np.ones(input_list.shape) * ctx.shift
        
#         gradients = []
#         for i in range(len(input_list)):
#             expectation_right = ctx.quantum_circuit.run(shift_right[i]) / (2 * ctx.shift)
#             expectation_left  = ctx.quantum_circuit.run(shift_left[i]) / (2 * ctx.shift)
            
#             gradient = torch.tensor([expectation_right]) - torch.tensor([expectation_left])
#             gradients.append(gradient)
#         gradients = np.array([gradients]).T
#         return torch.tensor([gradients]).float() * grad_output.float(), None, None
