import numpy as np
import os
import re
from northwest import solve_north_west_corner
from balas_hammer import solve_balas_hammer

np.set_printoptions(threshold=np.inf, linewidth=np.inf, suppress=True)

def load_table(file_path):
    with open(file_path, 'r') as f:
        data = f.read().split()
    n, m = int(data[0]), int(data[1])
    cursor = 2
    costs, provisions = [], []
    for i in range(n):
        costs.append([int(x) for x in data[cursor : cursor + m]])
        provisions.append(int(data[cursor + m]))
        cursor += (m + 1)
    orders = [int(x) for x in data[cursor : cursor + m]]
    return n, m, np.array(costs), provisions, orders

def display_results(name, n, m, costs, provisions, orders):
    # Calculs
    alloc_nw = solve_north_west_corner(n, m, provisions, orders)
    alloc_bh = solve_balas_hammer(n, m, costs, provisions, orders)
    
    print(f"\n{'='*50}")
    print(f" RÉSULTATS POUR : {name}")
    print(f"{'='*50}")
    
    print("\n[1] MATRICE DES COÛTS (INPUT)")
    print(costs)
    
    print(f"\n[2] NORD-OUEST (Coût: {np.sum(alloc_nw * costs)})")
    print(alloc_nw)
    
    print(f"\n[3] BALAS-HAMMER (Coût: {np.sum(alloc_bh * costs)})")
    print(alloc_bh)

def main():
    directory = "Tables"
    if not os.path.exists(directory):
        print("Dossier 'Tables' introuvable.")
        return

    # Tri naturel des fichiers
    files = sorted([f for f in os.listdir(directory) if f.endswith('.txt')], 
                   key=lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('([0-9]+)', s)])

    while True:
        print("\n--- INTERFACE DE SÉLECTION ---")
        for i, f in enumerate(files):
            print(f"{i+1}. {f}")
        print("0. Quitter")
        
        choix = input("\nChoisissez un tableau (numéro) : ")
        
        if choix == "0":
            break
        
        try:
            idx = int(choix) - 1
            if 0 <= idx < len(files):
                file_path = os.path.join(directory, files[idx])
                n, m, costs, prov, ords = load_table(file_path)
                display_results(files[idx], n, m, costs, prov, ords)
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre.")

if __name__ == "__main__":
    main()