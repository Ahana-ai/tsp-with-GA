from sys import maxsize

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
                path = [i+1] + temp_path
            mask[i] = 0

    return ans, path

node = 4
visited = [1 for i in range(node)] 
dist = [[0, 10, 15, 20], [5, 0, 9, 10], [6, 13, 0, 12], [8, 8, 9, 0]]
mask = [0 for i in range(node)]
mask[0] = 1
cost, path = tsp(mask, 0)
path = [1] + path

print("Cost: ", cost, "\nPath: ", path)