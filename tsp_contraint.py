import random, matplotlib.pyplot as plt, networkx as nx, sys
from math import sqrt


def generate_path_permutation(arr):
    start = arr[0]
    return [start] + random.sample(arr[1:], len(arr) - 1)


def generate_population(arr, size):
    population = []
    for i in range(size):
        population.append(generate_path_permutation(arr))
    return population


def calculate_path_cost(arr):
    # Linear Implementation
    sum = 0
    for i in range(len(arr) - 1):
        node1 = arr[i]
        node2 = arr[i + 1]
        if ([node1, node2]) in blockage:
            sum += sys.maxsize
        else:
            sum += dist[node1][node2]
    if ([arr[0], arr[-1]]) in blockage:
        sum += sys.maxsize
    else:
        sum += dist[arr[-1]][arr[0]]
    if sum == 0:
        # returns infinity for invalid paths
        return sys.maxsize
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
            nodes_list[i],
            nodes_list[i + 1],
            weight=dist[nodes_list[i]][nodes_list[i + 1]],
        )
    G.add_edge(
        nodes_list[-1], nodes_list[0], weight=dist[nodes_list[-1]][nodes_list[0]]
    )

    # Define the positions for the nodes
    pos = {i: (coordinates[i][0], coordinates[i][1]) for i in nodes_list}

    node_colors = ["red" if node == start else "green" for node in nodes_list]

    # Plotting the graph
    nx.draw(G, pos, with_labels=True, arrows=True, node_color=node_colors)
    # for path in blockage:
    #     nx.draw_networkx_edges(G, pos, edgelist=[path], edge_color="red")
    plt.show()


# Driver code -------->
# node = int(input("Node: "))
# start = int(input("Start Node: "))
node = 42
start = 0
arr = [i for i in range(node)]
arr.remove(start)
arr = [start] + arr

# Example coordinates
# coordinates = [
#     [5, 8],
#     [2, 6],
#     [9, 4],
#     [3, 1],
#     [7, 2],
#     [6, 9],
#     [8, 3],
#     [1, 7],
#     [4, 5],
#     [2, 3],
#     [6, 8],
#     [9, 1],
#     [7, 4],
#     [5, 6],
#     [3, 9],
#     [8, 2],
#     [4, 7],
#     [1, 5],
#     [3, 2],
#     [6, 4],
#     [9, 7],
#     [8, 5],
#     [5, 3],
#     [2, 9],
#     [7, 6],
#     [4, 1],
#     [6, 2],
#     [3, 8],
#     [1, 9],
#     [9, 5],
#     [8, 7],
#     [5, 1],
#     [7, 3],
#     [4, 6],
#     [2, 8],
#     [1, 4],
#     [3, 7],
#     [9, 6],
#     [6, 5],
#     [8, 1],
#     [2, 4],
#     [7, 9],
#     [5, 2],
#     [4, 3],
#     [1, 8],
#     [9, 3],
#     [3, 5],
#     [6, 7],
#     [4, 9],
#     [8, 6],
# ]

coordinates = [
    [174.0, 87.0],
    [170.0, 85.0],
    [166.0, 88.0],
    [133.0, 73.0],
    [140.0, 70.0],
    [142.0, 55.0],
    [126.0, 53.0],
    [125.0, 60.0],
    [119.0, 68.0],
    [117.0, 74.0],
    [99.0, 83.0],
    [73.0, 79.0],
    [72.0, 91.0],
    [37.0, 94.0],
    [6.0, 106.0],
    [3.0, 97.0],
    [21.0, 82.0],
    [33.0, 67.0],
    [4.0, 66.0],
    [3.0, 42.0],
    [27.0, 33.0],
    [52.0, 41.0],
    [57.0, 59.0],
    [58.0, 66.0],
    [88.0, 65.0],
    [99.0, 67.0],
    [95.0, 55.0],
    [89.0, 55.0],
    [83.0, 38.0],
    [85.0, 25.0],
    [104.0, 35.0],
    [112.0, 37.0],
    [112.0, 24.0],
    [113.0, 13.0],
    [125.0, 30.0],
    [135.0, 32.0],
    [147.0, 18.0],
    [147.5, 36.0],
    [154.5, 45.0],
    [157.0, 54.0],
    [158.0, 61.0],
    [172.0, 82.0],
]


