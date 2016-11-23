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
        self.environment = environment
        self.position = deepcopy(position)
        self.velocity = deepcopy(velocity)                  # velocity is normalized
        self.speed = self.environment.settings.fish_speed   # We use same constant speed for all fishes now in the beginning
        self.ann = ann
        self.sensor = RetinaSensor(environment, self, self.environment.settings.fish_nbr_retina_cells)
        self.mass = 1
        if self.environment.settings.graphics_on:
            self.sprite = pyglet.sprite.Sprite(image, position[0], position[1], subpixel = True, batch = sprite_batch)
            self.sprite.scale = self.environment.settings.fish_sprite_scale


    def calculate_fish_forces(self):
        f = np.array([0.0, 0.0])
        neighbours = self.find_neighbours()
        k = self.environment.settings.k
        power = self.environment.settings.power
        for fish in neighbours:

            magnitude = k / np.linalg.norm(fish.position-self.position)**power
            direction = self.position-fish.position
            f_i = magnitude * direction
            f += f_i
        return f

    def find_neighbours(self):
        neighbours = [other_fish for other_fish in self.environment.fish_lst if mu.is_neighbour(self, other_fish, self.environment.settings.fish_neighbourhood_radius)]
        return neighbours

    def find_hostile_neighbors(self):
        return [predator for predator in self.environment.predator_lst if mu.is_neighbour(self, predator, self.environment.settings.fish_neighbourhood_radius)]




    def think(self): # Can NOT change global system state, nor the pos./vel. of self       
        # Check what's around

        self.neighbouring_fish = self.find_neighbours()
        self.neighbouring_predators = self.find_hostile_neighbors()

        # run sensor and neural network
        friendly_sensor_output = self.sensor.read_fish()
        hostile_sensor_output = self.sensor.read_predators()
        ann_input = friendly_sensor_output + hostile_sensor_output
        ann_input = np.reshape(ann_input, [len(ann_input),1])        
        ann_output = self.ann.feed_forward(ann_input)
 
        # set angular velocity in interval [-pi/2,pi/2] based on ann-output
        self.angular_velocity = float(ann_output)*np.pi/2

    def advance(self, delta_time):

         # Update velocity and position
        #self.velocity = mu.rotate_ccw(self.velocity, - self.angular_velocity * delta_time)

        force = self.calculate_fish_forces()
        self.velocity = mu.normalize(self.velocity+force / self.mass ) * self.speed
        self.position += self.velocity * delta_time



        # Wrap around
        x_max = self.environment.boundaries[1]
        y_max = self.environment.boundaries[3]
        self.position[0]  = self.position[0] % x_max
        self.position[1] = self.position[1]  % y_max

        # Update sprite if we are running with graphics on        
        if self.environment.settings.graphics_on:

            self.sprite.rotation = mu.dir_to_angle(self.velocity)
            self.sprite.set_position(self.position[0], self.position[1])


        

class Predator(object):
    def  __init__(self, position, velocity, predator_id, environment, image = None, sprite_batch = None):
        self.environment = environment
        self.position = position
        self.velocity = velocity
        self.speed = self.environment.settings.predator_speed
        self.environment = environment
        self.neighbourhood_radius = 400
        nbr_retina_cells = 20
        self.sensor = RetinaSensor(environment, self, nbr_retina_cells)
        if self.environment.settings.graphics_on:
            self.sprite = pyglet.sprite.Sprite(image, position[0], position[1], subpixel = True, batch = sprite_batch)
            self.sprite.scale = self.environment.settings.predator_sprite_scale

    def think(self):
        # Check what's around
        self.neighbouring_fish = [other_fish for other_fish in self.environment.fish_lst if mu.is_neighbour(self, other_fish, self.neighbourhood_radius)]

        # run sensor
        sensor_output = self.sensor.read_fish()
        
        nbr_cells = len(sensor_output)
        tmp = [index for index, is_active in enumerate(sensor_output) if is_active]
        winning_cell = np.mean(tmp)
        interval_size = (nbr_cells-1)/2
        desired_rotation = np.pi*( winning_cell - interval_size) / interval_size
        
        angular_gain = 20
        self.angular_velocity = angular_gain*desired_rotation

       
    """
        sensor_output = self.sensor(self.fish_index)
        action = self.fsm(sensor_output)
       """ 
    def advance(self, delta_time):
        # hacked in so we get something moving/rotating
        #self.velocity += ((np.random.rand(1,2)[0] * 2) - 1) * 0.01
        self.velocity = mu.normalize(self.velocity)
        max_rotation = np.pi/4
        rotation = self.angular_velocity*delta_time
        if abs(rotation) > max_rotation:
            rotation = np.sign(rotation) * max_rotation
        self.velocity = mu.rotate_ccw(self.velocity, -rotation)
        self.position += self.velocity * self.environment.settings.predator_speed * delta_time
        
        # Wrap around
        x_max = self.environment.boundaries[1]
        y_max = self.environment.boundaries[3]
        self.position[0]  = self.position[0] % x_max
        self.position[1] = self.position[1]  % y_max

        if self.environment.settings.graphics_on:
            self.sprite.rotation = mu.dir_to_angle(self.velocity)
            self.sprite.set_position(self.position[0], self.position[1])

