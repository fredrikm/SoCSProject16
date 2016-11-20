# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 11:03:48 2016

@author: Rasmus
"""
import numpy as np
import unittest

from main import Environment
from agents import Fish


class TestFishNeigbourhood(unittest.TestCase):
    def test_detection_fish(self): # Test that fish within neigbourhood radius is detected
        ann_weights = [np.array([0,0]), np.array([0,0])]
        environment = Environment(3, 0, [0,10,0,10], ann_weights)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([[0],[0]])
        fishA.velocity = np.array([[1],[0]])
        fishA.neighbourhood_radius = 2
        fishB = environment.fish_lst[1]
        fishB.position = np.array([[0],[0.5]])       
        fishA.think()
        self.assertIn(fishB, fishA.neighbouring_fish)

    def test_detection_predator(self): # Test that predator within neigbourhood radius is detected
        ann_weights = [np.array([0,0]), np.array([0,0])]
        environment = Environment(3, 1, [0,10,0,10], ann_weights)
        fish = environment.fish_lst[0]
        fish.position = np.array([[0],[0]])
        fish.velocity = np.array([[1],[0]])
        fish.neighbourhood_radius = 2
        predator = environment.predator_lst[0]
        predator.position = np.array([[0],[0.5]])       
        fish.think()
        self.assertIn(predator, fish.neighbouring_predators)

    def test_rejection(self): # Test that fish outside neigbourhood radius is NOT detected
        ann_weights = [np.array([0,0]), np.array([0,0])]
        environment = Environment(3, 0, [0,10,0,10], ann_weights)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([[0],[0]])
        fishA.velocity = np.array([[1],[0]])
        fishA.neighbourhood_radius = 2
        fishB = environment.fish_lst[1]
        fishB.position = np.array([[0],[2.01]])       
        fishA.think()
        self.assertNotIn(fishB, fishA.neighbouring_fish)

if __name__ == '__main__':
    unittest.main()
