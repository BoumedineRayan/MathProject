import numpy as np
from numba import njit, prange

@njit
def solve_balas_hammer_fast(costs, provisions, orders):
    n, m = costs.shape
    supply = provisions.copy().astype(np.float64)
    demand = orders.copy().astype(np.float64)
    allocation = np.zeros((n, m), dtype=np.float64)
    
    row_active = np.ones(n, dtype=np.bool_)
    col_active = np.ones(m, dtype=np.bool_)

    while np.any(row_active) and np.any(col_active):
        max_penalty = -1.0
        best_idx = -1
        is_row = True

        # Penalités lignes
        for i in range(n):
            if row_active[i]:
                first, second = 1e18, 1e18
                count = 0
                for j in range(m):
                    if col_active[j]:
                        count += 1
                        val = costs[i, j]
                        if val < first:
                            second = first
                            first = val
                        elif val < second:
                            second = val
                penalty = second - first if count > 1 else first
                if penalty > max_penalty:
                    max_penalty, best_idx, is_row = penalty, i, True

        # Penalités colonnes
        for j in range(m):
            if col_active[j]:
                first, second = 1e18, 1e18
                count = 0
                for i in range(n):
                    if row_active[i]:
                        count += 1
                        val = costs[i, j]
                        if val < first:
                            second = first
                            first = val
                        elif val < second:
                            second = val
                penalty = second - first if count > 1 else first
                if penalty > max_penalty:
                    max_penalty, best_idx, is_row = penalty, j, False

        # Allocation
        if is_row:
            i = best_idx
            min_val, j = 1e18, -1
            for jj in range(m):
                if col_active[jj] and costs[i, jj] < min_val:
                    min_val, j = costs[i, jj], jj
        else:
            j = best_idx
            min_val, i = 1e18, -1
            for ii in range(n):
                if row_active[ii] and costs[ii, j] < min_val:
                    min_val, i = costs[ii, j], ii

        q = min(supply[i], demand[j])
        allocation[i, j] = q
        supply[i] -= q
        demand[j] -= q
        if supply[i] <= 1e-9: row_active[i] = False
        if demand[j] <= 1e-9: col_active[j] = False

    return allocation