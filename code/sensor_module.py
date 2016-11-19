# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:26:54 2016

@author: Rasmus
"""
import numpy as np
from main import Environment



def _check_visibility_disk_util(agent, surrounding_agents, radius, field_of_view = -1):
    visible_agents = []
    for other_agent in surrounding_agents:
        distance = np.linalg.norm(other_agent.position-agent.position)
        if distance <= radius:
            if field_of_view == -1: #No limitation on field of view
                visible_agents.append(other_agent)
            else:
                normalized_agent_pos = agent.position / np.linalg.norm(agent.position)
                normalized_other_pos = other_agent.position / np.linalg.norm(other_agent.position)
                
                angle = float(np.arccos(np.transpose(normalized_agent_pos) @ normalized_other_pos))
                if angle <= field_of_view:
                    visible_agents.append(other_agent)
    return visible_agents
            
""" Disregard for now

class VisibilitySensor(object):
    def __init__(self, environment, agent):
        self.environment = environment
        self.agent = agent

    def scan_surroundings(self, radius, field_of_view = -1):
        visible_fish = _check_visibility_disk_util(self, self.environment.fish_lst, 
                                                   radius, field_of_view)
        visible_predators = _check_visibility_disk_util(self, self.environment.predator_lst, 
                                                   radius, field_of_view)
        return visible_fish, visible_predators

class FishSensor(VisibilitySensor):
    def __init__(self):
        pass
        

class PredaotorSensor(VisiblitySensor):
    def __init__(self):
        pass
"""