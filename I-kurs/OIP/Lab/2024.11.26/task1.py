# Description: This script simulates a genetic algorithm to optimize the placement of Wi-Fi access points in a classroom to maximize signal coverage. It initializes a population of random access point positions, iteratively improves their placement over several generations using selection, crossover, and mutation, and visualizes the initial and final distributions as well as the dynamic changes in signal strength and fitness scores across generations.
# Tags: Genetic Algorithm, Optimization, Wi-Fi Placement, Signal Strength, Visualization

import random
import scipy.io
import matplotlib.pyplot as plt
import numpy as np


classroom_width = 7
classroom_length = 5
num_app = 5
population_size = 12
generations = 10
mutation_rate = 0.1


initial_population = [(random.uniform(0, classroom_width), random.uniform(0, classroom_length))
                      for _ in range(population_size)]
population = [initial_population.copy()]

best_solution = None
best_fitness = float('-inf')
all_fitness_scores = []


def calculate_signal_strength(ap_x, ap_y, point_x, point_y):
    distance = np.sqrt((ap_x - point_x)**2 + (ap_y - point_y)**2)
    return 1 / (distance + 1)


def visualize_initial_and_final(classroom_width, classroom_length, initial_population, final_population):
    plt.figure(figsize=(15, 6))

    for i, (x, y) in enumerate(initial_population):
        plt.text(x, y, str(i + 1), color='black',
                 fontsize=8, ha='center', va='center')
        plt.scatter(*zip(*initial_population), color='red',
                    marker='o', label='Initial Position of Wi-Fi')

    for i, (x, y) in enumerate(final_population):
        plt.text(x, y, str(i + 1), color='black',
                 fontsize=8, ha='center', va='center')
        plt.scatter(*zip(*final_population), color='blue',
                    marker='o', label='Final Position of Wi-Fi')

    plt.xlabel('Classroom Width (m)')
    plt.ylabel('Classroom Length (m)')
    plt.title('Initial and Final Distribution of Wi-Fi Access Points')
    plt.legend()
    plt.show()


def visualize_dynamic_changes(classroom_width, classroom_length, population, fitness_scores):
    for generation in range(generations):
        plt.figure(figsize=(15, 6))

        plt.subplot(1, 2, 1)
        ap_placements = population[generation]
        x = np.linspace(0, classroom_width, 100)
        y = np.linspace(0, classroom_length, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        for ap_x, ap_y in ap_placements:
            Z += calculate_signal_strength(ap_x, ap_y, X, Y)
        plt.pcolormesh(X, Y, Z, shading='auto', cmap='viridis')
        plt.colorbar(label='Сила на сигнала')
        for i, (x, y) in enumerate(ap_placements):
            plt.text(x, y, str(i + 1), color='black',
                     fontsize=8, ha='center', va='center')
        plt.scatter(*zip(*ap_placements), color='red', marker='o',
                    label='Разпределение на точките за достъп')
        plt.xlabel('Ширина на учебна зала (м)')
        plt.ylabel('Дължина на учебна зала (м)')
        plt.title(
            f'Сила на Wi-Fi сигнала и разпределение на точките за достъп (Поколение {generation + 1})')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(range(1, generation + 2),
                 fitness_scores[:generation + 1], marker='o')
        plt.xlabel('Поколение')
        plt.ylabel('Резултат от фитнеса')
        plt.title('Резултат от фитнеса за различните поколения')

        plt.tight_layout()
        plt.show()


# Optimization loop of the genetic algorithm
for generation in range(generations):
    # Evaluate the fitness of each individual in the population
    fitness_scores = []
    for ap_x, ap_y in population[generation]:
        coverage = 0
        for point_x in range(classroom_width):
            for point_y in range(classroom_length):
                coverage += calculate_signal_strength(
                    ap_x, ap_y, point_x, point_y)
        fitness_scores.append(coverage)

    # Save the best solution identified by the highest fitness score
    if max(fitness_scores) > best_fitness:
        best_solution = population[generation][fitness_scores.index(
            max(fitness_scores))]
        best_fitness = max(fitness_scores)

    # Save all fitness scores
    all_fitness_scores.append(max(fitness_scores))

    # Select parents based on fitness scores with probabilities proportional to fitness
    selected_parents = random.choices(
        population[generation], weights=fitness_scores, k=population_size)

    # Generate offspring via crossover between two parents and apply mutation
    offspring = []
    for _ in range(population_size):
        parent1, parent2 = random.sample(selected_parents, 2)
        crossover_x = random.uniform(parent1[0], parent2[0])
        crossover_y = random.uniform(parent1[1], parent2[1])
        offspring.append((crossover_x, crossover_y))

    # Apply mutation
    for i in range(len(offspring)):
        if random.random() < mutation_rate:
            offspring[i] = (random.uniform(0, classroom_width),
                            random.uniform(0, classroom_length))

    # Replace the old population with the new one
    population.append(offspring)


visualize_initial_and_final(
    classroom_width, classroom_length, initial_population, best_solution)