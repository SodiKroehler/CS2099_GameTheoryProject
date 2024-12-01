from ortools.linear_solver import pywraplp

def get_u_d_j_t(j,t):
    # u_d = c_t * 1 + (1 - c_t) * 0
    #ie constant reward for all attacker types, and no penalty
    pass

def get_u_a_j_t(j, t):
    pass

def solve_sse():
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Number of targets
    n = len(k)

    # Variables
    d = [solver.NumVar(-solver.infinity(), solver.infinity(), f'd[{j}]') for j in range(n)]
    c = [solver.NumVar(0, 1, f'c[{t}]') for t in range(T)]
    a = [[solver.BoolVar(f'a[{j}][{t}]') for t in range(T)] for j in range(n)]
    dlambda = solver.NumVar(-solver.infinity(), solver.infinity(), 'dlambda')  # Maximize d_lambda

    # Objective: Maximize d_lambda
    solver.Maximize(dlambda)

    # Constraints
    for j in range(n):
        for t in range(T):
            # (2) d_j - Ud(j, c_t, t) <= M * (1 - a_t_j)
            solver.Add(d[j] - Ud(j, c[t], t) <= 1e5 * (1 - a[j][t]))

            # (3) 0 <= k_j - Ua(j, c_t, t) <= M * (1 - a_t_j)
            solver.Add(0 <= k[j] - Ua(j, c[t], t))
            solver.Add(k[j] - Ua(j, c[t], t) <= 1e5 * (1 - a[j][t]))

    # (4) d_j = d_star[j] for j < lambda_idx
    for j in range(lambda_idx):
        solver.Add(d[j] == d_star[j])

    # (5) d_j >= b_j for all j
    for j in range(n):
        solver.Add(d[j] >= b[j])

    # (6) a_t_j ∈ {0, 1}
    # Automatically enforced in OR-Tools with BoolVar.

    # (7) Sum_t(a_t_j) = 1 for each j
    for j in range(n):
        solver.Add(solver.Sum(a[j][t] for t in range(T)) == 1)

    # (8) 0 <= c_t <= 1
    # Automatically enforced in OR-Tools by defining c_t in [0, 1].

    # (9) Sum_t(c_t) <= m
    solver.Add(solver.Sum(c[t] for t in range(T)) <= m)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found!")
        print(f"dlambda = {dlambda.solution_value()}")
        print("d values:", [d[j].solution_value() for j in range(n)])
        print("c values:", [c[t].solution_value() for t in range(T)])
        print("a values:")
        for j in range(n):
            print(f"  Target {j}: {[a[j][t].solution_value() for t in range(T)]}")
    else:
        print("No optimal solution found.")

# Example usage
def Ud(j, c_t, t):
    """Defender utility function example."""
    return 10 * c_t  # Example: linear function of resource allocation

def Ua(j, c_t, t):
    """Attacker utility function example."""
    return 5 * (1 - c_t)  # Example: attacker utility decreases with defender allocation

# Problem parameters
k = [15, 20, 25]         # Example k_j values
b = [5, 8, 10]           # Minimum defender payoffs
d_star = [10, 12]        # Predefined d_j^* for j < lambda_idx
m = 2                    # Total resource limit
lambda_idx = 2           # Index of lambda (1-based, so it's the 3rd target)
T = 3                    # Number of time periods

# Solve the SSE problem
solve_sse(Ud, Ua, k, b, d_star, m, lambda_idx, T)
