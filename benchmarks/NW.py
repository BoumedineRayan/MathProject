import numpy as np

def solve_north_west_corner(n, m, provisions, orders):
    supply = provisions.copy().astype(np.float64)
    demand = orders.copy().astype(np.float64)
    allocation = np.zeros((n, m), dtype=np.float64)
    
    i, j = 0, 0
    while i < n and j < m:
        quantity = min(supply[i], demand[j])
        allocation[i, j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity
        
        if supply[i] == 0 and i < n - 1:
            i += 1
        elif demand[j] == 0 and j < m - 1:
            j += 1
        else:
            i += 1
            j += 1
    
    # Sécurité pour la dégénérescence : ajouter un epsilon très petit
    # pour que Stepping Stone voit n+m-1 cellules
    mask = allocation > 0
    if np.count_nonzero(mask) < (n + m - 1):
        for r in range(n):
            for c in range(m):
                if allocation[r, c] == 0:
                    allocation[r, c] = 1e-15 # Zéro "logique" pour la base
                    if np.count_nonzero(allocation > 0) == (n + m - 1):
                        return allocation
    return allocation