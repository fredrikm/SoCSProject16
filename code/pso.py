import numpy as np
import particle
import unittest

class Pso:
    def __init__(self, function, number_of_particles, number_of_variables, c1, c2, inertia_max, inertia_min, beta, x_max, x_min):
        self.n_particles = number_of_particles
        self.n_variables = number_of_variables
        self.function = function

        self.particles = []
        for i in range(number_of_particles):
            self.particles.append(particle.Particle(self.n_variables, x_max, x_min))

        self.c1 = c1
        self.c2 = c2
        self.inertia = inertia_max
        self.inertia_min = inertia_min
        self.beta = beta

        self.swarm_best = np.zeros(self.n_variables)-1
        self.swarm_best_fitness = 2.0

    def evaluate_all_particles(self):

        for p in self.particles:
            position = p.position
            fitness = self.function(position)

            if fitness < p.particle_best_fitness:
                p.particle_best = p.position
                p.particle_best_fitness = fitness

                if fitness < self.swarm_best_fitness :
                    self.swarm_best = p.position
                    self.swarm_best_fitness = fitness

    def update_velocities(self):
        for p in self.particles:
            p.update_velocity(self.inertia, self.swarm_best, self.c1, self.c2)

    def update_positions(self):
        for p in self.particles:
            p.update_position()

    def update_inertia(self):
        if self.inertia>self.inertia_min:
            self.inertia = self.inertia*self.beta

    def advance(self):
        self.evaluate_all_particles()
        self.update_positions()
        self.update_velocities()
        self.update_inertia()

class TestPsoAlgorithm(unittest.TestCase):

    def test_benchmark_one(self):
        pso = Pso(self.benchmark_one,40, 2, 2, 2, 1.4, 0.4, 0.9999, 2, -2)
        sol = np.array([0,-1])
        tol = 10**(-3)


        while(np.linalg.norm(pso.swarm_best-sol)>tol):
            pso.evaluate_all_particles()
            pso.update_positions()
            pso.update_velocities()
            pso.update_inertia()

    def benchmark_one(self, position):
        x_1 = position[0]
        x_2 = position[1]

        s1 = (1+((x_1+x_2+1)**2)*(19-14*x_1+3*x_1**2-14*x_2+6*x_1*x_2+3*x_2**2))
        s2 = (30+((2*x_1-3*x_2)**2)*(18-32*x_1+12*x_1**2+48*x_2-36*x_1*x_2+27*x_2**2))

        return (s1*s2)

if __name__ == '__main__':
    unittest.main()
