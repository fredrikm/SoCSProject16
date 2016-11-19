# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:36:08 2016

@author: Rasmus
"""

from abc import ABCMeta, abstractmethod, abstractproperty

from sensor_module import _check_visibility_disk_util

""" Interface for fish

--- Variables ---
velocity (np.array)
position (np.array)
fish_id (integer)
environment (Environment)

--- Methods ---
think()       Can NOT change global system state
frame_advance(delta_time):

"""


""" Interface for predator

--- Variables ---
velocity (np.array)
position (np.array)
predator_id (integer)
environment (Environment)

--- Methods ---
think()       Can NOT change global system state
frame_advance(delta_time):

"""



    
class Fish(object):
    def  __init__(self, position, velocity, fish_id, environment, sensor, ann):
        pass
    """
    self.sensor = Sensor(self.environment)
    self.ann = ANN()
    # variables
    self.position #vector np.array
    self.velocity #vector np.array
    self.sensor #reference to instance of class Sensor, or sublcasses
    self.ann # instance of ANN
    self.environment # reference to global simulation state and variables/constants (include reference to self)
    self._time_since_last_ANN_update
    self.fish_index
    """
    

    def think(self): # Can NOT change global system state
    
        self.visible_fish, self.visibe_predators = _check_visibility_disk_util(self.environment.fish_lst, 
                                                   radius, field_of_view)
        pass
        """        sensor_output = self.sensor(self.fish_index)
        action = self.control(sensor_output)
        
        if turn right:
            rotate velocity +5degrees
            ....
        """     
    def advance(self, delta_time):
        #check for collisions, add repelleing forces
        pass
 
        
    

class Predator(object):
    def  __init__(self, position, velocity, predator_id, environment, sensor, fsm):
        pass
        """
        self.sensor = Sensor(broken, fuzzy,...)
        self.ann = ANN()
    # variables
    self.position #vector np.array
    self.velocity #vector np.array
    self.sensor #reference to instance of class Sensor, or sublcasses
    self.fsm # instance of FSM
    self.environment # reference to global simulation state and variables/constants
    self._time_since_last_ANN_update
    self.fish_index"""

    

    def think(self):
        pass
    """
        sensor_output = self.sensor(self.fish_index)
        action = self.fsm(sensor_output)
       """ 
    def advance(self, delta_time):
        pass
        

        
    

