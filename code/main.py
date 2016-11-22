# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:35:18 2016

@author: Rasmus
"""

import numpy as np
from time import sleep
import pyglet
import random

from agents import Fish, Predator
from neural_network import ANN
from sensor_module import RetinaSensor
from fsm_module import Predator_FSM
import math_utility_module as mu


def simulate(nbr_fish, nbr_predators, boundaries, ann_weights, nbr_of_iteraions = -1):
    # ann_weights is a list of matrices  ann_weights = [matrix_layer1, matrix_layer2,...]
    
    delta_t = 0.1
    environment = Environment(nbr_fish, nbr_predators, boundaries, ann_weights)
    i = 0
    while nbr_of_iteraions ==-1 or i<nbr_of_iteraions:
        for fish in environment.fish_lst:
            fish.think()
        for predator in environment.predator_lst:
            predator.think()
        for fish in environment.fish_lst:
            fish.advance(delta_t)
        for predator in environment.predator_lst:
            predator.advance(delta_t)
        
        i += 1
        print(environment)
    
    #TODO calculate fitness score
    fitness = -1
    return fitness
        

class Environment(object):

    #sprite_batch_fishes = pyglet.graphics.Batch()

    def __init__(self, nbr_fish, nbr_predators, boundaries, ann_weights, graphics_on = False):
        ann = ANN(ann_weights)
        #fsm = Predator_FSM(self)
        position = np.array([200.0, 200.0])
        velocity = np.array([0.1, 0.1])

        if graphics_on:
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
        for i in range(nbr_fish):
            pos = np.array([np.random.random() * boundaries[1], np.random.random() * boundaries[1]])
            velocity = mu.normalize(np.array([random.randint(-100,100), random.randint(-100,100)]))

            fish = Fish(pos, velocity, i, self, ann, fish_image, self.sprite_batch_fishes)
            self.fish_lst.append(fish)

        # Initialize physical constants of  Coloumb force equation
        self.k = 10
        self.power = 2

        #self.fish_lst = [Fish(position, velocity, i, self, sensor, ann) for i in range(nbr_fish)] # Becomes for loop if we wanr to use different ANN variants for different fish        
        self.predator_lst = [Predator(position, velocity, i, self, predator_image, self.sprite_batch_predators) for i in range(nbr_predators)]
        
        self.boundaries = boundaries
    
    def __str__(self):
        return "Environment object"

    # centers an image so it's rotation is around it's center
    def center_image(self, image):
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2


if __name__ == "__main__":
    # Create main window, we hardcode size for now
    window = pyglet.window.Window(width = 800, height = 600, vsync = False)

    # Set resource path for pyglet
    pyglet.resource.path = ['./textures']
    pyglet.resource.reindex()

    fps_display = pyglet.clock.ClockDisplay()

    nbr_fish = 20
    nbr_predators = 1
    boundaries = [0, window.width, 0, window.height]
    ann_weights = [np.array([0,0]), np.array([0,0])]

    environment = Environment(nbr_fish, nbr_predators, boundaries, ann_weights, graphics_on = True)

    # runs once per frame
    def update(dt):
        
        for fish in environment.fish_lst:
            fish.think()
            ## demonstrate neigbour-detection
            #if fish.neighbouring_predators != [] and fish.sprite.image != environment.dead_fish_image:
            #    fish.sprite.image = environment.dead_fish_image
            
            # demonstrate sensor functionality
            if sum(fish.sensor.read_predators()) != 0 and fish.sprite.image != environment.dead_fish_image:
                fish.sprite.image = environment.dead_fish_image
                
        for predator in environment.predator_lst:
            predator.think()
        for fish in environment.fish_lst:
            fish.advance(dt)
        for predator in environment.predator_lst:
            predator.advance(dt)
       
    # event when renderig is requested
    @window.event
    def on_draw():
        window.clear()
        
        # render the spritebatch containing fishes
        environment.sprite_batch_fishes.draw()
        environment.sprite_batch_predators.draw()


        fps_display.draw()
        
    def present(environment):
        print(environment)

    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
   
    #simulate(10,1,[0,10,0,10], [np.array([0,0]), np.array([0,0])], 100)

  