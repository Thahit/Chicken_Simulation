import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches  # For adding legend
import pandas as pd
import community as community_louvain  # For modularity-based community detection
from networkx.algorithms.community import label_propagation_communities  # For other clustering methods


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


def create_graph(adj_matrix, min_weight=None, max_size=None):
    G = nx.Graph()
    num_nodes = adj_matrix.shape[0]
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):  # Assuming an undirected graph
            weight = adj_matrix[i, j]
            if weight != 0 and (min_weight is None or weight >= min_weight):
                G.add_edge(i, j, weight=round(weight, 2))
    return G


def visualize_graph(adj_matrix, all_object_names, min_weight=None, max_size=None):
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

    G = create_graph(adj_matrix, min_weight=min_weight)
    if max_size!= None:# to only take chicken for example
        G = G.subgraph(range(max_size))
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

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_color_list, edge_color=edge_colors, 
            node_size=500, font_size=7, labels=node_names,
            width = thickness)
    
    # Draw edge labels
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels
                                 )
    ax = plt.gca()
    if False:#draw color legend
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


def read_week_adj_data(adj_lists, week=1, week_size=5):
    """
    Averages the adjacency matrices for a given week and returns the averaged matrix.
    
    Parameters:
    adj_lists (list of np.ndarray): List of adjacency matrices.
    week (int): The week number to process (1-based).
    week_size (int): The number of adjacency matrices per week.
    
    Returns:
    np.ndarray: The averaged adjacency matrix for the given week.
    """
    # Calculate the starting and ending indices for the current week
    start_idx = (week - 1) * week_size
    end_idx = start_idx + week_size
    
    # Get the adjacency matrices for the current week
    week_adj_matrices = adj_lists[start_idx:end_idx]
    
    # Calculate the average adjacency matrix for this week
    avg_adj_matrix = calculate_avg_adj_list(week_adj_matrices)
    
    return avg_adj_matrix



def read_all_weeks(adj_lists, week_size=5):
    """
    Processes all the adjacency matrices and averages them by week.
    
    Parameters:
    adj_lists (list of np.ndarray): List of adjacency matrices (one per time step).
    week_size (int): Number of adjacency matrices per week (default is 5).
    
    Returns:
    pd.DataFrame: DataFrame with the averaged adjacency matrix for each week.
    """
    weeks_data = {"names":[],"adj_matr":[]}
    
    for week in range(1, (len(adj_lists) // week_size) + 1):
        avg_adj_matrix = read_week_adj_data(adj_lists, week=week, week_size=week_size)
        #weeks_data.append({'week': f'week-{week}', 'adj_matrix': avg_adj_matrix})
        weeks_data["names"].append(f'week-{week}')
        weeks_data["adj_matr"].append(avg_adj_matrix)
    
    all_weeks_avg = calculate_avg_adj_list(adj_lists)
    weeks_data["names"].append(f'week-all')
    weeks_data["adj_matr"].append(all_weeks_avg)
    df_weeks = pd.DataFrame(weeks_data)
    
    return df_weeks


def create_graph_from_adj_matrix(adj_matrix, clustering_method='louvain',
        all_object_names=None, max_size=None):
    G = create_graph(adj_matrix)
    if max_size!= None:# to only take chicken for example
        G = G.subgraph(range(max_size))
    
    if clustering_method == 'louvain':
        partition = community_louvain.best_partition(G)
        communities = list(partition.values())
    elif clustering_method == 'label_propagation':
        communities = list(label_propagation_communities(G))
    else:
        raise ValueError("Unknown clustering method")

    pos = nx.spring_layout(G)  
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_size=500, cmap=plt.cm.coolwarm, 
                           node_color=communities, alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    if all_object_names != None:
        print(f"{len(all_object_names)=}, {len(G.nodes())=}")
        print(all_object_names)
        node_names = {i: all_object_names[i] for i in G.nodes()}

    nx.draw_networkx_labels(G,pos=pos, labels= node_names if all_object_names!=None else None, font_size=12)
    plt.title(f"Graph with {clustering_method.capitalize()} Clustering")
    plt.show()
