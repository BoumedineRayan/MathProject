import numpy as np
from collections import deque

# Check if graph is degenerate, if so connect it with the cheapest edge
def get_bfs_components(n, m, basis):
    adj = {f"R{i}": [] for i in range(n)}
    adj.update({f"C{j}": [] for j in range(m)})
    
    for r, c in basis:
        adj[f"R{r}"].append(f"C{c}")
        adj[f"C{c}"].append(f"R{r}")
        
    visited = set()
    components = []
    
    for node in adj:
        if node not in visited:
            comp = set()
            q = deque([node])
            while q:
                curr = q.popleft()
                if curr not in visited:
                    visited.add(curr)
                    comp.add(curr)
                    for neighbor in adj[curr]:
                        if neighbor not in visited:
                            q.append(neighbor)
            components.append(comp)
    
    return components

# Check if graph is connected with connected less expensive edge than any other edge
def make_connected(n, m, costs, basis, verbose=True):
    components = get_bfs_components(n, m, basis)
    while len(components) > 1:
        if verbose:
            print(f"Graph not connected {len(components)} subgraphs. Searching for an edge to add...")
        
        c1 = components[0]
        c2 = components[1]
        
        r_nodes_1 = [int(x[1:]) for x in c1 if x.startswith('R')]
        c_nodes_1 = [int(x[1:]) for x in c1 if x.startswith('C')]
        r_nodes_2 = [int(x[1:]) for x in c2 if x.startswith('R')]
        c_nodes_2 = [int(x[1:]) for x in c2 if x.startswith('C')]
        
        best_cost = float('inf')
        best_edge = None
        
        # Test from rows of C1 to columns of C2
        for r in r_nodes_1:
            for c in c_nodes_2:
                if costs[r][c] < best_cost:
                    best_cost = costs[r][c]
                    best_edge = (r, c)
        
        # Test from columns of C1 to rows of C2
        for c in c_nodes_1:
            for r in r_nodes_2:
                if costs[r][c] < best_cost:
                    best_cost = costs[r][c]
                    best_edge = (r, c)
                    
        if best_edge:
            if verbose:
                print(f"Adding an edge of cost {best_cost} to connect the graph: P{best_edge[0]+1} to C{best_edge[1]+1}")
            basis.append(best_edge)
        
        components = get_bfs_components(n, m, basis)

# Get potentials U and V strictly from the basis (avoids bugs related to 0 from degeneracy).
def get_potentials(n, m, costs, basis):
    u = {0: 0}
    v = {}
    changed = True
    while changed:
        changed = False
        for r, c in basis:
            if r in u and c not in v:
                v[c] = costs[r][c] - u[r]
                changed = True
            elif c in v and r not in u:
                u[r] = costs[r][c] - v[c]
                changed = True
    return [u.get(i, 0) for i in range(n)], [v.get(j, 0) for j in range(m)]

# Find cycle using BFS
def find_cycle_bfs(basis, start_r, start_c):
    adj = {}
    for r, c in basis:
        if (r, c) == (start_r, start_c): 
            continue # Ignore the new edge to find the path that connects them
        R_node = f"R{r}"
        C_node = f"C{c}"
        if R_node not in adj: adj[R_node] = []
        if C_node not in adj: adj[C_node] = []
        adj[R_node].append(C_node)
        adj[C_node].append(R_node)
        
    start_node = f"R{start_r}"
    target_node = f"C{start_c}"
    
    q = deque([start_node])
    parent = {start_node: None}
    
    while q:
        curr = q.popleft()
        if curr == target_node:
            break
        for neighbor in adj.get(curr, []):
            if neighbor not in parent:
                parent[neighbor] = curr
                q.append(neighbor)
                
    # Reconstruct the path
    path_nodes = []
    curr = target_node
    while curr is not None:
        path_nodes.append(curr)
        curr = parent[curr]
    path_nodes.reverse() 
    
    # Transform BFS nodes into alternating cells + / -
    cycle = [(start_r, start_c)]
    for i in range(len(path_nodes) - 1):
        u = path_nodes[i]
        v = path_nodes[i+1]
        if u.startswith('R'):
            cycle.append((int(u[1:]), int(v[1:])))
        else:
            cycle.append((int(v[1:]), int(u[1:])))
            
    return cycle

def solve_stepping_stone(n, m, costs, allocation, verbose=True):
    allocation = allocation.copy()
    
    # 1. Extract initial basis
    basis = [(i, j) for i in range(n) for j in range(m) if allocation[i][j] > 0]
    
    iteration = 1
    while True:
        if verbose:
            print(f"\n--- Stepping-Stone Iteration {iteration} ---")
            
        # 2. Make connected and handle degeneracy
        make_connected(n, m, costs, basis, verbose)
        
        # 3. Calculate potentials
        u, v = get_potentials(n, m, costs, basis)
        
        # 4. Identify best marginal cost
        best_marg = 0
        best_cell = None
        
        for i in range(n):
            for j in range(m):
                if (i, j) not in basis:
                    marg = costs[i][j] - (u[i] + v[j])
                    if marg < best_marg:
                        best_marg = marg
                        best_cell = (i, j)
                        
        if best_cell is None:
            if verbose:
                print(">>> Optimal solution found! All marginal costs are >= 0.")
            break
            
        if verbose:
            print(f"Best improving edge: P{best_cell[0]+1}-C{best_cell[1]+1} (Marginal cost: {best_marg})")
            
        # 5. Maximize along the cycle
        basis.append(best_cell)
        cycle = find_cycle_bfs(basis, best_cell[0], best_cell[1])
        
        if verbose:
            print(f"Cycle detected (BFS) : {[(r+1, c+1) for r, c in cycle]}")
            
        # The odd indices in the cycle correspond to the cells with "-"
        minus_cells = [cycle[i] for i in range(1, len(cycle), 2)]
        delta = min(allocation[r][c] for r, c in minus_cells)
        
        if verbose:
            print(f"Maximized transport of: {delta}")
            
        for i, (r, c) in enumerate(cycle):
            if i % 2 == 0:
                allocation[r][c] += delta
            else:
                allocation[r][c] -= delta
                
        # 6. Update the basis (remove ONE edge that fell to 0 to keep the tree connected)
        for r, c in minus_cells:
            if allocation[r][c] == 0:
                basis.remove((r, c))
                if verbose:
                    print(f"Edge removed from basis: P{r+1}-C{c+1}")
                break
                
        iteration += 1
        
    return allocation


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
    

from balas_hammer import solve_balas_hammer

if __name__ == "__main__":

    n, m, costs, provisions, orders = load_table("Tables/Table9.txt")
    allocation = solve_balas_hammer(n, m, costs, provisions, orders)

    solve_stepping_stone(n, m, costs, allocation, verbose=True)