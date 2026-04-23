import numpy as np

def solve_balas_hammer(n, m, costs, provisions, orders):
    allocation = np.zeros((n, m))
    supply = list(provisions)
    demand = list(orders)
    costs_copy = costs.astype(float).copy()
    
    while sum(supply) > 0 and sum(demand) > 0:
        penalties = []
        # Lignes
        for i in range(n):
            if supply[i] > 0:
                row = sorted([costs_copy[i][j] for j in range(m) if demand[j] > 0])
                p = row[1] - row[0] if len(row) > 1 else (row[0] if len(row) == 1 else 0)
                penalties.append((p, 'row', i))
        # Colonnes
        for j in range(m):
            if demand[j] > 0:
                col = sorted([costs_copy[i][j] for i in range(n) if supply[i] > 0])
                p = col[1] - col[0] if len(col) > 1 else (col[0] if len(col) == 1 else 0)
                penalties.append((p, 'col', j))
        
        if not penalties: break
        penalties.sort(key=lambda x: x[0], reverse=True)
        _, type_p, idx = penalties[0]
        
        if type_p == 'row':
            best_j = min([(costs_copy[idx][j], j) for j in range(m) if demand[j] > 0])[1]
            best_i = idx
        else:
            best_i = min([(costs_copy[i][idx], i) for i in range(n) if supply[i] > 0])[1]
            best_j = idx
            
        val = min(supply[best_i], demand[best_j])
        allocation[best_i][best_j] = val
        supply[best_i] -= val
        demand[best_j] -= val
        
    return allocation