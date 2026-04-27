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
    delta_NW_list = []
    delta_BH_list = []
    sizeOfMatrix = int(input("Enter the size of the squared matrix: "))
    filename = f"benchmarks_{sizeOfMatrix}x{sizeOfMatrix}.csv"
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Iteration", "Northwest_Time", "Balas_Hammer_Time"])
    
    
        for i in range(100):
            matrix_A = generate_random_matrix(sizeOfMatrix)
            Pi, Cj = calculate_provisions_and_orders(generate_random_matrix(sizeOfMatrix))
            delta_NW = calculate_time_complexity_northwest(sizeOfMatrix, Pi, Cj)
            print(f"Time taken to execute the Northwest Corner method for a matrix of size {sizeOfMatrix}x{sizeOfMatrix}: {delta_NW} seconds")
            delta_BH = calculate_time_complexity_balas_hammer(sizeOfMatrix, matrix_A, Pi, Cj)
            print(f"Time taken to execute the Balas-Hammer method for a matrix of size {sizeOfMatrix}x{sizeOfMatrix}: {delta_BH} seconds")
            delta_NW_list.append(delta_NW)
            delta_BH_list.append(delta_BH)
            writer.writerow([i + 1, delta_NW, delta_BH])
        print("-" * 30)
        avg_nw = np.mean(delta_NW_list)
        avg_bh = np.mean(delta_BH_list)
        print(f"Moyenne NW: {avg_nw:.6f} s")
        print(f"Moyenne BH: {avg_bh:.6f} s")
        print(f"Données enregistrées dans : {filename}")
main()