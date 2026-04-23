import numpy as np

def calculate_potentials_and_marginals(n, m, costs, allocation):
    """Calcule les vecteurs U, V et la matrice des coûts marginaux."""
    u = [None] * n
    v = [None] * m
    u[0] = 0  
    for _ in range(n + m):
        for i in range(n):
            for j in range(m):
                if allocation[i][j] > 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = costs[i][j] - u[i]
                    elif v[j] is not None and u[i] is None:
                        u[i] = costs[i][j] - v[j]

    # Remplacement of None by 0
    u = [x if x is not None else 0 for x in u]
    v = [x if x is not None else 0 for x in v]

    # Marginal cost
    marginal_matrix = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            marginal_matrix[i][j] = costs[i][j] - (u[i] + v[j])
            
    return u, v, marginal_matrix

def display_all_tables(name, n, m, costs, allocation):
    """Affiche les 4 tables réglementaires demandées par le projet."""
    u, v, marginals = calculate_potentials_and_marginals(n, m, costs, allocation)
    
    print(f"\n{'-'*20} ANALYSE DÉTAILLÉE : {name} {'-'*20}")
    
    print("\n[1] COST MATRIX (c_ij)")
    print(costs)
    
    print("\n[2] TRANSPORTATION PROPOSAL (x_ij)")
    print(allocation)
    
    print("\n[3] POTENTIAL COSTS")
    print(f"Vecteur U (Lignes)   : {u}")
    print(f"Vecteur V (Colonnes) : {v}")
    
    print("\n[4] MARGINAL COSTS TABLE (Delta_ij)")
    print(marginals)
    
    # Test d'optimalité
    is_optimal = np.all(marginals >= -1e-9) 
    if is_optimal:
        print("\n>>> RÉSULTAT : La proposition est OPTIMALE.")
    else:
        print("\n>>> RÉSULTAT : La proposition n'est pas optimale (présence de coûts négatifs).")