import numpy as np
from numba import njit
from collections import deque

@njit
def get_potentials_numba(n, m, costs, basis_indices):
    # Initialisation explicite en float64 pour éviter les conflits de types
    u = np.full(n, np.nan, dtype=np.float64)
    v = np.full(m, np.nan, dtype=np.float64)
    u[0] = 0.0
    
    # Propagation des potentiels sur n+m itérations maximum
    for _ in range(n + m):
        changed = False
        for k in range(basis_indices.shape[0]):
            r = basis_indices[k, 0]
            c = basis_indices[k, 1]
            
            # Vérification si U est connu mais pas V
            if not np.isnan(u[r]) and np.isnan(v[c]):
                v[c] = costs[r, c] - u[r]
                changed = True
            # Vérification si V est connu mais pas U
            elif not np.isnan(v[c]) and np.isnan(u[r]):
                u[r] = costs[r, c] - v[c]
                changed = True
        if not changed:
            break
            
    # Nettoyage des NaN pour les composants isolés (dégénérescence)
    for i in range(n):
        if np.isnan(u[i]): u[i] = 0.0
    for j in range(m):
        if np.isnan(v[j]): v[j] = 0.0
    return u, v

def solve_stepping_stone(n, m, costs, allocation, verbose=False):
    costs = np.ascontiguousarray(costs, dtype=np.float64)
    allocation = np.ascontiguousarray(allocation, dtype=np.float64)
    
    # CRITIQUE : S'assurer que la base a assez d'éléments (n + m - 1)
    # Si manque des cellules (dégénérescence), on ajoute des zéros infinitésimaux
    basis_indices = np.argwhere(allocation > 1e-12).astype(np.int64)
    
    iteration = 1
    while iteration < 1000: # Sécurité contre boucle infinie
        u, v = get_potentials_numba(n, m, costs, basis_indices)
        marginal_costs = costs - (u.reshape(-1, 1) + v)
        
        # Masquage manuel des cellules de la base
        for k in range(len(basis_indices)):
            marginal_costs[basis_indices[k,0], basis_indices[k,1]] = 0
            
        best_marg = np.min(marginal_costs)
        if best_marg >= -1e-8: break
            
        idx = np.argmin(marginal_costs)
        start_node = (int(idx // m), int(idx % m))
        
        cycle = find_cycle_fast(n, m, basis_indices, start_node)
        
        # PROTECTION : Si le cycle est vide, on sort pour éviter le crash min()
        if not cycle or len(cycle) < 4:
            break

        minus_cells = [cycle[i] for i in range(1, len(cycle), 2)]
        
        # Calcul de delta avec sécurité
        delta = min(allocation[r, c] for r, c in minus_cells)
        
        for i, (r, c) in enumerate(cycle):
            if i % 2 == 0: allocation[r, c] += delta
            else:          allocation[r, c] -= delta
            
        # Mise à jour de la base
        new_basis = [tuple(x) for x in basis_indices]
        new_basis.append(start_node)
        
        removed = False
        for r, c in minus_cells:
            if allocation[r, c] <= 1e-12 and not removed:
                new_basis.remove((r, c))
                removed = True
        
        basis_indices = np.array(new_basis, dtype=np.int64)
        iteration += 1
        
    return allocation

def find_cycle_fast(n, m, basis_indices, start_node):
    # On construit un graphe biparti (Lignes et Colonnes)
    adj = {}
    nodes = set()
    
    # Ajouter la cellule de départ et les cellules de la base
    all_cells = list(basis_indices) + [np.array(start_node)]
    
    for r, c in all_cells:
        r_node, c_node = int(r), int(c + n)
        if r_node not in adj: adj[r_node] = []
        if c_node not in adj: adj[c_node] = []
        adj[r_node].append(c_node)
        adj[c_node].append(r_node)

    # BFS pour trouver le chemin le plus court entre start_r et start_c_node
    start_r, start_c = int(start_node[0]), int(start_node[1] + n)
    queue = deque([(start_r, [start_r])])
    visited = {start_r}
    
    while queue:
        curr, path = queue.popleft()
        for neighbor in adj[curr]:
            if neighbor == start_c and len(path) >= 3:
                # Cycle trouvé ! On convertit le chemin de nodes en cellules (r, c)
                full_path = path + [start_c]
                cycle_cells = []
                for i in range(0, len(full_path), 2):
                    cycle_cells.append((full_path[i], full_path[i+1] - n))
                    if i+2 < len(full_path):
                        cycle_cells.append((full_path[i+2], full_path[i+1] - n))
                return cycle_cells
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return []