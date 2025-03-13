import numpy as np

def normalize_adj_matrix(adj_matrix: np.array):
    # Normalize the adjacency matrix
    # so that the sum of each row is 1
    row_sums = adj_matrix.sum(axis=1)
    row_sums[row_sums == 0] = 1  # Avoid division by zero
    adj_matrix = adj_matrix / row_sums[:, np.newaxis]
     
    return adj_matrix