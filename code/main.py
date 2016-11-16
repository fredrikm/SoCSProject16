# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:35:18 2016

@author: Rasmus
"""

import numpy as np
from time import sleep

from agents import Fish, Predator
from neural_network import ANN
from sensor_module import VisibilitySensor
from fsm_module import Predator_FSM


def simulate(nbr_fish, nbr_predators, boundaries, ann_weights, nbr_of_iteraions = -1):
    # ann_weights is a list of matrices  ann_weights = [matrix_layer1, matrix_layer2,...]
    
    delta_t = 0.1
    environment = Environment(nbr_fish, nbr_predators, boundaries, ann_weights)
    i = 0
    while nbr_of_iteraions ==-1 or i<nbr_of_iteraions:
        for fish in environment.fish_lst:
            fish.think()
        for predator in environment.predator_lst:
            predator.think()
        for fish in environment.fish_lst:
            fish.advance(delta_t)
        for predator in environment.predator_lst:
            predator.advance(delta_t)
        
        present(environment)
        i += 1
        sleep(2)
    
    
    #TODO calculate fitness score
    fitness = -1
    return fitness
        

class Environment(object):
    def __init__(self, nbr_fish, nbr_predators, boundaries, ann_weights):
        sensor = VisibilitySensor(self)
        ann = ANN(ann_weights)
        fsm = Predator_FSM(self)
        position = np.array([0,0])
        velocity = np.array([0,0])
        
        self.fish_lst = [Fish(position, velocity, i, self, sensor, ann) for i in range(nbr_fish)] # Becomes for loop if we wanr to use different ANN variants for different fish        
        self.predator_lst = [Predator(position, velocity, i, self, sensor, fsm) for i in range(nbr_predators)]
        self.boundaries = boundaries
    
    def __to_string__():
        pass
        
        
def present(environment):
    print(environment)


if __name__ == "__main__":
    simulate(10,1,[0,10,0,10], [np.array([0,0]), np.array([0,0])], 3)