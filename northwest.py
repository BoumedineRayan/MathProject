import numpy as np

def solve_north_west_corner(n, m, provisions, orders):
    allocation = np.zeros((n, m))
    i, j = 0, 0
    supply = list(provisions)
    demand = list(orders)
    
    while i < n and j < m:
        quantity = min(supply[i], demand[j])
        allocation[i][j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity
        if supply[i] == 0:
            i += 1
        else:
            j += 1
    return allocation