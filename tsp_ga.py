import random, matplotlib.pyplot as plt, numpy as np, networkx as nx
from math import sqrt


def generate_path_permutation(arr):
    start = arr[0]
    return [start] + random.sample(arr[1:], len(arr) - 1)


def generate_population(arr, size):
    population = []
    for i in range(size):
        population.append(generate_path_permutation(arr))
    return population


def calculate_path_cost(arr):  # 0 1 2 3
    # Linear Implementation
    sum = 0
    for i in range(len(arr) - 1):
        sum += dist[arr[i]][arr[i + 1]]
    sum += dist[arr[i + 1]][arr[0]]
    if sum == 0:
        return float("inf")
    return sum


def calculate_fitness(population):
    fitness = []
    for i in range(len(population)):
        fitness.append(calculate_path_cost(population[i]))
    return fitness


def crossover(arr):
    # self-crossover: one point crossover
    point = random.randint(1, len(arr) - 1)
    arr1 = arr[:point]
    arr2 = arr[point:]
    arr2 = arr2[::-1]

    arr = arr1 + arr2

    return arr


def mutation(arr):
    point = random.randint(2, len(arr) - 1)
    pos1 = random.randint(1, point)
    pos2 = random.randint(point, len(arr) - 1)

    # Scramble Mutation
    arr2 = arr[pos1:pos2]
    arr2 = arr2[::-1]

    arr = arr[:pos1] + arr2 + arr[pos2:]
    return arr


def bubbleSort(population, fitness):
    for i in range(len(fitness)):
        for j in range(len(fitness) - i - 1):
            if fitness[j] > fitness[j + 1]:
                # Swap elements
                fitness[j], fitness[j + 1] = fitness[j + 1], fitness[j]
                population[j], population[j + 1] = population[j + 1], population[j]
    return population, fitness


# Roulette Wheel Selection During Parent Selection
def rouletteWheel(population, fitness):
    # Bubble sort the fitness and population arrays
    population, fitness = bubbleSort(population, fitness)

    # Implementation of Roulette Wheel
    totalSum = sum(fitness)

    rouletteWheel = [0]

    # Making of rouletteWheel Array
    for i in range(len(population)):
        rouletteWheel.append(rouletteWheel[i] + fitness[i] / totalSum)

    parent = []
    # Rotating the wheel ------>
    for i in range(len(population)):
        for j in range(len(population)):
            if rouletteWheel[j] < random.random():
                parent.append(population[j])
                break

    return parent


def parentSelection(population, fitness):
    new_population = rouletteWheel(population, fitness)
    for i in range(len(new_population)):
        child = crossover(new_population[i])

        if random.random() > 0.2:
            child = mutation(child)

        new_population[i] = child

    new_fitness = calculate_fitness(new_population)
    return new_population, new_fitness


def survivalSelection(new_population, new_fitness):
    population = rouletteWheel(new_population, new_fitness)
    population = population[0 : len(population) // 2]
    fitness = calculate_fitness(population)
    return population, fitness


def calculate_distance_matrix(coordinates):
    num_nodes = len(coordinates)
    distance_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for i in range(num_nodes):
        x1, y1 = coordinates[i]
        for j in range(num_nodes):
            x2, y2 = coordinates[j]
            distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            distance_matrix[i][j] = distance

    return distance_matrix


def show_graph(nodes_list):
    # Initiating a Directed Graph
    G = nx.DiGraph()

    # Adding edges to the graph
    for i in range(len(nodes_list) - 1):
        G.add_edge(
            nodes_list[i] + 1,
            nodes_list[i + 1] + 1,
            weight=dist[nodes_list[i]][nodes_list[i + 1]],
        )
    G.add_edge(nodes_list[-1] + 1, nodes_list[0] + 1, weight=dist[-1][0])

    # Define the positions for the nodes
    pos = {1: (0, 0), 2: (1, 1), 3: (2, 0), 4: (1, -1)}

    # Plotting the graph
    nx.draw(G, pos, with_labels=True, arrows=True)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()


# Driver code -------->
# node = int(input("Node: "))
# start = int(input("Start Node: "))
node = 4
start = 0
arr = [i for i in range(node)]
arr.remove(start)
arr = [start] + arr

# Example coordinates
coordinates = [(0, 0), (1, 1), (2, 0), (1, -1)]

dist = calculate_distance_matrix(coordinates)

# dist = [[0, 10, 15, 20], [5, 0, 9, 10], [6, 13, 0, 12], [8, 8, 9, 0]]

print("Distance: ", dist)

pop_size = int(input("Population size: "))
population = generate_population(arr, pop_size)
fitness = calculate_fitness(population)
print("Initial Population: ", population)
print("Initial Fitness: ", fitness)

# To check the previous generation max fitness value
prev = 0
generation_count = 1

while True:
    # Crossover & Mutation
    new_population, new_fitness = parentSelection(population, fitness)

    # Survival Function:
    population, fitness = survivalSelection(
        new_population + population, new_fitness + fitness
    )

    # print("Generation: ", generation_count)
    # print("Fitness: ", 1/min(fitness))

    # In case of repetions
    if prev != min(fitness):
        prev = min(fitness)
        generation_count += 1
        continue
    else:
        # If all elements in the fitness array are same: reached local maxima
        for k in range(15):
            new_population, new_fitness = parentSelection(population, fitness)

            # Survival Function:
            population, fitness = survivalSelection(
                new_population + population, new_fitness + fitness
            )

            generation_count += 1
            # print("Generation: ", generation_count)
            # print("Fitness: ", 1/min(fitness))
        if prev == min(fitness):
            break

min_sum = min(fitness)
list = population[fitness.index(min_sum)]
print("Min Path: ", list, "\nMin Sum: ", min_sum)

show_graph(list)
