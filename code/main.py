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
    settings.window_width = 800     # Also used as our simulation boundary
    settings.window_height = 600    # Also used as our simulation boundary
    settings.nbr_fishes = 50
    settings.nbr_predators = 1

    settings.fish_sprite_scale = 0.5
    settings.fish_nbr_retina_cells = 4
    settings.fish_neighbourhood_radius = 100
    settings.fish_speed = 20 # units per second in direction of velocity

    settings.predator_speed = 40

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
        
        for fish in environment.fish_lst:
            fish.think()
            ## demonstrate neigbour-detection
            #if fish.neighbouring_predators != [] and fish.sprite.image != environment.dead_fish_image:
            #    fish.sprite.image = environment.dead_fish_image
            
            # demonstrate sensor functionality
            if environment.settings.graphics_on:
                if sum(fish.sensor.read_predators()) != 0 and fish.sprite.image != environment.dead_fish_image:
                    fish.sprite.image = environment.dead_fish_image
                
        for predator in environment.predator_lst:
            predator.think()
        for fish in environment.fish_lst:
            fish.advance(dt)
        for predator in environment.predator_lst:
            predator.advance(dt)
       
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
    
  