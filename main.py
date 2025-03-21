from src.Cage import Cage
from src.Chicken import RandomChicken
from src.utils import calculate_avg_adj_list, visualize_graph
import random
import numpy as np

height = 12
width = 10
n_chicken = 5

chickens = [RandomChicken(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(n_chicken)]
cage = Cage(width=width, height=height, chickens=chickens, food_positions=[(0, 2), (0, 3)], water_positions=[(9, 1)], bath_positions=[(5, 9)])
adj_lists =cage.simulate(1000, adj_matrix_interval=5, visual=True)

# average weights over the simulation
avg_adj_list = calculate_avg_adj_list(adj_lists)

visualize_graph(avg_adj_list, cage.all_object_names, min_weight=0.1)
