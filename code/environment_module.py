# -*- coding: utf-8 -*-

import random
import numpy as np
import pyglet

from agents import Fish, Predator
from sensor_module import RetinaSensor
from fsm_module import Predator_FSM
from neural_network import ANN
import math_utility_module as mu
from virtual_game_area import VirtualGameArea

# Configuration settings
class ConfigurationSettings(object):
    def __init__(self):
        self.window_width = -1
        self.window_height = -1
        self.nbr_fishes = -1
        self.nbr_predators = -1
        self.graphics_on = False

        # fish parameters
        self.fish_sprite_scale = -1
        self.fish_nbr_retina_cells = -1
        self.fish_neighbourhood_radius2 = -1
        self.fish_speed = 0

        # predator parameters
        self.predator_sprite_scale = -1
        self.predator_nbr_retina_cells = -1
        self.predator_neighbourhood_radius2 = -1
        self.predator_attack_radius = -1
        self.predator_speed = 0
        self.predator_feeding_frequency = 1

   

# The simulation environment
class Environment(object):

    def __init__(self, config_settings, ann_weights):
        ann = ANN(ann_weights)

        # Configuration
        self.settings = config_settings

        # We derive boundaries from window width/height
        self.boundaries = [0, self.settings.window_width, 0, self.settings.window_height]

        self.virtual_game_area = VirtualGameArea(self.settings.window_width, self.settings.window_height)

        #fsm = Predator_FSM(self)

        if self.settings.graphics_on:
            # sprites
            fish_image = pyglet.resource.image("orange_fish.png")
            predator_image = pyglet.resource.image("shark.jpg")
            self.dead_fish_image = pyglet.resource.image("dead_fish.png")
            self.center_image(fish_image)
            self.center_image(predator_image)
            self.center_image(self.dead_fish_image)
            # sprite batches for performance
            self.sprite_batch_fishes = pyglet.graphics.Batch()
            self.sprite_batch_predators = pyglet.graphics.Batch()

        else:
            fish_image = None
            self.sprite_batch_fishes = None
            predator_image = None
            self.sprite_batch_predators = None
        
        # Initialize fishes
        self.fish_lst = []
        for i in range(self.settings.nbr_fishes):
            pos = np.array([np.random.random() * self.boundaries[1], np.random.random() * self.boundaries[1]])
            velocity = mu.normalize(np.array([random.randint(-100,100), random.randint(-100,100)]))

            fish = Fish(pos, velocity, i, self, ann, fish_image, self.sprite_batch_fishes)
            self.fish_lst.append(fish)


        # Initialize predators
        position = np.array([200.0,200.0])
        velocity = np.array([0.1,0.1])
        self.predator_lst = [Predator(position, velocity, i, self, predator_image, self.sprite_batch_predators) for i in range(self.settings.nbr_predators)]
               
    
    def __str__(self):
        return "Environment object"

    # centers an image so it's rotation is around it's center
    def center_image(self, image):
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2

    def remove_dead_fish(self):

        for fish in self.fish_lst:
            if not fish.is_alive:
                fish.sprite.image = self.dead_fish_image
                self.fish_lst.remove(fish)