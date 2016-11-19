# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:32:21 2016

@author: Rasmus
"""

class Predator_FSM(object):
    
    
    def __init__(self, predator, environment, visibility):
        self.predator = predator
        self.environment = environment
        self.state = "search"
        self.updates_since_switch = 0
    
    
    def next_action():
        
        
        
