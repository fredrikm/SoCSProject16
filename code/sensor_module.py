# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:26:54 2016

@author: Rasmus
"""
import numpy as np
from main import Environment



class RetinaSensor(object):
    def __init__(self, environment, agent):
        self.environment = environment
        self.agent = agent

    def scan_surroundings(self, radius, field_of_view = -1):
        #pseudo code        
        for fish in agent.visible_fish:
            self.retina_sector.add_fish(fish)
        for predator in agent.visible_predators:
            self.retina_sector.add_predator(predator)
        return [retina_sector.calculate_output() for self.sector_generator]
        
        
class FishSensor(VisibilitySensor):
    def __init__(self):
        pass
        

class PredaotorSensor(VisiblitySensor):
    def __init__(self):
        pass
"""