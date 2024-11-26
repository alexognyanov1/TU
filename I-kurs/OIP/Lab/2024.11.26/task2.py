# Description: This script uses a genetic algorithm to optimize the placement of access points in a rectangular room to maximize coverage. It initializes a population of random access point positions, evaluates their fitness based on the area covered, and iteratively improves the positions through selection, crossover, and mutation. The script visualizes the coverage heatmap for the initial and final access point placements, plots the fitness over generations, and animates the changes in access point positions across generations.
# Tags: Genetic Algorithm, Optimization, Access Point Placement, Coverage, Heatmap

import numpy as np
import matplotlib.pyplot as plt
import random

# Parameters
room_width = 7  # Width of the lecture hall
room_height = 5  # Height of the lecture hall
num_access_points = 5  # Number of access points
population_size = 50  # Population size
num_generations = 10  # Number of generations
mutation_rate = 0.1  # Mutation rate (10%)
crossover_rate = 0.7  # Crossover rate


class Individual:
    def __init__(self, positions=None):
        if positions is None:
            # Randomly initialize positions
            self.positions = np.random.rand(
                num_access_points, 2) * [room_width, room_height]
        else:
            self.positions = positions
        self.fitness = 0

    def evaluate_fitness(self):
        # Compute fitness based on coverage
        grid_size = 1  # Grid size for discretization
        x = np.arange(0, room_width, grid_size)
        y = np.arange(0, room_height, grid_size)
        xv, yv = np.meshgrid(x, y)
        grid_points = np.vstack([xv.ravel(), yv.ravel()]).T

        # Coverage radius for each access point
        coverage_radius = 20

        covered = np.zeros(len(grid_points), dtype=bool)
        for ap_pos in self.positions:
            distances = np.linalg.norm(grid_points - ap_pos, axis=1)
            covered = covered | (distances <= coverage_radius)
        # Fitness is the percentage of area covered
        self.fitness = np.sum(covered) / len(covered)


def initialize_population():
    return [Individual() for _ in range(population_size)]


def select_parent(population):
    fitnesses = np.array([ind.fitness for ind in population])
    total_fitness = np.sum(fitnesses)
    probabilities = fitnesses / total_fitness
    return population[np.random.choice(len(population), p=probabilities)]


def crossover(parent1, parent2):
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, num_access_points - 1)
        child1_positions = np.vstack((parent1.positions[:crossover_point],
                                      parent2.positions[crossover_point:]))
        child2_positions = np.vstack((parent2.positions[:crossover_point],
                                      parent1.positions[crossover_point:]))
        return Individual(child1_positions), Individual(child2_positions)
    else:
        # No crossover, return copies of parents
        return Individual(parent1.positions.copy()), Individual(parent2.positions.copy())


def mutate(individual):
    for i in range(num_access_points):
        if random.random() < mutation_rate:
            # Mutate position
            individual.positions[i] = np.random.rand(
                2) * [room_width, room_height]


def genetic_algorithm():
    population = initialize_population()
    # Evaluate initial fitness
    for ind in population:
        ind.evaluate_fitness()
    best_fitnesses = []
    best_individuals = []
    positions_over_generations = []
    positions_over_generations.append(
        [ind.positions.copy() for ind in population])
    for generation in range(num_generations):
        new_population = []
        for _ in range(population_size // 2):
            # Selection
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            # Crossover
            child1, child2 = crossover(parent1, parent2)
            # Mutation
            mutate(child1)
            mutate(child2)
            # Evaluate fitness
            child1.evaluate_fitness()
            child2.evaluate_fitness()
            new_population.extend([child1, child2])
        # Update population
        population = new_population
        # Record best fitness
        best_individual = max(population, key=lambda ind: ind.fitness)
        best_fitnesses.append(best_individual.fitness)
        best_individuals.append(best_individual)
        positions_over_generations.append(
            [ind.positions.copy() for ind in population])
        print(
            f"Generation {generation}, Best Fitness: {best_individual.fitness:.4f}")
    # Return the best individual and positions over generations
    return best_individual, best_fitnesses, best_individuals


def plot_coverage(individual, title='Access Point Coverage Heatmap'):
    plt.figure(figsize=(8, 8))
    plt.title(title)
    plt.xlabel('Width')
    plt.ylabel('Height')

    # Define grid
    grid_resolution = 1  # Adjust grid resolution if needed
    x = np.arange(0, room_width, grid_resolution)
    y = np.arange(0, room_height, grid_resolution)
    xv, yv = np.meshgrid(x, y)
    grid_points = np.vstack([xv.ravel(), yv.ravel()]).T

    # Compute signal strength at each grid point
    signal_strength = np.zeros(len(grid_points))
    attenuation_constant = 20  # Adjust attenuation constant as needed
    for ap_pos in individual.positions:
        distances = np.linalg.norm(grid_points - ap_pos, axis=1)
        # Avoid division by zero
        distances[distances == 0] = 0.1
        # Example signal model: signal decreases exponentially with distance
        signal_strength += np.exp(-distances / attenuation_constant)

    # Reshape signal strength to 2D grid
    signal_strength_grid = signal_strength.reshape(xv.shape)

    # Plot heatmap
    plt.imshow(signal_strength_grid, extent=(0, room_width, 0,
               room_height), origin='lower', cmap='hot', alpha=0.8)
    plt.colorbar(label='Signal Strength')
    # Plot access point positions
    plt.scatter(individual.positions[:, 0], individual.positions[:,
                1], c='blue', s=100, label='Access Points')
    plt.legend()
    plt.show()


def plot_fitness_over_generations(fitnesses):
    plt.figure()
    plt.plot(fitnesses)
    plt.title('Fitness over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()


def plot_positions_over_generations(best_individuals):
    plt.figure(figsize=(8, 8))
    plt.xlim(0, room_width)
    plt.ylim(0, room_height)
    plt.title('Access Point Positions Over Generations')
    plt.xlabel('Width')
    plt.ylabel('Height')
    for i, ind in enumerate(best_individuals):
        # Plot every 10 generations
        if i % 10 == 0 or i == len(best_individuals) - 1:
            plt.scatter(ind.positions[:, 0],
                        ind.positions[:, 1], label=f'Gen {i}')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # Run genetic algorithm
    best_individual, best_fitnesses, best_individuals = genetic_algorithm()
    # Visualize initial placement
    initial_individual = best_individuals[0]
    plot_coverage(initial_individual,
                  title='Initial Access Point Coverage Heatmap')
    # Visualize final placement
    plot_coverage(best_individual,
                  title='Optimized Access Point Coverage Heatmap')
    # Plot fitness over generations
    plot_fitness_over_generations(best_fitnesses)
    # Visualize changes in points across generations
    plot_positions_over_generations(best_individuals)