# import math

# def calculate_distance_matrix(coordinates):
#     num_nodes = len(coordinates)
#     distance_matrix = [[0] * num_nodes for _ in range(num_nodes)]

#     for i in range(num_nodes):
#         x1, y1 = coordinates[i]
#         for j in range(num_nodes):
#             x2, y2 = coordinates[j]
#             distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#             distance_matrix[i][j] = distance

#     return distance_matrix


# # Example coordinates
# coordinates = [
#     (0, 0),
#     (1, 1),
#     (2, 0),
#     (1, -1)
# ]

# dist = calculate_distance_matrix(coordinates)
# for row in dist:
#     print(row)
import sys
a = float('inf')

print(sys.maxsize)