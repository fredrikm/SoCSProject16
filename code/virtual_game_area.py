# -*- coding: utf-8 -*-

import numpy as np
from agents import Fish


class VirtualGameArea(object):
    def __init__(self, width, height):
        self.game_area_width = width
        self.game_area_height = height

    def get_virtual_positions(self, pos):
        p1 = pos + np.array([0, self.game_area_height])
        p2 = pos + np.array([self.game_area_width, self.game_area_height])
        p3 = pos + np.array([self.game_area_width, 0])
        p4 = pos + np.array([self.game_area_width, -self.game_area_height])
        p5 = pos + np.array([0, -self.game_area_height])
        p6 = pos + np.array([-self.game_area_width, -self.game_area_height])
        p7 = pos + np.array([-self.game_area_width, 0])
        p8 = pos + np.array([-self.game_area_width, self.game_area_height])

        return [pos, p1, p2, p3, p4, p5, p6, p7, p8]

