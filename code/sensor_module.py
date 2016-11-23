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


class RetinaSensor(object):
    def __init__(self, environment, agent, nbr_cells, radius = -1, field_of_view = -1):
        assert nbr_cells%2 == 0, "There must be an even number of cells!"
        self.environment = environment
        self.agent = agent
        self._nbr_cells = nbr_cells
        self._cell_width = np.pi/(nbr_cells/2)
        self._retina_cells = [RetinaCell() for i in range(nbr_cells)]
        self._radius = radius# placeholder for future sensor limitation
        self._field_of_view = field_of_view # placeholder for future sensor limitation
        
        tmp = [i*np.pi/nbr_cells for i in range(-nbr_cells,nbr_cells)]
        tmp.pop(nbr_cells)
        self.cell_angles = tmp

    def read_fish(self):
        for cell in self._retina_cells:
            cell.reset()
        for (fish, pos) in self.agent.neighbouring_fish:
            cell = self.find_cell(fish, pos)
            cell.agents_in_sight.append(fish)
        return [cell.read() for cell in self._retina_cells]
    
    def read_predators(self):
        for cell in self._retina_cells:
            cell.reset()
        for (predator, pos) in self.agent.neighbouring_predators:
            cell = self.find_cell(predator, pos)
            cell.agents_in_sight.append(predator)
        return [cell.read() for cell in self._retina_cells]
        
    def find_cell(self, other_agent, pos):
        rel_pos_other_agent = pos - self.agent.position
        angle = mu.directed_angle2D(rel_pos_other_agent, self.agent.velocity)
        tmp = math.floor(angle / self._cell_width)
        index = int(tmp + self._nbr_cells/2)
        return self._retina_cells[index]
