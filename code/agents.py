# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:36:08 2016

@author: Rasmus
"""
import pyglet
import numpy as np
import math
from copy import deepcopy

import math_utility_module as mu
from sensor_module import RetinaSensor
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
advance(delta_time):

"""

    
class Fish(object):
    def  __init__(self, position, velocity, fish_id, environment, ann, image = None, sprite_batch = None):
        self.position = deepcopy(position)
        self.velocity = deepcopy(velocity)
        self.environment = environment
        self.ann = ann
        self.neighbourhood_radius = 100
        nbr_retina_cells = 4
        self.sensor = RetinaSensor(environment, self, nbr_retina_cells)
        
        if not (image is None):
            self.sprite = pyglet.sprite.Sprite(image, position[0], position[1], subpixel = True, batch = sprite_batch)
            self.sprite.scale = 0.5
    

    def think(self): # Can NOT change global system state, nor the pos./vel. of self       
        # Check what's around
        self.neighbouring_fish = [other_fish for other_fish in self.environment.fish_lst if mu.is_neighbour(self, other_fish, self.neighbourhood_radius)]
        self.neighbouring_predators = [predator for predator in self.environment.predator_lst if mu.is_neighbour(self, predator, self.neighbourhood_radius)]

        # run sensor and neural network
        friendly_sensor_output = self.sensor.read_fish()
        hostile_sensor_output = self.sensor.read_predators()
        ann_input = friendly_sensor_output + hostile_sensor_output
        ann_input = np.reshape(ann_input, [len(ann_input),1])        
        ann_output = self.ann.feed_forward(ann_input)
 
        # set angular velocity in interval [-pi/2,pi/2] based on ann-output
        self.angular_velocity = float(ann_output)*np.pi/2

    def advance(self, delta_time):
        # hacked in so we get something moving/rotating
        #self.velocity += ((np.random.rand(1,2)[0] * 2) - 1) * delta_time
        #self.velocity = mu.normalize(self.velocity)
        #if self.angular_velocity != 0:
         #   print(self.angular_velocity)
        self.velocity = mu.rotate_ccw(self.velocity, - self.angular_velocity*delta_time)
        self.position += self.velocity * delta_time * 20
        x_max = self.environment.boundaries[1]
        y_max = self.environment.boundaries[3]
        self.position[0]  = self.position[0] % x_max
        self.position[1] = self.position[1]  % y_max
        
        try:
            self.sprite.rotation = mu.dir_to_angle(self.velocity)
            self.sprite.set_position(self.position[0], self.position[1])
        except AttributeError: # Then the fish has no sprite
            pass
        #check for collisions, add repelleing forces
        # Use self.visible_fish to get potential collisions so that we don't have
        # to run the costly search more than once
 
        

class Predator(object):
    def  __init__(self, position, velocity, predator_id, environment, image = None, sprite_batch = None):
        self.position = position
        self.velocity = velocity
        if not (image is None):
            self.sprite = pyglet.sprite.Sprite(image, position[0], position[1], subpixel = True, batch = sprite_batch)
            self.sprite.scale = 0.5
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
        # hacked in so we get something moving/rotating
        self.velocity += ((np.random.rand(1,2)[0] * 2) - 1) * 0.01
        self.velocity = mu.normalize(self.velocity)
        self.position += self.velocity * delta_time * 20
        
        try:
            self.sprite.rotation = mu.dir_to_angle(self.velocity)
            self.sprite.set_position(self.position[0], self.position[1])
        except AttributeError: # Then the fish has no sprite
            pass

