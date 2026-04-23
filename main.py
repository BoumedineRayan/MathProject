import numpy as np
import os
import re

# Imports de tes modules personnalisés
from northwest import solve_north_west_corner
from balas_hammer import solve_balas_hammer
from display_utils import display_all_tables

# Consol display in case of 10 11 12
np.set_printoptions(threshold=np.inf, linewidth=np.inf, suppress=True)

def load_table(file_path):
    """Loading the files"""
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

def run_analysis(file_name, file_path):
    """Executing the Algorithms"""
    n, m, costs, provisions, orders = load_table(file_path)
    
    print(f"\n{'#'*60}")
    print(f" ANALYSE DU FICHIER : {file_name}")
    print(f"{'#'*60}")

    
    print("\nWhich method would you like ?")
    print("1. Coin Nord-Ouest (Simple)")
    print("2. Balas-Hammer (Optimized)")
    methode = input("Your choice : ")

    if methode == "1":
        allocation = solve_north_west_corner(n, m, provisions, orders)
        method_name = "NORD-OUEST"
    else:
        allocation = solve_balas_hammer(n, m, costs, provisions, orders)
        method_name = "BALAS-HAMMER"



    #  total cost 
    total_cost = np.sum(allocation * costs)
    


    #4 tables (Costs, Alloc, Potentials, Marginals)
    display_all_tables(f"{file_name} ({method_name})", n, m, costs, allocation)


    
    print(f"\nCOÛT TOTAL GÉNÉRÉ PAR {method_name} : {total_cost}")


def main():
    directory = "Tables"
    
    if not os.path.exists(directory):
        print(f"Erreur : Le dossier '{directory}' est introuvable.")
        return
    files = sorted([f for f in os.listdir(directory) if f.endswith('.txt')], 
                   key=lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('([0-9]+)', s)])

    while True:
        print(f"\n{'-'*30}")
        print("Hector & Rayan & Tim & Ambroise Project")
        print(f"{'-'*30}")
        for i, f in enumerate(files):
            print(f"{i+1}. {f}")
        print("0.Leave")
        
        choix = input("\n Select table ")
        
        if choix == "0":
            print("Ending session")
            break
        
        try:
            idx = int(choix) - 1
            if 0 <= idx < len(files):
                run_analysis(files[idx], os.path.join(directory, files[idx]))
                input("\npress ENTER to get back to our menue")
            else:
                print("invalid number")
        except ValueError:
            print("Enter a valid number")

if __name__ == "__main__":
    main()