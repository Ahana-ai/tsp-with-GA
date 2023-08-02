import random, matplotlib.pyplot as plt, networkx as nx, sys, time
from math import sqrt

start = time.process_time()


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


def one_point_crossover(arr):
    # self-crossover: one point crossover
    point = random.randint(1, len(arr) - 1)
    arr1 = arr[:point]
    arr2 = arr[point:]
    arr2 = arr2[::-1]

    arr = arr1 + arr2

    return arr


def uniform_crossover(parent1, parent2):
    size = len(parent1)

    point = random.randint(1, size - 1)

    child1 = parent1[:point]

    for gene in parent2:
        if gene not in child1:
            child1.append(gene)

    # Create child2 by copying genes from parent2 until the crossover point
    child2 = parent2[:point]

    # Fill child2 with genes from parent1 that are not already present
    for gene in parent1:
        if gene not in child2:
            child2.append(gene)

    return child1, child2


def order_crossover(parent1, parent2):
    size = len(parent1)
    # Randomly select two crossover points
    point1 = random.randint(0, size - 1)
    point2 = random.randint(0, size - 1)

    # Make sure the two points are distinct
    while point1 == point2:
        point2 = random.randint(0, size - 1)

    # Determine the start and end points of the segment to be copied
    start = min(point1, point2)
    end = max(point1, point2)

    # Create a copy of parent1 and fill the segment with its genes
    offspring = parent1[:]
    offspring[start : end + 1] = parent1[start : end + 1]

    # Fill the remaining positions in the offspring with genes from parent2
    for gene in parent2:
        if gene not in offspring[start : end + 1]:
            for i in range(size):
                if offspring[i] is None:
                    offspring[i] = gene
                    break

    return offspring


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
    # return rouletteWheel


def parentSelection(population, fitness):
    new_population = rouletteWheel(population, fitness)
    for i in range(len(new_population)):
        # child = one_point_crossover(new_population[i])
        child = new_population[i]
        # child1, child2 = uniform_crossover(new_population[i], new_population[i-1])
        # child = order_crossover(new_population[i], new_population[i - 1])

        if random.random() > 0.2:
            child = one_point_crossover(new_population[i])
            child = mutation(child)
            new_population[i] = child
        else:
            child = one_point_crossover(new_population[i])
            new_population[i] = child
        # child1 = mutation(child1)
        # child2 = mutation(child2)

        # new_population[i], new_population[i-1] = child1, child2

    # roulette_wheel = rouletteWheel(population, fitness)
    # new_population = []
    # # Parent 1 ----------------->
    # # Rotating the wheel ------>
    # for i in range(len(population)):
    #     for j in range(len(population)):
    #         if roulette_wheel[j] < random.random():
    #             parent1 = population[j]
    #         else:
    #             parent2 = population[j]

    #     child1, child2 = uniform_crossover(parent1, parent2)

    #     if random.random() > 0.2:
    #         child1 = mutation(child1)
    #         child2 = mutation(child2)

    #     new_population.append(child1)
    #     new_population.append(child2)

    # new_population, new_fitness = bubbleSort(new_population, calculate_fitness(new_population))


    new_fitness = calculate_fitness(new_population)
    return new_population, new_fitness


