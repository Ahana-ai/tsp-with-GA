import networkx as nx
import matplotlib.pyplot as plt

# Define the coordinates of nodes
coordinates = {
    'A': (0, 0),
    'B': (1, 1),
    'C': (2, 0),
    'D': (1, -1)
}

# Define the modified distance matrix with asymmetric weights
distance_matrix = [
    [0, 1, 2, 2],
    [3, 0, 1, 2],
    [2, 1, 0, 1],
    [4, 2, 1, 0]
]

# Create an empty directed graph
G = nx.DiGraph()

# Add nodes with their coordinates to the graph
for node, (x, y) in coordinates.items():
    G.add_node(node, pos=(x, y))

# Add directed edges with weights from the modified distance matrix
for i in range(len(distance_matrix)):
    for j in range(len(distance_matrix[i])):
        if i != j:
            weight = distance_matrix[i][j]
            G.add_edge(list(coordinates.keys())[i], list(coordinates.keys())[j], weight=weight)

# Get the positions from node attributes
# pos = nx.get_node_attributes(G, 'pos')

# Draw the graph with node labels and edge weights
nx.draw_spring(G, with_labels=True, node_color='lightblue', node_size=500, font_size=12, font_color='black', arrows=True)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G,  edge_labels=edge_labels)
plt.show()
