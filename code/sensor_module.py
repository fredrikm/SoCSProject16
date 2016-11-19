# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:26:54 2016

@author: Rasmus
"""
import numpy as np
import math

import math_utility_module as mu



class RetinaCell(object):
    def __init__(self):
        self.agents_in_sight = []
    def read(self):
        if self.agents_in_sight == []:
            return 0
        else:
            return 1   
    def reset(self):
        self.agents_in_sight = []


class RetinaSensor(object): # Looks for fish
    def __init__(self, environment, agent, nbr_cells):
        assert nbr_cells%2 == 0, "There must be an even number of cells!"
        self.environment = environment
        self.agent = agent
        self._nbr_cells = nbr_cells
        self._cell_width = np.pi/nbr_cells
        self._retina_cells = [RetinaCell() for i in range(nbr_cells)]
        
        tmp = [i for i in range(-nbr_cells,nbr_cells)]
        tmp.pop(nbr_cells)
        self.cell_angles = tmp*np.pi/nbr_cells

    def read_fish(self, radius, field_of_view = -1):
        #pseudo code
        for cell in self.retina_cells:
            cell.reset()
        for fish in self.agent.visible_fish:
            cell = self.find_cell(fish)
            cell.agents_in_sight.append(fish)
        return [cell.res() for cell in self.retina_cells]
    
    def read_predators(self, radius, field_of_view = -1):
        #pseudo code
        for cell in self.retina_cells:
            cell.reset()
        for predator in self.agent.visible_predators:
            cell = self.find_cell(predator)
            cell.agents_in_sight.append(predator)
        return [cell.res() for cell in self.retina_cells]
        
    def find_cell(self, other_agent):
        # Must account for negative angle, how?!
        angle = mu.directed_angle2D(self.agent.velocity, other_agent.position)
        tmp = math.floor(angle / self._cell_width)
        index = tmp + self._nbr_cells/2
        return self._retina_cells[index]