def survivalSelection(new_population, new_fitness):
    population = rouletteWheel(new_population, new_fitness)
    population = population[0 : len(population) // 2]
    fitness = calculate_fitness(population)

    # roulette_wheel = rouletteWheel(new_population, new_fitness)
    # population = []
    # # Rotating the wheel ------>
    # for i in range(len(new_population)):
    #     for j in range(len(new_population)):
    #         if roulette_wheel[j] < random.random():
    #             population.append(new_population[j])
    #             break

    # population = population[0 : len(new_population) // 2]
    # fitness = calculate_fitness(population)

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
    for path in blockage:
        nx.draw_networkx_edges(G, pos, edgelist=[path], edge_color="red")
    plt.show()


# Driver code -------->
# node = int(input("Node: "))
# start = int(input("Start Node: "))


# Example coordinates
coordinates = [
    [607455, 953773],
    [845467, 854635],
    [585545, 672185],
    [19913, 39467],
    [500785, 699650],
    [161032, 876069],
    [819775, 765484],
    [695697, 229314],
    [77707, 804296],
    [580407, 611640],
    [194514, 823649],
    [773629, 823948],
    [251036, 989851],
    [677640, 64245],
    [236311, 263133],
    [850442, 316934],
    [498653, 843431],
    [12549, 550548],
    [165419, 921219],
    [339384, 445646],
    [371465, 251158],
    [985973, 71267],
    [996845, 837956],
    [343295, 80483],
    [211709, 137651],
    [508066, 889011],
    [7791, 98239],
    [256671, 626801],
    [609637, 87161],
    [156705, 282808],
    [383985, 106277],
    [260988, 110318],
    [726830, 378455],
    [398625, 341569],
    [256706, 336506],
    [627861, 736378],
    [802828, 431915],
    [627538, 755490],
    [681394, 394016],
    [97309, 648889],
    [913818, 528302],
    [468094, 272773],
    [931498, 902175],
    [345028, 30107],
    [226983, 707141],
    [868701, 559846],
    [4129, 401717],
    [310474, 360690],
    [979851, 898811],
    [254703, 358084],
    [542609, 905508],
    [190874, 809032],
    [495032, 667837],
    [525915, 392542],
    [342271, 243655],
    [768805, 917776],
    [497378, 480115],
    [690138, 421430],
    [929947, 795289],
    [791310, 195245],
    [527677, 924673],
    [689517, 869930],
    [437138, 930613],
    [620362, 358943],
    [878425, 909056],
    [2427, 578001],
    [353673, 583045],
    [894277, 793378],
    [493573, 530435],
    [778007, 655612],
    [976051, 347800],
    [771553, 249460],
    [218865, 336710],
    [492074, 313391],
    [643155, 359321],
    [334062, 803881],
    [300665, 430360],
    [245591, 829463],
    [692477, 856440],
    [103481, 102984],
    [560325, 602291],
    [838877, 188831],
    [703811, 179243],
    [421600, 455552],
    [435808, 126293],
    [253056, 43334],
    [403962, 538419],
    [77101, 677342],
    [212968, 563458],
    [497100, 341526],
    [104464, 94205],
    [14985, 67828],
    [315387, 381697],
    [114466, 127966],
    [109261, 621073],
    [884556, 320770],
    [440850, 823126],
    [56192, 369167],
    [857033, 605606],
    [810140, 704199],
    [329159, 998095],
    [443618, 932329],
    [843335, 917130],
    [695307, 723465],
    [977258, 169560],
    [71227, 557652],
    [628005, 148962],
    [228025, 617280],
    [197591, 387063],
    [347247, 629608],
    [524610, 298136],
    [355499, 841540],
    [882091, 38049],
    [505826, 532172],
    [706272, 229021],
    [819561, 544867],
    [203103, 636432],
    [798626, 334587],
    [691986, 936169],
    [955738, 768744],
    [238897, 365181],
    [758982, 387375],
    [768495, 867060],
    [976983, 423086],
    [565651, 851739],
    [862866, 20419],
    [773502, 676364],
    [975547, 669111],
    [955717, 739579],
    [256283, 877031],
    [759482, 737221],
    [1513, 928050],
    [818462, 373093],
    [421249, 448413],
    [938989, 914983],
    [655691, 651379],
    [694140, 294087],
    [859865, 203818],
    [802738, 754793],
    [766389, 671384],
    [494763, 477252],
    [581332, 781113],
    [735881, 500545],
    [61077, 876644],
    [210607, 479493],
    [902986, 757283],
    [964006, 591639],
    [231588, 453569],
    [910132, 677399],
    [577165, 632638],
    [351689, 928593],
    [218799, 457073],
    [25081, 99310],
    [745838, 52522],
    [872543, 614194],
    [67313, 651948],
    [67384, 656856],
    [915517, 352129],
    [67248, 765754],
    [954182, 39657],
    [987769, 158605],
    [417344, 709812],
    [963073, 624319],
    [819549, 534731],
    [478110, 585137],
    [394745, 128799],
    [591174, 74006],
    [513052, 297606],
    [434961, 698098],
    [710513, 645228],
    [541197, 78678],
    [164832, 961652],
    [33686, 591038],
    [134444, 587148],
    [309893, 822959],
    [823532, 239897],
    [338777, 254774],
    [861880, 109243],
    [39786, 356365],
    [683813, 465039],
    [379209, 480395],
    [475083, 216729],
    [318970, 190320],
    [483179, 458838],
    [214569, 646276],
    [826592, 139705],
    [721102, 130050],
    [131347, 800248],
    [155731, 796154],
    [986499, 265528],
    [625700, 745333],
    [978526, 413029],
    [101847, 8688],
    [669594, 353590],
    [395581, 192412],
    [718869, 406692],
    [531708, 681729],
    [342595, 638389],
    [398570, 958783],
    [290302, 463003],
    [535024, 317989],
    [574993, 614130],
    [436141, 218160],
    [849117, 227269],
    [928362, 102226],
    [566767, 399917],
    [832290, 266350],
    [101621, 934280],
    [112905, 86684],
    [136301, 24634],
    [122248, 119031],
    [532992, 907550],
    [855490, 146984],
    [491244, 107208],
    [55083, 296569],
    [590810, 547531],
    [721435, 163409],
    [480455, 37941],
    [998659, 483650],
    [45367, 269308],
    [470438, 563804],
    [26956, 211522],
    [134772, 348518],
    [530533, 574552],
    [741117, 211519],
    [346085, 392288],
    [731593, 363516],
    [604919, 736362],
    [504318, 178318],
    [185590, 320798],
    [763926, 844773],
    [614048, 871474],
    [997635, 287757],
    [94445, 271351],
    [211273, 142474],
    [396082, 978131],
    [826494, 566351],
    [862375, 540735],
    [15224, 851378],
    [404875, 166986],
    [677097, 13065],
    [897056, 484719],
    [540719, 993225],
    [379269, 871924],
    [37704, 604726],
    [983638, 792765],
    [500915, 626721],
    [929241, 78590],
    [617280, 689726],
    [535724, 201599],
    [143391, 401485],
    [932, 859040],
    [594135, 605291],
    [462954, 480367],
    [241504, 207308],
    [408393, 893093],
    [591802, 703542],
    [850453, 275586],
    [977497, 985211],
    [356097, 733714],
    [365677, 522363],
    [773588, 305792],
    [197216, 202870],
    [820690, 434244],
    [318121, 930181],
    [235181, 70133],
    [930346, 280544],
    [483342, 482073],
    [965816, 811852],
    [29837, 144585],
    [64, 729239],
    [949509, 267086],
    [17068, 39006],
    [824322, 266090],
    [197557, 763021],
    [492334, 558731],
    [171634, 816814],
    [840410, 425958],
    [476619, 956503],
    [756210, 752723],
    [322163, 97609],
    [692331, 927513],
    [793960, 787700],
    [381370, 114015],
    [243185, 23895],
    [11633, 596879],
    [747907, 317631],
    [683339, 284032],
    [861667, 106719],
    [427610, 498391],
    [474476, 20073],
    [361407, 596926],
    [74461, 859130],
    [123230, 78793],
    [86474, 618686],
    [976169, 423454],
    [392874, 720093],
    [241882, 521773],
    [775532, 288904],
    [903866, 527932],
    [187680, 271594],
    [381455, 660561],
    [193681, 872159],
    [924307, 449844],
    [495223, 940925],
    [695277, 738877],
    [971757, 697089],
    [891042, 515033],
    [607819, 752490],
    [638452, 366381],
    [555231, 807260],
    [650788, 946145],
    [515168, 774493],
    [727469, 46338],
    [598607, 631062],
    [490410, 937227],
    [321278, 983804],
    [372896, 321532],
    [727757, 474701],
    [74930, 403914],
    [431895, 417577],
    [532449, 612324],
    [341766, 399040],
    [547180, 255902],
    [915571, 981521],
    [348669, 984648],
    [342763, 354969],
    [391556, 613865],
    [908101, 325997],
    [351456, 805054],
    [223986, 970451],
    [402910, 240614],
    [716754, 564272],
    [565575, 920717],
    [167897, 315115],
    [406869, 299214],
    [495924, 801379],
    [939738, 704997],
    [266753, 936750],
    [227371, 367479],
    [445583, 797137],
    [610619, 444307],
    [726494, 829306],
    [223782, 672789],
    [600373, 402993],
    [420623, 369110],
    [337041, 406253],
    [99495, 204432],
    [42336, 763303],
    [973385, 348660],
    [350391, 986988],
    [361847, 160726],
    [252578, 395427],
]

node = len(coordinates)
start = 0
arr = [i for i in range(node)]
arr.remove(start)
arr = [start] + arr

blockage = []


dist = calculate_distance_matrix(coordinates)

# print("Distance: ", dist)

pop_size = int(input("Population size: "))
# pop_size = (node//50)*100
print("Population size: ", pop_size)
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
        for k in range(15):
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

end = time.process_time()
print("Time: ", end - start)


show_graph(list)
