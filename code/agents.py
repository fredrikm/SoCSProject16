# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:36:08 2016

@author: Rasmus
"""
import pyglet
import numpy as np
import math
from abc import ABCMeta, abstractmethod, abstractproperty

import math_utility_module as mu

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
    def  __init__(self, position, velocity, fish_id, environment, sensor, ann, image = None, sprite_batch = None):
        self.position = position
        self.velocity = velocity
        if not (image is None):
            self.sprite = pyglet.sprite.Sprite(image, position[0], position[1], subpixel = True, batch = sprite_batch)
            self.sprite.scale = 0.5
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
        pass
        
        """        sensor_output = self.sensor(self.fish_index)
        action = self.control(sensor_output)
        
        if turn right:
            rotate velocity +5degrees
            ....
        """     
    def advance(self, delta_time):
        # hacked in so we get something moving/rotating
        self.velocity += ((np.random.rand(1,2)[0] * 2) - 1) * 0.1
        self.velocity = mu.normalize(self.velocity)
        self.position += self.velocity * delta_time * 20
        
        try:
            self.sprite.rotation = mu.dir_to_angle(self.velocity)
            self.sprite.set_position(self.position[0], self.position[1])
        except AttributeError: # Then the fish has no sprite
            pass
        #check for collisions, add repelleing forces
 
        
    

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
        

        
    

