import numpy as np
import pandas as pd
import time
import os
from benchmarks.SS import solve_stepping_stone 
from benchmarks.ballas import solve_balas_hammer_fast
from benchmarks.NW import solve_north_west_corner

def generate_data(size):
    costs = np.random.randint(1, 101, (size, size)).astype(np.float64)
    Pi = np.random.randint(10, 100, size).astype(np.float64)
    Cj = np.random.randint(10, 100, size).astype(np.float64)
    diff = np.sum(Pi) - np.sum(Cj)
    Cj[-1] += diff 
    return costs, Pi, Cj

def run_benchmarks():
    sizes = [10, 40, 100, 400, 1000, 4000, 10000]
    iterations = 100

    for s in sizes:
        filename = f"benchmarks_{s}x{s}.csv"
        results = []
        
        start_iter = 0
        if os.path.exists(filename):
            df_old = pd.read_csv(filename)
            if len(df_old) >= iterations:
                print(f"✅ {filename} déjà complet. Passage au suivant.")
                continue
            start_iter = len(df_old)
            results = df_old.to_dict('records')

        print(f"\n🚀 Lancement Taille {s}x{s} ({start_iter} -> {iterations})")

        for i in range(start_iter, iterations):
            costs, Pi, Cj = generate_data(s)
            
            # 1. NORTHWEST
            t0 = time.perf_counter()
            alloc_nw = solve_north_west_corner(s, s, Pi, Cj)
            t_nw = time.perf_counter() - t0
            
            # 2. BALAS HAMMER
            t0 = time.perf_counter()
            alloc_bh = solve_balas_hammer_fast(costs, Pi, Cj)
            t_bh = time.perf_counter() - t0
            
            # 3. SS (Northwest)
            t_ss_nw = 0
            t0 = time.perf_counter()
            solve_stepping_stone(s, s, costs, alloc_nw, verbose=False)
            t_ss_nw = time.perf_counter() - t0
            
            t0 = time.perf_counter()
            solve_stepping_stone(s, s, costs, alloc_bh, verbose=False)
            t_ss_bh = time.perf_counter() - t0
            
            res = {
                "Iteration": i + 1,
                "Northwest_Time": t_nw,
                "Balas_Hammer_Time": t_bh,
                "SS_NorthWest_Time": t_ss_nw,
                "SS_BallasHammer_Time": t_ss_bh,
                "Total_NorthWest_Time": t_nw + t_ss_nw,
                "Total_BallasHammer_Time": t_bh + t_ss_bh
            }
            results.append(res)
            
            if (i+1) % 5 == 0:
                print(f"   Iter {i+1}/100 terminée...")
                pd.DataFrame(results).to_csv(filename, index=False)

        pd.DataFrame(results).to_csv(filename, index=False)
        print(f"💾 {filename} sauvegardé.")

run_benchmarks()