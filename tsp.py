from sys import maxsize
from math import sqrt
import time

start = time.process_time()


def tsp(mask, pos):
    if visited == mask:
        return dist[pos][0], [1]

    ans = maxsize
    path = []
    for i in range(1, node):
        if mask[i] == 0 and i != pos:
            mask[i] = 1
            cost, temp_path = tsp(mask, i)
            temp_cost = dist[pos][i] + cost
            if temp_cost < ans:
                ans = temp_cost
                path = [i + 1] + temp_path
            mask[i] = 0

    return ans, path


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
    # [99.0, 83.0],
    # [73.0, 79.0],
    # [72.0, 91.0],
    # [37.0, 94.0],
    # [6.0, 106.0],
    # [3.0, 97.0],
    # [21.0, 82.0],
    # [33.0, 67.0],
    # [4.0, 66.0],
    # [3.0, 42.0],
    # [27.0, 33.0],
    # [52.0, 41.0],
    # [57.0, 59.0],
    # [58.0, 66.0],
    # [88.0, 65.0],
    # [99.0, 67.0],
    # [95.0, 55.0],
    # [89.0, 55.0],
    # [83.0, 38.0],
    # [85.0, 25.0],
    # [104.0, 35.0],
    # [112.0, 37.0],
    # [112.0, 24.0],
    # [113.0, 13.0],
    # [125.0, 30.0],
    # [135.0, 32.0],
    # [147.0, 18.0],
    # [147.5, 36.0],
    # [154.5, 45.0],
    # [157.0, 54.0],
    # [158.0, 61.0],
    # [172.0, 82.0],
]

node = len(coordinates)
visited = [1 for i in range(node)]
dist = calculate_distance_matrix(coordinates)
mask = [0 for i in range(node)]
mask[0] = 1
cost, path = tsp(mask, 0)
path = [1] + path

end = time.process_time()

print("Cost: ", cost, "\nPath: ", path)
print("Time: ", end - start)
