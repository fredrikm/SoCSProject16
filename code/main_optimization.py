# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 19:48:08 2016

@author: Rasmus
"""

from copy import deepcopy
from functools import partial
import numpy as np
import csv
import os
import random
import time

from pso import Pso

from environment_module import Environment, ConfigurationSettings



def encode_weights(ann_weights):
    weights_tmp = deepcopy(ann_weights)
    chromosome = []
    for i in range(len(ann_weights)):
        matrix_i = weights_tmp[i]
        array_i = matrix_i.flatten()
        list_i = array_i.tolist()
        chromosome.extend(list_i)
    return chromosome

def decode_chromosome(chromosome, size_spec):
    chromosome_tmp = deepcopy(chromosome)
    if type(chromosome_tmp) == np.ndarray:
        chromosome_tmp = chromosome_tmp.tolist()
    nbr_matrices = len(size_spec)-1
    ann_weights = [None for i in range(nbr_matrices)]
    for i in range(nbr_matrices):
            nbr_inputs = size_spec[i]
            nbr_outputs = size_spec[i+1]
            nbr_matrix_elements = nbr_inputs*nbr_outputs
            elements = [chromosome_tmp.pop(0) for i in range(nbr_matrix_elements)]
            ann_weights[i] = np.reshape(elements, [nbr_outputs, nbr_inputs])
    return ann_weights

def calculate_chromosome_length(ann_size_spec):
    chromosome_length = 0
    nbr_matrices = len(ann_size_spec)-1
    for i in range(nbr_matrices):
            nbr_inputs = ann_size_spec[i]
            nbr_outputs = ann_size_spec[i+1]
            nbr_matrix_elements = nbr_inputs*nbr_outputs
            chromosome_length += nbr_matrix_elements
    return chromosome_length

def evaluate_weights(ann_weights, environment_settings , delta_t, nbr_iterations):
    # ann_weights is a list of matrices  ann_weights = [matrix_layer1, matrix_layer2,...]  
    # Instantiate our simulation environment
    environment = Environment(environment_settings, ann_weights)
    # Run simulation
    t = time.time()

    for i in range(nbr_iterations):
        for fish in environment.fish_lst:
            fish.think()
        for predator in environment.predator_lst:
            predator.think()
        for fish in environment.fish_lst:
            fish.advance(delta_t)
        for predator in environment.predator_lst:
            predator.advance(delta_t)
        for predator in environment.predator_lst:
            predator.attack(delta_t)
        environment.remove_dead_fish()
    print('Elapsed time (seconds): '+str(time.time()-t))
    # Calculate fitness score
    surviving_fish = len(environment.fish_lst)
    inital_population_size = environment_settings.nbr_fishes
    rel_mortality = (inital_population_size - surviving_fish)/inital_population_size
    print('rel_mortality:' + str(rel_mortality))
    return rel_mortality

def evaluate_chromosome(chromosome, size_spec, environment_settings, delta_t, nbr_iterations):
    ann_weights = decode_chromosome(chromosome, size_spec)
    return evaluate_weights(ann_weights, environment_settings , delta_t, nbr_iterations)


def results_to_file(chromosome, size_spec, save_path, iteration, run_number):
    save_path = save_path[:-1] + str(run_number) + '/'
    save_path_chrom = save_path + "_run_" + str(iteration) + "_chromosome_"
    save_path_spec = save_path + "_run_" + str(iteration) + "_size_spec_"


    if not os.path.exists(save_path):
        os.mkdir(save_path, 0o755)

    np.savetxt(save_path_chrom, chromosome, delimiter = ",")
    np.savetxt(save_path_spec, size_spec, delimiter = ",")

def results_from_file(chromosome_path, size_spec_path):
    with open(chromosome_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        chromosome = [np.float(row[0]) for row in readCSV]        
    with open(size_spec_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        size_spec = [int(np.float(row[0])) for row in readCSV]
    return chromosome, size_spec

def main():
    # ann_settings
    size_spec = [8,4,1]
    # pso settings
    nbr_generations = 200
    number_of_particles = 20

    number_of_variables = calculate_chromosome_length(size_spec)
    c1 = 2
    c2 = 2
    inertia_max = 1.4
    inertia_min = 0.4
    beta = 0.99
    x_max = 2
    x_min = -2
    # simulation settings
    delta_t = 0.2
    nbr_iterations = round(80 / delta_t)
       
    # environment settings
    settings = ConfigurationSettings() 
       
    # simulation settings
    settings.k = 10**6
    settings.power = 6
    settings.window_width = 1024     # Also used as our simulation boundary
    settings.window_height = 768    # Also used as our simulation boundary
    settings.nbr_fishes = 40
    settings.nbr_predators = 1

    settings.fish_nbr_retina_cells = 4
    settings.fish_neighbourhood_radius2 = 90**2
    settings.fish_speed = 45  # units per second in direction of velocity

    settings.predator_nbr_retina_cells = 20
    settings.predator_neighbourhood_radius2 = 250**2
    settings.predator_attack_radius = 80 ** 2
    settings.predator_speed = 110
    settings.predator_feeding_frequency = 1.5

    evaluate = partial(evaluate_chromosome, size_spec = size_spec, environment_settings=settings, delta_t=delta_t, nbr_iterations=nbr_iterations)

    
    #instantiate pso
    pso = Pso(evaluate, number_of_particles, number_of_variables, c1, c2, inertia_max, inertia_min, beta, x_max, x_min)
    # run pso
    previous_best_fitness = np.inf
    fitnesses = np.zeros(nbr_generations)
    run_hash = random.getrandbits(16)

    for i in range(nbr_generations):
            pso.evaluate_all_particles()
            pso.update_positions()
            pso.update_velocities()
            pso.update_inertia()

            if pso.swarm_best_fitness < previous_best_fitness:
                previous_best_fitness = pso.swarm_best_fitness
                print("New best fitness: "+str(previous_best_fitness))
                print("For weights: "+str(pso.swarm_best))
            print("saving...")
            np.append(fitnesses, previous_best_fitness)
            save_path = '../best_network/'
            results_to_file(pso.swarm_best, size_spec, save_path, i, run_hash)
    
    print("------ RESULTS -------")
    print("Best network")
    print(pso.swarm_best)
    print("With relative mortality")
    print(previous_best_fitness)

    save_path = '../best_network' + str(run_hash) + '/fitnesses'
    print("Results have been saved to folder: " + save_path)
    np.savetxt(save_path, fitnesses)

    #debugging
    """ann_weights = [np.ones([4,8]), np.ones([1,4])]
    print(ann_weights)
    chromosome = encode_weights(ann_weights)
    print(chromosome)
    extracted_weights = decode_chromosome(chromosome,size_spec)
    print(extracted_weights)
    fitness = evaluate(chromosome)
    print(fitness)"""
    
if __name__ == "__main__":
    main()
