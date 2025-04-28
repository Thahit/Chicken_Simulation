from src.Cage import Cage
from src.Chicken import RandomChicken
from src.utils import calculate_avg_adj_list, visualize_graph, read_all_weeks, create_graph_from_adj_matrix
import random
import numpy as np

height = 12
width = 10
n_chicken = 20
analyze_only_chicken= False

chickens = [RandomChicken(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(n_chicken)]
cage = Cage(width=width, height=height, chickens=chickens, food_positions=[(0, 2), (0, 3)], water_positions=[(9, 1)], bath_positions=[(5, 9)])
adj_lists =cage.simulate_visual(1000, adj_matrix_interval=5, visual=True)

# average weights over the simulation
avg_adj_list = calculate_avg_adj_list(adj_lists)
names= cage.all_object_names
#visualize_graph(avg_adj_list, names, min_weight=0.1)


print("analysis")

df = read_all_weeks(adj_lists, week_size=5)

# Call the function with your adjacency matrix and clustering method
create_graph_from_adj_matrix(avg_adj_list,all_object_names=names, 
        clustering_method='louvain', max_size= n_chicken if analyze_only_chicken else None)  # Or 'label_propagation' for another method
