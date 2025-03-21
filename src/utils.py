import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as mpatches  # For adding legend

def normalize_adj_matrix(adj_matrix: np.array):
    # Normalize the adjacency matrix
    # so that the sum of each row is 1
    row_sums = adj_matrix.sum(axis=1)
    row_sums[row_sums == 0] = 1  # Avoid division by zero
    adj_matrix = adj_matrix / row_sums[:, np.newaxis]
     
    return adj_matrix

def calculate_avg_adj_list(adj_lists):
    adj_lists = np.array(adj_lists)
    return np.mean(adj_lists, axis=0)


def visualize_graph(adj_matrix, all_object_names, min_weight=None):
    """
    Visualizes a weighted graph from an adjacency matrix, coloring edges by weight.
    
    Parameters:
    adj_matrix (np.ndarray): 2D NumPy array representing the adjacency matrix.
    min_weight (float, optional): Minimum edge weight to be included in the graph.
    """

    node_types = {}

    for idx, obj in enumerate(all_object_names):
        obj_type = obj.split('_')[0]
        
        node_types[idx] = obj_type

    G = nx.Graph()
    num_nodes = adj_matrix.shape[0]
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):  # Assuming an undirected graph
            weight = adj_matrix[i, j]
            if weight != 0 and (min_weight is None or weight >= min_weight):
                G.add_edge(i, j, weight=weight)
    
    #G.add_edge(1, 2, weight=1)# for testing
    pos = nx.spring_layout(G) 
    

    weights = [G[u][v]['weight'] for u,v in G.edges()]

    #edge styling
    cmap = plt.cm.coolwarm
    edge_colors = [cmap(weight) for weight in weights]
    thickness = [(.3+weight)*5 for weight in weights]

    # node styling
    type_colors = {
        'chicken': 'red',
        'food': 'green',
        'water': 'blue',
        'bath': 'orange'
    }
    
    node_color_list = [type_colors.get(node_types.get(idx, 'path'), 'grey') for idx in G.nodes()]
    node_names = {i: all_object_names[i] for i in G.nodes()}
    print(node_names)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_color_list, edge_color=edge_colors, 
            node_size=500, font_size=7, labels=node_names,
            width = thickness)
    
    # Draw edge labels
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    ax = plt.gca()
    sm = plt.cm.ScalarMappable(cmap=cmap)
    sm.set_array([])  # Empty array, just to create the colorbar
    cbar = plt.colorbar(sm, ax=ax)  # Pass the axis explicitly to colorbar
    cbar.set_label('Edge Weight (Low -> High)')

    legend_labels = {
        'chicken': 'red',
        'food': 'green',
        'water': 'blue',
        'bath': 'orange'
    }

    handles = [mpatches.Patch(color=color, label=label) for label, color in legend_labels.items()]
    ax.legend(handles=handles, title='Node Types')
    plt.show()
