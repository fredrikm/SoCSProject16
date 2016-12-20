# -*- coding: utf-8 -*-

import numpy as np

class Particle:
    def __init__(self, nbr_variables, x_max, x_min):
        self.n_variables = nbr_variables

        self.position = np.zeros(nbr_variables)
        for i in range(nbr_variables):
            r = np.random.rand()
            self.position[i] = x_min + r*(x_max-x_min)

        self.velocity = np.zeros(nbr_variables)
        for i in range(nbr_variables):
            r = np.random.rand()
            self.velocity[i] = (-(x_max - x_min) / 2 + r * (x_max - x_min))

        self.v_max = x_max-x_min
        self.particle_best = self.position
        self.particle_best_fitness = np.inf

    def update_velocity(self, inertia, swarm_best, C1, C2):
        q = np.random.rand()
        r = np.random.rand()

        self.velocity = inertia*self.velocity+C1*q*(self.particle_best-self.position)+C2*r*(swarm_best-self.position)

        for i in range(self.n_variables):
            if  self.velocity[i] > self.v_max:
                self.velocity[i] = self.v_max
            elif self.velocity[i] < -self.v_max:
                self.velocity[i] = -self.v_max

    def update_position(self):
        self.position = self.position + self.velocity
