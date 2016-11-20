# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:21:05 2016

@author: Rasmus
"""

import numpy as np
from copy import deepcopy
import unittest

class ANN(object):
    def __init__(self, weights, beta = 1):
        self._weight_matrices = deepcopy(weights) # weights is a list of matrices weights = [matrix_layer1, matrix_layer2,...]
        self._beta = beta


    def feed_forward(self, input_vector, check_formatting = False):
        #input vector must be column vector matching the first weightmatrix
        if check_formatting:
            weight_matrix0 = self._weight_matrices[0]
            assert(input_vector.shape == (weight_matrix0.shape[0], 1))
        input_i = input_vector
        for weight_matrix_i in self._weight_matrices:
            local_fields = weight_matrix_i @ input_i
            output_i = np.tanh(self._beta * local_fields)
            input_i = output_i
        return output_i
        
        
        
class TestANN(unittest.TestCase):

    def test_immutability(self):
        """ This test checks that the ANN instance does not keep a reference to
            the list that was originally fed to the constructor. We want to ensure
            that this is not the case, since that would give indirect 
            access to the ann._weight_matrices property, meaning the object could 
            easily be corrupted"""
        
        original_value = 1.5
        simple_matrix = np.ones([2,2]) * original_value
        lst_of_matrices = [simple_matrix, simple_matrix]
        ann = ANN(lst_of_matrices)
        simple_matrix[0][0] = -1
        self.assertEqual(ann._weight_matrices[0][0][0], original_value)

    def test_feed_forward_vector_ouput(self):
        """ Tests that the feed_forward executes correctly when the expected 
            output is a two-dimensional array (two ouput nodes)."""
        simple_matrix = np.zeros([2,2])
        simple_matrix[0][0] = 1
        lst_of_matrices = [simple_matrix, simple_matrix]
        ann = ANN(lst_of_matrices, beta = 5)

        expected_output = np.array([[1],[0]])
        ann_output = ann.feed_forward(np.ones([2,1]))
        
        self.assertTrue(abs(sum(ann_output-expected_output)) < 0.01)

    def test_feed_forward_single_output(self):
        """ Tests that the feed_forward executes correctly when the expected 
            output is a one-dimensional array (single output node)."""
        simple_matrix = np.zeros([2,2])
        simple_matrix[0][0] = 1
        lst_of_matrices = [simple_matrix, np.array([1,1])]
        ann = ANN(lst_of_matrices, beta = 5)

        expected_output = np.array([1])
        ann_output = ann.feed_forward(np.ones([2,1]))
        
        self.assertTrue(abs(sum(ann_output-expected_output)) < 0.01)


    def test_feed_forward_check_formatting1(self):
        """ Tests that the check_formatting logic does not halt execution when
            feed_forward is given correctly formatted input"""
        simple_matrix = np.zeros([2,2])
        simple_matrix[0][0] = 1
        lst_of_matrices = [simple_matrix, np.array([1,1])]
        ann = ANN(lst_of_matrices, beta = 5)

        expected_output = np.array([1])
        ann_output = ann.feed_forward(np.ones([2,1]), check_formatting = True)
        
        self.assertTrue(abs(sum(ann_output-expected_output)) < 0.01)

    def test_feed_forward_check_formatting2(self):
        """ Tests that the check_formatting logic raises AssertionError
            when feed_forward is given incorrectly formatted input"""        
        simple_matrix = np.zeros([2,2])
        simple_matrix[0][0] = 1
        lst_of_matrices = [simple_matrix, np.array([1,1])]
        ann = ANN(lst_of_matrices, beta = 5)

        try:
            ann_output = ann.feed_forward(np.ones([2,2]), check_formatting = True)
        except AssertionError:
            assertion_error_raised = True
        else:
            assertion_error_raised = False
        self.assertTrue(assertion_error_raised)


if __name__ == '__main__':
    unittest.main()
