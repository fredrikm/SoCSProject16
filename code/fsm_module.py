# -*- coding: utf-8 -*-

class Predator_FSM(object):
    
    
    def __init__(self, predator, environment):
        self.predator = predator
        self.environment = environment
        self.state = "search"
        self.updates_since_switch = 0
    
    
    def next_action():
        pass