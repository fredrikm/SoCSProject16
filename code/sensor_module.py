# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:26:54 2016

@author: Rasmus
"""
import numpy as np
from main import Environment


class RetinaCell(object):
    def __init__(self):
        self.agents_in_sight = []
    def read():
        if self.agents_in_sight == []:
            return 0
        else:
            return 1   
    def reset():
        self.agents_in_sight = []


class RetinaSensor(object): # Looks for fish
    def __init__(self, environment, agent, nbr_cells):
        self.environment = environment
        self.agent = agent
        
    def read_fish(self, radius, field_of_view = -1):
        #pseudo code
        for cell in self.retina_cells:
            cell.reset()
        for fish in self.agent.visible_fish:
            cell = find_cell(fish)
            cell.agents_in_sight.append(fish)
        return [cell.res() for cell in self.retina_cells]
    
    def read_predators(self, radius, field_of_view = -1):
        #pseudo code
        for cell in self.retina_cells:
            cell.reset()
        for predator in self.agent.visible_predators:
            cell = find_cell(predator)
            cell.agents_in_sight.append(predator)
        return [cell.res() for cell in self.retina_cells]