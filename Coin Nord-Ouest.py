import numpy as np
import os

def solve_north_west_corner(n, m, provisions, orders):
    """Apply the Nord-Ouest coin to find the initial solution and the cost"""
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

def process_file(file_path):
    """Lit un fichier de données et affiche les résultats du calcul."""
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return

    with open(file_path, 'r') as f:
        data = f.read().split()
    
    if not data:
        return
    
    n = int(data[0])
    m = int(data[1])
    
    # Lecture des C et P
    cursor = 2
    costs = []
    provisions = []
    for i in range(n):
        row_costs = [int(x) for x in data[cursor : cursor + m]]
        costs.append(row_costs)
        provisions.append(int(data[cursor + m]))
        cursor += (m + 1)
    
    orders = [int(x) for x in data[cursor : cursor + m]]
    costs_np = np.array(costs)
    
    #la solution initiale
    allocation = solve_north_west_corner(n, m, provisions, orders)
    
    #coût total
    total_cost = np.sum(allocation * costs_np)
    
    # Affichage propre
    print(f"{'='*40}")
    print(f"FICHIER : {os.path.basename(file_path)}")
    print(f"{'='*40}")
    print(f"Dimensions : {n}x{m}")
    print(f"Coût total (Nord-Ouest) : {total_cost}")
    print(f"Matrice d'allocation :\n{allocation}\n")



# Le print du truc
directory = "Tables"

if os.path.exists(directory):
    files = sorted([f for f in os.listdir(directory) if f.endswith('.txt')])
    
    if len(files) == 0:
        print(f"Aucun fichier .txt trouvé dans le dossier '{directory}'")
    else:
        for filename in files:
            full_path = os.path.join(directory, filename)
            process_file(full_path)
else:
    print(f"Le dossier '{directory}' n'existe pas. Vérifie le nom du répertoire.")