import numpy as np

def solve_balas_hammer_fast(costs, provisions, orders):
    costs = np.array(costs, dtype=float)
    supply = np.array(provisions, dtype=float)
    demand = np.array(orders, dtype=float)
    n, m = costs.shape
    allocation = np.zeros((n, m))

    # 1. Pré-tri des indices pour éviter de chercher le min à chaque itération
    # On stocke les indices des colonnes triées par coût pour chaque ligne
    row_sorted_indices = [list(np.argsort(costs[i, :])) for i in range(n)]
    # On stocke les indices des lignes triées par coût pour chaque colonne
    col_sorted_indices = [list(np.argsort(costs[:, j])) for j in range(m)]

    row_active = np.ones(n, dtype=bool)
    col_active = np.ones(m, dtype=bool)

    while np.any(row_active) and np.any(col_active):
        max_penalty = -1
        best_type = None
        best_idx = -1

        # --- CALCUL DES PÉNALITÉS ---
        
        # Pour chaque ligne active
        for i in range(n):
            if not row_active[i]: continue
            # Nettoyer les indices des colonnes qui ne sont plus actives
            while row_sorted_indices[i] and not col_active[row_sorted_indices[i][0]]:
                row_sorted_indices[i].pop(0)
            
            indices = row_sorted_indices[i]
            if len(indices) >= 2:
                p = costs[i, indices[1]] - costs[i, indices[0]]
            elif len(indices) == 1:
                p = costs[i, indices[0]]
            else:
                p = -1
            
            if p > max_penalty:
                max_penalty, best_type, best_idx = p, 'row', i

        # Pour chaque colonne active
        for j in range(m):
            if not col_active[j]: continue
            # Nettoyer les indices des lignes qui ne sont plus actives
            while col_sorted_indices[j] and not row_active[col_sorted_indices[j][0]]:
                col_sorted_indices[j].pop(0)
            
            indices = col_sorted_indices[j]
            if len(indices) >= 2:
                p = costs[indices[1], j] - costs[indices[0], j]
            elif len(indices) == 1:
                p = costs[indices[0], j]
            else:
                p = -1
                
            if p > max_penalty:
                max_penalty, best_type, best_idx = p, 'col', j

        if best_idx == -1: break

        # --- ALLOCATION ---
        
        if best_type == 'row':
            i = best_idx
            j = row_sorted_indices[i][0]
        else:
            j = best_idx
            i = col_sorted_indices[j][0]

        quantity = min(supply[i], demand[j])
        allocation[i, j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity

        if supply[i] <= 1e-9: # Utilisation d'un epsilon pour les flottants
            row_active[i] = False
        if demand[j] <= 1e-9:
            col_active[j] = False

    return allocation