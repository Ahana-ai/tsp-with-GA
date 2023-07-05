import math
import time

start = time.process_time()


def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_total_distance(route, cities):
    total_distance = 0
    n = len(route)
    for i in range(n):
        city1 = cities[route[i]]
        city2 = cities[route[(i + 1) % n]]
        total_distance += distance(city1, city2)
    return total_distance


def two_opt(route, cities):
    best_route = route
    improved = True
    while improved:
        improved = False
        for i in range(len(route) - 2):
            for j in range(i + 2, len(route)):
                new_route = route[: i + 1] + route[i + 1 : j + 1][::-1] + route[j + 1 :]
                new_distance = calculate_total_distance(new_route, cities)
                if new_distance < calculate_total_distance(best_route, cities):
                    best_route = new_route
                    improved = True
        route = best_route
    return best_route


# City coordinates
cities = [
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

# Initialize the route as a simple ordering of cities
route = [i for i in range(len(cities))]

# Apply the 2-Opt algorithm to find an improved route
new_route = two_opt(route, cities)

end = time.process_time()

# Print the final route and total distance
print("Final Route:", new_route)
print("Total Distance:", calculate_total_distance(new_route, cities))
print("Time:", end - start)
