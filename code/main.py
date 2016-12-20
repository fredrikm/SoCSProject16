# -*- coding: utf-8 -*-

import numpy as np
import pyglet

from environment_module import Environment, ConfigurationSettings
from main_optimization import results_from_file, decode_chromosome

# Entrypoint for presentation
if __name__ == "__main__":

    # settings
    settings = ConfigurationSettings()
    


    # simulation settings
    settings.k = 10**6
    settings.power = 6
    settings.window_width = 1024     # Also used as our simulation boundary
    settings.window_height = 768    # Also used as our simulation boundary
    settings.nbr_fishes = 40
    settings.nbr_predators = 1

    settings.fish_nbr_retina_cells = 4
    settings.fish_neighbourhood_radius2 = 150**2
    settings.fish_speed = 45  # units per second in direction of velocity

    settings.predator_nbr_retina_cells = 20
    settings.predator_neighbourhood_radius2 = 250**2
    settings.predator_attack_radius = 80 ** 2
    settings.predator_speed = 110
    settings.predator_feeding_frequency = 1.5

    # graphic settings
    settings.graphics_on = True
    settings.fish_sprite_scale = 0.25
    settings.predator_sprite_scale = 0.5
        
    # Create main window
    window = pyglet.window.Window(width = settings.window_width, height = settings.window_height, vsync = False)

    # Set resource path for pyglet
    pyglet.resource.path = ['./textures']
    pyglet.resource.reindex()

    fps_display = pyglet.clock.ClockDisplay()

    # Load results
    (chromosome, size_spec) = results_from_file('./network/_chromosome_', './network/_size_spec_')
    ann_weights = decode_chromosome(chromosome, size_spec)
    #ann_weights = [np.ones([4,8]), np.ones([1,4])]

    # Instantiate our simulation environment
    environment = Environment(settings, ann_weights)

    # runs once per frame
    def update(dt):

        fish_to_remove = []

        for fish in environment.fish_lst:
            fish.think()
                        
        for predator in environment.predator_lst:
            predator.think()
        for fish in environment.fish_lst:
            fish.advance(dt)
        for predator in environment.predator_lst:
            predator.advance(dt)

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

    pyglet.clock.schedule_interval(update, 1/30.0)
    pyglet.app.run()    
    
  