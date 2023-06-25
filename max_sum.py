# Using Roulette Wheel selection:

import random


def generate_permutation(arr):
    return random.sample(arr, len(arr))


def generate_population(arr, size):
    population = []
    for i in range(size):
        population.append(generate_permutation(arr))
    return population


def calculate_sum(arr):
    # Circular Implementation
    # sum = abs(arr[0] - arr[-1])
    # Linear Implementation
    sum = 0
    for i in range(1, len(arr)):
        sum += abs(arr[i] - arr[i - 1])
    return sum


def calculate_fitness(population):
    fitness = []
    for i in range(len(population)):
        fitness.append(calculate_sum(population[i]))
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
    point = random.randint(1, len(arr) - 1)
    pos1 = random.randint(0, point)
    pos2 = random.randint(point, len(arr) - 1)

    # Scramble Mutation
    arr2 = arr[pos1:pos2]
    arr2 = arr2[::-1]

    arr = arr[:pos1] + arr2 + arr[pos2:]
    return arr

def bubbleSort(population, fitness):
    for i in range(len(fitness)):
        for j in range(len(fitness) - i - 1):
            if fitness[j] < fitness[j + 1]:
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


# Driver code
# arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# arr = [7, 60, 113, 166, 219, 272, 325, 378, 431, 484, 537, 590, 643, 696, 749, 802, 855, 908, 961, 1014, 1067, 1120, 1173, 1226, 1279, 1332, 1385, 1438, 1491, 1544, 1597, 1650, 1703, 1756, 1809, 1862, 1915, 1968, 2021, 2074, 2127, 2180, 2233, 2286, 2339, 2392, 2445, 2498, 2551, 2604, 2657, 2710, 2763, 2816, 2869, 2922, 2975, 3028, 3081, 3134, 3187, 3240, 3293, 3346, 3399, 3452, 3505, 3558, 3611, 3664, 3717, 3770, 3823, 3876, 3929, 3982, 4035, 4088, 4141, 4194, 4247, 4300, 4353, 4406, 4459, 4512, 4565, 4618, 4671, 4724, 4777, 4830, 4883, 4936, 4989, 5042, 5095, 5148, 5201, 5254, 5307, 5360, 5413, 5466, 5519, 5572, 5625, 5678, 5731, 5784, 5837, 5890, 5943, 5996, 6049, 6102, 6155, 6208, 6261, 6314, 6367, 6420, 6473, 6526, 6579, 6632, 6685, 6738, 6791, 6844, 6897, 6950, 7003, 7056, 7109, 7162, 7215, 7268, 7321, 7374, 7427, 7480, 7533, 7586, 7639, 7692, 7745, 7798, 7851, 7904, 7957, 8010, 8063, 8116, 8169, 8222, 8275, 8328, 8381, 8434, 8487, 8540, 8593, 8646, 8699, 8752, 8805, 8858, 8911, 8964, 9017, 9070, 9123, 9176, 9229, 9282, 9335, 9388, 9441, 9494, 9547, 9600, 9653, 9706, 9759, 9812, 9865, 9918, 9971, 10024, 10077, 10130, 10183, 10236, 10289, 10342, 10395, 10448, 10501, 10554, 10607, 10660, 10713, 10766, 10819, 10872, 10925, 10978, 11031, 11084, 11137, 11190, 11243, 11296, 11349, 11402, 11455, 11508, 11561, 11614, 11667, 11720, 11773, 11826, 11879, 11932, 11985, 12038, 12091, 12144, 12197, 12250, 12303, 12356, 12409, 12462, 12515, 12568, 12621, 12674, 12727, 12780, 12833, 12886, 12939, 12992, 13045, 13098, 13151, 13204, 13257, 13310, 13363, 13416, 13469, 13522, 13575, 13628, 13681, 13734, 13787, 13840, 13893, 13946, 13999,
#             14052, 14105, 14158, 14211, 14264, 14317, 14370, 14423, 14476, 14529, 14582, 14635, 14688, 14741, 14794, 14847, 14900, 14953, 15006, 15059, 15112, 15165, 15218, 15271, 15324, 15377, 15430, 15483, 15536, 15589, 15642, 15695, 15748, 15801, 15854, 15907, 15960, 16013, 16066, 16119, 16172, 16225, 16278, 16331, 16384, 16437, 16490, 16543, 16596, 16649, 16702, 16755, 16808, 16861, 16914, 16967, 17020, 17073, 17126, 17179, 17232, 17285, 17338, 17391, 17444, 17497, 17550, 17603, 17656, 17709, 17762, 17815, 17868, 17921, 17974, 18027, 18080, 18133, 18186, 18239, 18292, 18345, 18398, 18451, 18504, 18557, 18610, 18663, 18716, 18769, 18822, 18875, 18928, 18981, 19034, 19087, 19140, 19193, 19246, 19299, 19352, 19405, 19458, 19511, 19564, 19617, 19670, 19723, 19776, 19829, 19882, 19935, 19988, 20041, 20094, 20147, 20200, 20253, 20306, 20359, 20412, 20465, 20518, 20571, 20624, 20677, 20730, 20783, 20836, 20889, 20942, 20995, 21048, 21101, 21154, 21207, 21260, 21313, 21366, 21419, 21472, 21525, 21578, 21631, 21684, 21737, 21790, 21843, 21896, 21949, 22002, 22055, 22108, 22161, 22214, 22267, 22320, 22373, 22426, 22479, 22532, 22585, 22638, 22691, 22744, 22797, 22850, 22903, 22956, 23009, 23062, 23115, 23168, 23221, 23274, 23327, 23380, 23433, 23486, 23539, 23592, 23645, 23698, 23751, 23804, 23857, 23910, 23963, 24016, 24069, 24122, 24175, 24228, 24281, 24334, 24387, 24440, 24493, 24546, 24599, 24652, 24705, 24758, 24811, 24864, 24917, 24970, 25023, 25076, 25129, 25182, 25235, 25288, 25341, 25394, 25447, 25500, 25553, 25606, 25659, 25712, 25765, 25818, 25871, 25924, 25977, 26030, 26083, 26136, 26189, 26242, 26295, 26348, 26401, 26454]
arr = [11, 100, 189, 278, 367, 456, 545, 634, 723, 812, 901, 990, 1079, 1168, 1257, 1346, 1435, 1524, 1613, 1702, 1791, 1880, 1969, 2058, 2147, 2236, 2325, 2414, 2503, 2592, 2681, 2770, 2859, 2948, 3037, 3126, 3215, 3304, 3393, 3482, 3571, 3660, 3749, 3838, 3927, 4016, 4105, 4194, 4283, 4372, 4461, 4550, 4639, 4728, 4817, 4906, 4995, 5084, 5173, 5262, 5351, 5440, 5529, 5618, 5707, 5796, 5885, 5974, 6063, 6152, 6241, 6330, 6419, 6508, 6597, 6686, 6775, 6864, 6953, 7042, 7131, 7220, 7309, 7398, 7487, 7576, 7665, 7754, 7843, 7932, 8021, 8110, 8199, 8288, 8377, 8466, 8555, 8644, 8733, 8822]

"""
arr = []
a = 1
while(a):
    n = int(input("Enter element of array: "))
    arr.append(n)
    a = int(input("Enter 0 to stop or 1 to continue adding elements: "))
"""

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
    print("Fitness: ", max(fitness))
    # print("Fitness: ", fitness)
    print("Population: ", len(population))

    # In case of repetions
    if prev != max(fitness):
        prev = max(fitness)
        generation_count += 1
        continue
    else:
        # If all elements in the fitness array are same: reached local maxima
        for k in range(25):
            new_population, new_fitness = parentSelection(population, fitness)

            # Survival Function:
            population, fitness = survivalSelection(
                new_population + population, new_fitness + fitness
            )
        if prev == max(fitness):
            break

max_sum = max(fitness)
print("Max Value: ", max_sum)
# print("Array for max value: ", population[fitness.index(max_sum)])
