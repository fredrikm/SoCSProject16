# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 11:03:48 2016

@author: Rasmus
"""
import numpy as np
import unittest

from environment_module import Environment, ConfigurationSettings
from agents import Fish

def create_environment(nbr_fishes, nbr_predators, boundaries, radius):
    # settings
    settings = ConfigurationSettings()

    settings.k = 10**6
    settings.power = 4
    settings.window_width = boundaries[1]
    settings.window_height = boundaries[3]
    settings.nbr_fishes = nbr_fishes
    settings.nbr_predators = nbr_predators

    settings.fish_sprite_scale = 0.5
    settings.fish_nbr_retina_cells = 4
    settings.fish_neighbourhood_radius2 = radius**2
    settings.fish_speed = 20 # units per second in direction of velocity

    settings.predator_nbr_retina_cells = 20
    settings.predator_neighbourhood_radius2 = radius**2
    settings.predator_speed = 40

    # graphic settings
    settings.graphics_on = False
    settings.fish_sprite_scale = 0.5
    settings.predator_sprite_scale = 0.6

    ann_weights = [np.ones([4,8]), np.ones([1,4])]

    return Environment(settings, ann_weights)

def is_fish_in_list(fish, list):
    for (f, pos) in list:
        if f == fish:
            return True
    return False

def is_predator_in_list(predator, list):
    for (f, pos) in list:
        if f == predator:
            return True
    return False

def set_fish_position(environment, index, position):
    fish = environment.fish_lst[index]
    fish.position = position
    fish.positions = fish.environment.virtual_game_area.get_virtual_positions(position)

    return fish

class TestFishNeigbourhood(unittest.TestCase):
    def test_detection_fish(self): # Test that fish within neigbourhood radius is detected
        #ann_weights = [np.ones([4,8]), np.ones([1,4])]
        environment = create_environment(2, 0, [0,10,0,10], 2)

        fishA = set_fish_position(environment, 0, np.array([0, 0]))
        fishB = set_fish_position(environment, 1, np.array([0, 0.5]))

        fishA.think()

        self.assertTrue(is_fish_in_list(fishB, fishA.neighbouring_fish))

    def test_detection_of_predator(self): # Test that predator within neigbourhood radius is detected
        environment = create_environment(3, 1, [0,10,0,10], 2)

        fish = set_fish_position(environment, 0, np.array([0,0]))

        predator = environment.predator_lst[0]
        predator.position = np.array([0,10])
        predator.positions = predator.environment.virtual_game_area.get_virtual_positions(predator.position)
        fish.think()

        self.assertTrue(is_predator_in_list(predator, fish.neighbouring_predators))

    def test_detection_predator(self):
        environment = create_environment(3, 1, [0, 10, 0, 10], 2)

        fish = set_fish_position(environment, 0, np.array([0, 10]))

        predator = environment.predator_lst[0]
        predator.position = np.array([0, 10])
        predator.positions = predator.environment.virtual_game_area.get_virtual_positions(predator.position)
        predator.think()

        self.assertTrue(is_fish_in_list(fish, predator.neighbouring_fish))

    def test_rejection(self): # Test that fish outside neigbourhood radius is NOT detected
        environment = create_environment(3, 0, [0,10,0,10], 2)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([0,0])
        fishA.velocity = np.array([1,0])
        fishB = environment.fish_lst[1]
        fishB.position = np.array([0,2.01])
        fishA.think()
        self.assertFalse(is_fish_in_list(fishB, fishA.neighbouring_fish))
    def test_periodicity(self):
        boundaries =    [0,10,0,10]
        environment = create_environment(3, 0, [0,10,0,10], 2)
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





"""
class TestFishRetina(unittest.TestCase):
    def test_read_fish_secctor0(self):
        environment = create_environment(2, 0, [0,10,0,10], 30)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([7,6])
        fishA.velocity = np.array([1,0])
        fishB = environment.fish_lst[1]
        fishB.position = np.array([1,9])       
        fishA.think()
        sensor_output = fishA.sensor.read_fish()
        self.assertEqual(sensor_output[0], 1)

    def test_read_fish_secctor1(self):
        environment = create_environment(2, 0, [0,10,0,10], 30)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([7,6])
        fishA.velocity = np.array([1,0])
        fishB = environment.fish_lst[1]
        fishB.position = np.array([13,13])       
        fishA.think()
        sensor_output = fishA.sensor.read_fish()
        self.assertEqual(sensor_output[1], 1)

    def test_read_fish_secctor2(self):
        environment = create_environment(2, 0, [0,10,0,10], 30)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([7,6])
        fishA.velocity = np.array([1,0])
        fishB = environment.fish_lst[1]
        fishB.position = np.array([10,-2])       
        fishA.think()
        sensor_output = fishA.sensor.read_fish()
        self.assertEqual(sensor_output[2], 1)
        
        
    def test_read_fish_secctor3(self):
        environment = create_environment(2, 0, [0,10,0,10], 30)
        fishA = environment.fish_lst[0]
        fishA.position = np.array([7,6])
        fishA.velocity = np.array([1,0])
        fishB = environment.fish_lst[1]
        fishB.position = np.array([1,1])       
        fishA.think()
        sensor_output = fishA.sensor.read_fish()
        self.assertEqual(sensor_output[3], 1)
"""

if __name__ == '__main__':
    unittest.main()
