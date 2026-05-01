import numpy as np
import time
import csv
from ballas import solve_balas_hammer_fast
from northwest import solve_north_west_corner



def generate_random_matrix(size: int) -> np.ndarray:
    return np.random.randint(0, 101, (size, size))


def calculate_provisions_and_orders(matrix: np.ndarray) -> tuple:
    Pi = np.sum(matrix, axis=1)
    Cj = np.sum(matrix, axis=0)
    return Pi, Cj


def calculate_time_complexity_northwest(size: int, provisions: np.ndarray, orders: np.ndarray) -> float:
    '''Calculate the time complexity of the Northwest Corner method.
    
    Args:        
        size (int): The size of the squared matrix.
        provisions (list): A list containing the provisions for each row.
        orders (list): A list containing the orders for each column.
    Returns:
        float: The time taken to execute the Northwest Corner method in seconds.
    '''
    time_start = time.perf_counter()
    solve_north_west_corner(size, size, provisions, orders)
    time_end = time.perf_counter()
    return time_end - time_start

def calculate_time_complexity_balas_hammer(size: int, costs: np.ndarray, provisions: np.ndarray, orders: np.ndarray) -> float:
    '''Calculate the time complexity of the Balas-Hammer method.
    
    Args:        
        size (int): The size of the squared matrix.
        costs (list): A squared matrix containing the costs for each cell.
        provisions (list): A list containing the provisions for each row.
        orders (list): A list containing the orders for each column.
    Returns:
        float: The time taken to execute the Balas-Hammer method in seconds.
    '''
    time_start = time.perf_counter()
    testo = solve_balas_hammer_fast(costs, provisions, orders)
    time_end = time.perf_counter()
    return time_end - time_start
    
    
def main():
    EXPORT_TO_CSV = False  

    delta_NW_list = []
    delta_BH_list = []
    sizeOfMatrix = int(input("Enter the size of the squared matrix: "))
    filename = f"benchmarks_{sizeOfMatrix}x{sizeOfMatrix}.csv"
    f = None
    writer = None
    
    if EXPORT_TO_CSV:
        f = open(filename, mode='w', newline='')
        writer = csv.writer(f)
        writer.writerow(["Iteration", "Northwest_Time", "Balas_Hammer_Time"])

    try:
        for i in range(100):
            matrix_A = generate_random_matrix(sizeOfMatrix)
            Pi, Cj = calculate_provisions_and_orders(generate_random_matrix(sizeOfMatrix))
            
            delta_NW = calculate_time_complexity_northwest(sizeOfMatrix, Pi, Cj)
            print(f"Iteration {i+1} - NW: {delta_NW}s")
            
            delta_BH = calculate_time_complexity_balas_hammer(sizeOfMatrix, matrix_A, Pi, Cj)
            print(f"Iteration {i+1} - BH: {delta_BH}s")
            
            delta_NW_list.append(delta_NW)
            delta_BH_list.append(delta_BH)
            
            if EXPORT_TO_CSV and writer:
                writer.writerow([i + 1, delta_NW, delta_BH])
                
        print("-" * 30)
        avg_nw = np.mean(delta_NW_list)
        avg_bh = np.mean(delta_BH_list)
        print(f"Moyenne NW: {avg_nw:.6f} s")        
        print(f"Moyenne BH: {avg_bh:.6f} s")
        
        if EXPORT_TO_CSV:
            print(f"Données enregistrées dans : {filename}")

    finally:
        if f:
            f.close()
main()