# blockage = [[9, 1], [7, 4], [1, 8], [5, 3], [2, 9], [3, 7]]
# blockage = [
#     [8, 1],
#     [2, 6],
#     [7, 4],
#     [1, 5],
#     [3, 9],
#     [6, 2],
#     [5, 8],
#     [2, 3],
#     [9, 1],
#     [7, 2],
#     [3, 1],
#     [4, 7],
#     [6, 5],
#     [9, 7],
#     [8, 2],
#     [3, 2],
#     [4, 1],
#     [5, 6],
#     [7, 6],
#     [9, 3],
#     [2, 9],
#     [1, 4],
#     [5, 3],
#     [3, 7],
#     [8, 5],
#     [6, 8],
#     [1, 7],
#     [4, 9],
#     [9, 4],
#     [8, 6],
#     [7, 3],
#     [6, 4],
#     [4, 3],
#     [2, 8],
#     [3, 8],
#     [5, 2],
#     [1, 8],
#     [7, 9],
#     [4, 6],
#     [9, 6],
# ]
blockage = [
    [20, 28],
    [6, 35],
    [8, 33],
    [2, 17],
    [16, 19],
    [11, 22],
    [14, 32],
    [1, 10],
    [3, 19],
    [3, 14],
    [31, 37],
    [7, 12],
    [13, 30],
    [36, 41],
    [16, 29],
    [2, 36],
    [7, 15],
    [23, 41],
    [8, 31],
    [5, 41],
    [21, 27],
    [18, 28],
    [9, 27],
    [6, 22],
    [12, 39],
    [10, 37],
    [5, 38],
    [15, 25],
    [4, 26],
    [1, 25],
    [4, 30],
    [26, 33],
    [18, 21],
    [9, 23],
    [39, 40],
    [32, 35],
    [17, 34],
    [11, 24],
    [20, 24],
    [13, 38],
    [34, 40],
    [2, 1],
    [1, 2],
    [3, 4],
    [6, 7],
    [23, 22],
    [14, 15],
    [15, 14],
    [1, 41],
    [2, 41],
    [41, 1],
    [30, 31],
    [16, 13],
    [27, 26],
    [40, 41],
    [0, 41],
    [41, 0],
    [1, 0],
    [0, 1],
    [4, 3],
    [3, 4],
    [26, 27],
    [2, 0],
    [41, 2],
    [0, 2],
    [12, 10],
    [10, 12],
    [11, 12],
    [12, 11],
    [14, 16],
    [16, 14],
]


dist = calculate_distance_matrix(coordinates)

# dist = [[0, 10, 15, 20], [5, 0, 9, 10], [6, 13, 0, 12], [8, 8, 9, 0]]

# print("Distance: ", dist)

pop_size = int(input("Population size: "))
population = generate_population(arr, pop_size)
fitness = calculate_fitness(population)
# print("Initial Population: ", population)
# print("Initial Fitness: ", fitness)

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

    print("Generation: ", generation_count)
    print("Fitness: ", min(fitness))

    # In case of repetions
    if prev != min(fitness):
        prev = min(fitness)
        generation_count += 1
        continue
    else:
        # If all elements in the fitness array are same: reached local maxima
        for k in range(50):
            new_population, new_fitness = parentSelection(population, fitness)

            # Survival Function:
            population, fitness = survivalSelection(
                new_population + population, new_fitness + fitness
            )

            generation_count += 1
            print("Generation: ", generation_count)
            print("Fitness: ", min(fitness))
        if prev == min(fitness):
            break

min_sum = min(fitness)
list = population[fitness.index(min_sum)]
print("Min Path: ", list, "\nMin Sum: ", min_sum)

show_graph(list)
