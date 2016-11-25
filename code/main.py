# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:35:18 2016

@author: Rasmus
"""

import numpy as np
import pyglet

from environment_module import Environment, ConfigurationSettings

# Entrypoint for presentation
if __name__ == "__main__":

    # settings
    settings = ConfigurationSettings()
    


    # simulation settings
    settings.k = 10**6
    settings.power = 4
    settings.window_width = 800     # Also used as our simulation boundary
    settings.window_height = 600    # Also used as our simulation boundary
    settings.nbr_fishes = 40
    settings.nbr_predators = 1

    settings.fish_nbr_retina_cells = 4
    settings.fish_neighbourhood_radius2 = 100**2
    settings.predator_attack_radius = 50 ** 2
    settings.fish_speed = 60 # units per second in direction of velocity

    settings.predator_nbr_retina_cells = 20
    settings.predator_neighbourhood_radius2 = 100**2
    settings.predator_speed = 100
    settings.predator_feeding_frequency = 5

    # graphic settings
    settings.graphics_on = True
    settings.fish_sprite_scale = 0.5
    settings.predator_sprite_scale = 0.6
        
    # Create main window
    window = pyglet.window.Window(width = settings.window_width, height = settings.window_height, vsync = False)

    # Set resource path for pyglet
    pyglet.resource.path = ['./textures']
    pyglet.resource.reindex()

    fps_display = pyglet.clock.ClockDisplay()

    ann_weights = [np.ones([4,8]), np.ones([1,4])]

    # Instantiate our simulation environment
    environment = Environment(settings, ann_weights)

    # runs once per frame
    def update(dt):

        fish_to_remove = []

        for fish in environment.fish_lst:
            fish.think()
            
            # demonstrate sensor functionality
            #if environment.settings.graphics_on:
                #if sum(fish.sensor.read_predators()) != 0 and fish.sprite.image != environment.dead_fish_image:
                    #fish.sprite.image = environment.dead_fish_image
                    #fish_to_remove.append(fish)
                        
        for predator in environment.predator_lst:
            predator.think()
        for fish in environment.fish_lst:
            fish.advance(dt)
        for predator in environment.predator_lst:
            predator.advance(dt)

        #for fish in fish_to_remove:
            #environment.fish_lst.remove(fish)

        for predator in environment.predator_lst:
            predator.attack(dt)

        environment.remove_dead_fish()
    # event when rendering is requested
    @window.event
    def on_draw():
        window.clear()
        
        # render spritebatches
        if environment.settings.graphics_on:
            environment.sprite_batch_fishes.draw()
            environment.sprite_batch_predators.draw()

            fps_display.draw()

    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()    
    
  