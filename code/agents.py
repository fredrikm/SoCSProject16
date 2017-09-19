# -*- coding: utf-8 -*-

import pyglet
import numpy as np
import math
from copy import deepcopy

import math_utility_module as mu
from sensor_module import RetinaSensor
    
class Fish(object):
    def  __init__(self, position, velocity, fish_id, environment, ann, image = None, sprite_batch = None):
        self.environment = environment
        self.position = deepcopy(position)
        self.velocity = deepcopy(velocity)                  # velocity is normalized
        self.speed = self.environment.settings.fish_speed   # We use same constant speed for all fishes now in the beginning
        self.ann = ann
        self.sensor = RetinaSensor(environment, self, self.environment.settings.fish_nbr_retina_cells)
        self.mass = 1
        self.is_alive = True
        
        # init virtual positions
        self.positions = self.environment.virtual_game_area.get_virtual_positions(self.position);

        if self.environment.settings.graphics_on:
            self.sprite = pyglet.sprite.Sprite(image, position[0], position[1], subpixel = True, batch = sprite_batch)
            self.sprite.scale = self.environment.settings.fish_sprite_scale


    def calculate_fish_forces(self):
        f = np.array([0.0, 0.0])
        neighbours = self.neighbouring_fish
        k = self.environment.settings.k
        power = self.environment.settings.power
        for (fish, pos) in neighbours:

            magnitude = k / np.linalg.norm(pos - self.position)**power
            if magnitude > 2:
                magnitude = 2
            direction = self.position-pos
            f_i = magnitude * direction
            f += f_i
        return f

    def find_neighbours(self):
        neighbours = []
        for fish in self.environment.fish_lst:
            (isa, pos) = mu.is_neighbour(self, fish, self.environment.settings.fish_neighbourhood_radius2)
            if isa == True:
                neighbours.append((fish, pos))

        return neighbours

    def find_hostile_neighbors(self):
        neighbours = []
        for predator in self.environment.predator_lst:
            (isa, pos) = mu.is_neighbour(self, predator, self.environment.settings.fish_neighbourhood_radius2)
            if isa == True:
                neighbours.append((predator, pos))

        return neighbours

    def think(self): # Can NOT change global system state, nor the pos./vel. of self       

        self.neighbouring_fish = self.find_neighbours()
        self.neighbouring_predators = self.find_hostile_neighbors()

        # run sensor and neural network
        friendly_sensor_output = self.sensor.read_fish()
        hostile_sensor_output = self.sensor.read_predators()
        ann_input = friendly_sensor_output + hostile_sensor_output
        ann_input = np.reshape(ann_input, [len(ann_input),1])        
        ann_output = self.ann.feed_forward(ann_input)
 
        # set angular velocity in interval [-pi/2,pi/2] based on ann-output
        self.angular_velocity = float(ann_output[0])*np.pi/2
        
        # set accelaration based on ann-output
        try:
            acc = float(ann_output[1])*10 # Helping network to get in working regime
            self.acceleration = np.sign(acc) * min([np.abs(acc), 18]) # Limit acc. to 2g
        except IndexError:
            self.acceleration = 0
        
        
    def advance(self, delta_time):

        # Update velocity
        turning_speed = 3;
        self.velocity = mu.rotate_ccw(self.velocity, - self.angular_velocity * delta_time * turning_speed)
        self.speed = self.speed + self.acceleration*delta_time
        self.speed = min([self.speed, self.environment.settings.fish_speed])
        self.speed = max([self.speed, 0.2*self.environment.settings.fish_speed]) # fish cannot stop completely
        force = self.calculate_fish_forces()
        self.velocity = mu.normalize(self.velocity) * self.speed + force / self.mass

        self.position += self.velocity * delta_time

        # Wrap around
        x_max = self.environment.boundaries[1]
        y_max = self.environment.boundaries[3]
        self.position[0]  = self.position[0] % x_max
        self.position[1] = self.position[1]  % y_max

        # Update virtual positions
        self.positions = self.environment.virtual_game_area.get_virtual_positions(self.position);

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
       
        # init virtual positions
        self.positions = self.environment.virtual_game_area.get_virtual_positions(self.position);
        
        self.sensor = RetinaSensor(environment, self, self.environment.settings.predator_nbr_retina_cells)
        if self.environment.settings.graphics_on:
            self.sprite = pyglet.sprite.Sprite(image, position[0], position[1], subpixel = True, batch = sprite_batch)
            self.sprite.scale = self.environment.settings.predator_sprite_scale

    def think(self):
        # Check what's around
        self.neighbouring_fish = []
        for fish in self.environment.fish_lst:
            (isa, pos) = mu.is_neighbour(self, fish, self.environment.settings.predator_neighbourhood_radius2)
            if isa == True:
                self.neighbouring_fish.append((fish, pos))
        # hack to override sensor instabilities
        if self.neighbouring_fish != []:
            fish_appeal_lst = []
            for (fish, pos) in self.neighbouring_fish:
                rel_fish_pos = self.position - pos
                distance2 = np.dot(rel_fish_pos, rel_fish_pos)
                angle = mu.calculate_angle2D(rel_fish_pos, self.velocity)                
                appeal = 1/(0.01 + distance2*angle)
                fish_appeal_lst.append(appeal)
            target_fish_index = mu.rws(fish_appeal_lst)
            self.neighbouring_fish = [self.neighbouring_fish[target_fish_index]]
        # run sensor
        sensor_output = self.sensor.read_fish()
        
        nbr_cells = len(sensor_output)
        tmp = [index for index, is_active in enumerate(sensor_output) if is_active]
        if tmp != []:
            winning_cell = np.mean(tmp)
            interval_size = (nbr_cells-1)/2
            desired_rotation = np.pi*( winning_cell - interval_size) / interval_size
        else:
            desired_rotation = 0

        angular_gain = 15
        self.angular_velocity = angular_gain*desired_rotation
        max_angular_vel = np.pi/2
        if abs(self.angular_velocity) > max_angular_vel:
            self.angular_velocity = np.sign(self.angular_velocity) * max_angular_vel

       
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

        # Update virtual positions
        self.positions = self.environment.virtual_game_area.get_virtual_positions(self.position);

        if self.environment.settings.graphics_on:
            self.sprite.rotation = mu.dir_to_angle(self.velocity)
            self.sprite.set_position(self.position[0], self.position[1])

    def attack(self, delta_time):
        
        r = np.random.rand()
        feeding_frequency = self.environment.settings.predator_feeding_frequency
        if r < delta_time * feeding_frequency:
            #Check for attackable fish
            self.attackable_fish = []
            for fish in self.environment.fish_lst:
                (isa, pos)=mu.is_neighbour(self, fish, self.environment.settings.predator_attack_radius)
                if isa == True:
                    self.attackable_fish.append(fish)
            nbr_attackable_fish = len(self.attackable_fish)
            if nbr_attackable_fish>0:
                index_attack = np.random.randint(nbr_attackable_fish)
                attacked_fish = self.attackable_fish[index_attack]
                attacked_fish.is_alive = False
        else:
            pass # no eating this time
