# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 19:48:08 2016

@author: Rasmus
"""

import numpy as np

from pso import Pso
from environment_module import Environment, ConfigurationSettings


def evaluate(ann_weights, environment_settings , delta_t, nbr_of_iteraions):
    # ann_weights is a list of matrices  ann_weights = [matrix_layer1, matrix_layer2,...]
    
    # Instantiate our simulation environment
    environment = Environment(environment_settings, ann_weights)

    for i in range(nbr_of_iteraions):
        for fish in environment.fish_lst:
            fish.think()
        for predator in environment.predator_lst:
            predator.think()
        for fish in environment.fish_lst:
            fish.advance(delta_t)
        for predator in environment.predator_lst:
            predator.advance(delta_t)
        for fish in environment.fish_lst:
            # placeholder for predator eating fish
            if sum(fish.sensor.read_predators()) != 0:
                environment.fish_lst.remove(fish)
            
    fitness = len(environment.fish_lst)/environment_settings.nbr_fishes
    return fitness

def main():
    delta_t = 0.2
    nbr_of_iteraions = 500
    
    # envirnoment settings
    settings = ConfigurationSettings()    
    settings.window_width = 800     # Also used as our simulation boundary
    settings.window_height = 600    # Also used as our simulation boundary
    settings.nbr_fishes = 50
    settings.nbr_predators = 1
    settings.fish_nbr_retina_cells = 4
    settings.fish_neighbourhood_radius = 100
    settings.fish_speed = 20 # units per second in direction of velocity
    settings.predator_speed = 40    

    

    ann_weights = [np.ones([4,8]), np.ones([1,4])]
    fitness = evaluate(ann_weights, settings , delta_t, nbr_of_iteraions)
    print(fitness)

    
if __name__ == "__main__":
    main()