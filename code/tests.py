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
        ann_weights = [np.ones([4,8]), np.ones([1,4])]
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
        ann_weights = [np.ones([4,8]), np.ones([1,4])]
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
        ann_weights = [np.ones([4,8]), np.ones([1,4])]
        environment = Environment(3, 0, [0,10,0,10], ann_weights)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([[0],[0]])
        fishA.velocity = np.array([[1],[0]])
        fishA.neighbourhood_radius = 2
        fishB = environment.fish_lst[1]
        fishB.position = np.array([[0],[2.01]])       
        fishA.think()
        self.assertNotIn(fishB, fishA.neighbouring_fish)
    def test_periodicity(self):
        ann_weights = [np.ones([4,8]), np.ones([1,4])]
        boundaries =    [0,10,0,10]               
        environment = Environment(3, 0, [0,10,0,10], ann_weights)
        fishA = environment.fish_lst[0]

        x_min = boundaries[0]
        x_max = boundaries[1]
        y_min = boundaries[2]
        y_max = boundaries[3]

        for i in range(0,1000):
            fishA.think()
            fishA.advance(1)
            self.assertTrue(fishA.position[0] >= x_min)
            self.assertTrue(fishA.position[0] <= x_max)
            self.assertTrue(fishA.position[1] >= y_min)
            self.assertTrue(fishA.position[1] <= y_max)
                        
        
        
        


class TestFishRetina(unittest.TestCase):
    def test_read_fish_secctor0(self):
        ann_weights = [np.ones([4,8]), np.ones([1,4])]
        environment = Environment(2, 0, [0,10,0,10], ann_weights)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([[7],[6]])
        fishA.velocity = np.array([[1],[0]])
        fishA.neighbourhood_radius = 30
        fishB = environment.fish_lst[1]
        fishB.position = np.array([[1],[9]])       
        fishA.think()
        sensor_output = fishA.sensor.read_fish()
        self.assertEqual(sensor_output[0], 1)

    def test_read_fish_secctor1(self):
        ann_weights = [np.ones([4,8]), np.ones([1,4])]
        environment = Environment(2, 0, [0,10,0,10], ann_weights)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([[7],[6]])
        fishA.velocity = np.array([[1],[0]])
        fishA.neighbourhood_radius = 30
        fishB = environment.fish_lst[1]
        fishB.position = np.array([[13],[13]])       
        fishA.think()
        sensor_output = fishA.sensor.read_fish()
        self.assertEqual(sensor_output[1], 1)

    def test_read_fish_secctor2(self):
        ann_weights = [np.ones([4,8]), np.ones([1,4])]
        environment = Environment(2, 0, [0,10,0,10], ann_weights)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([[7],[6]])
        fishA.velocity = np.array([[1],[0]])
        fishA.neighbourhood_radius = 30
        fishB = environment.fish_lst[1]
        fishB.position = np.array([[10],[-2]])       
        fishA.think()
        sensor_output = fishA.sensor.read_fish()
        self.assertEqual(sensor_output[2], 1)
        
        
    def test_read_fish_secctor3(self):
        ann_weights = [np.ones([4,8]), np.ones([1,4])]
        environment = Environment(2, 0, [0,10,0,10], ann_weights)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([[7],[6]])
        fishA.velocity = np.array([[1],[0]])
        fishA.neighbourhood_radius = 30
        fishB = environment.fish_lst[1]
        fishB.position = np.array([[1],[1]])       
        fishA.think()
        sensor_output = fishA.sensor.read_fish()
        self.assertEqual(sensor_output[3], 1)


if __name__ == '__main__':
    unittest.main()
