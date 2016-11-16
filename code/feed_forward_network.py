# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 11:09:44 2016

@author: Rasmus
"""
import numpy as np
from copy import deepcopy


def random_lst(length):
    return [2*(np.random.rand()-0.5) for x in range(length)]

def random_column_vector(length):
    return np.reshape(random_lst(length), [length, 1])

def random_row_vector(length):
    return np.transpose(random_column_vector(length))


def random_matrix(nbr_rows, nbr_columns):
    temp = [random_lst(nbr_columns) for x in range(nbr_rows)]
    return np.reshape(temp, [nbr_rows, nbr_columns])

class MultilayerNetwork():
    def __init__(self, size_spec, beta):
        self.beta = beta
        self._size_spec = size_spec.copy
        self.nbr_of_layers = len(size_spec) #Inluding I/O layers
        self._neuron_vectors = [None for x in size_spec]
        self._weight_matrices = [None for x in range(self.nbr_of_layers-1)]
        self._threshold_vectors = [None for x in range(self.nbr_of_layers-1)]
        

        for i in range(self.nbr_of_layers-1):
            nbr_inputs = size_spec[i]
            nbr_outputs = size_spec[i+1]            
            self._weight_matrices[i] = random_matrix(nbr_outputs, nbr_inputs) * 0.2
            self._threshold_vectors[i] = random_column_vector(nbr_outputs)

    @property
    def size_spec(self):
        return deepcopy(self._size_spec)

    @property
    def neuron_vectors(self):
        return deepcopy(self._neuron_vectors)

    @property
    def weight_matrices(self):
        return deepcopy(self._weight_matrices)

    @property
    def threshold_vectors(self):
        return deepcopy(self._threshold_vectors)
    
    def g_prime(self, b):
        return self.beta*(1-np.tanh(self.beta*b)**2)



    def feed_forward(self, input_vector):
        self._neuron_vectors[0] = np.copy(input_vector)
        self._local_field_vectors = [None for x in range(self.nbr_of_layers-1)]
        for i in range(self.nbr_of_layers-1):
            input_i = self._neuron_vectors[i]
            self._local_field_vectors[i] = self.weight_matrices[i] @ input_i - self.threshold_vectors[i]
            output_i = np.tanh(self.beta * self._local_field_vectors[i])
            self._neuron_vectors[i+1] = output_i
        return np.copy(output_i)


    def propogate_back(self, expected_output, learning_rate):
        deltas = [None for x in range(self.nbr_of_layers-1)]
        tmp_weights = self.weight_matrices
        tmp_thresholds = self.threshold_vectors

        deltas[-1] = expected_output - self.neuron_vectors[-1]
        tmp_weights[-1] += learning_rate * deltas[-1] @ np.transpose(self._neuron_vectors[-2])
        tmp_thresholds[-1] += np.reshape(-learning_rate * deltas[-1], [1,1])
        for l in range(self.nbr_of_layers-3,-1,-1): # loop backwards to calculate errors
            g_prime_b = self.g_prime(self._local_field_vectors[l])
            tmp = np.transpose(self._weight_matrices[l+1]) @ deltas[l+1]
            deltas[l] = np.reshape([tmp[i]*g_prime_b[i] for i in range(len(tmp))], [len(tmp), 1])
            tmp_weights[l] += learning_rate * deltas[l] @ np.transpose(self._neuron_vectors[l])
            tmp_thresholds[l] += -learning_rate * deltas[l]
            
        
        self._weight_matrices = tmp_weights
        self._threshold_vectors = tmp_thresholds
            
    
    
    def __str__(self):
        tmp =  "--------- \n Instance of MultiLayerNetwork \n"
        if self._neuron_vectors[0] is None:
            tmp += "Neuron vectors empty; the network has not been fed any input"
        else:
            tmp += "Neuron States \n"
            for index, vector in enumerate(self._neuron_vectors):
                tmp += "Layer " + str(index) + ": \n " + str(vector) + "\n"
        return tmp + "---------"

    def weights2str(self):
        tmp = "--------- \n"
        for index, matrix in enumerate(self._weight_matrices):
                tmp += "Weight matrix for connections from layer " + str(index) 
                tmp += " to layer " + str(index+1) + ": \n"
                tmp += str(matrix) + " \n"
        return tmp + "--------."

    def thresholds2str(self):
        tmp = "--------- \n"
        for index, vector in enumerate(self._threshold_vectors):
                tmp += "Threshold vector for connections from layer " + str(index) 
                tmp += " to layer " + str(index+1) + ": \n"
                tmp += str(vector) + " \n"
        return tmp + "--------"

    
