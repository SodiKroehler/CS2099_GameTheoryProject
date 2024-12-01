from ortools.linear_solver import pywraplp 

def create_data_model():
    data = {}
    data['udc'] = [[1,1,1]] # nTargets x nAtters
    data['uac'] = [[0,0,0]] # nTargets x nAtters
    data['udu'] = [[0,0,0]] # nTargets x nAtters
    data['uau'] = [[1,1,1]] # nTargets x nAtters
    return data

def milp_solver(b, obj):


    data = create_data_model()
    nTargets = len(data['udc'][0])
    nAtters = len(data['udc'])
    nObjs = len(b)
    M = 1e5

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        raise Exception("Solver not available.")
    

    c = [solver.NumVar(0.0, 1.0, f"c_{i}") for i in range(nTargets)]  # defender coverage
    
    for aType in range(nAtters):
        q = [solver.NumVar(0, 1, f"q_{i}") for i in range(nTargets)]
    
         # attacker coverage
    d = [solver.NumVar(0, solver.infinity(), f'd[{i}]') for i in range(nAtters)] # defender utility for current objective
    solver.Maximize(solver.Sum(d))

    # Constraints
    for j in range(nAtters):
        solver.Add(d[j] - data['udc'][c][j] <= M * (1 - q[j])) #will need to change this with more attacker types
        solver.Add(v - (Pa[i] - Ra[i]) * c[i] - Ra[i] <= (1 - q[i]) * M, f"Upper_Bound_AttEU_{i}")
        solver.Add(v - (Pa[i] - Ra[i]) * c[i] - Ra[i] >= 0, f"Lower_Bound_AttEU_{i}")
        solver.Add(v - (c[i] * Rd[i]) + ((1-c[i]) * Pd[i]) >= 0, f"Lower_Bound_DefEU_{i}")
        solver.Add(v - (c[i] * Rd[i]) + ((1-c[i]) * Pd[i]) <= c[i] * M, f"Upper_Bound_DefEU_{i}")
        # solver.Add(v <= (c[i] * Rd[i]) + ((1-c[i]) * Pd[i]), f"Def_EU_{i}")
        # solver.Add(0 <= k - c[i] * Rd[i]) + ((1-c[i]) * Pd[i]) <= M * (1 - c[i]), f"Upper_Bound_AttEU_{i}")

    # Defender allocation probabilities sum ≤ 1
    solver.Add(sum(c) <= 1, "Defender_Probability_Sum")

    # Exactly one target must be attacked
    solver.Add(sum(q) == 1, "Attacker_Probability_Sum")

    # Solve the problem
    status = solver.Solve()

    # Output results
    if status == pywraplp.Solver.OPTIMAL:
        print("Status: OPTIMAL")
        print("Objective Value (Defender Utility):", solver.Objective().Value())
        print("Defender's Allocation (c):", [c[i].solution_value() for i in range(n)])
        print("Attacker's Target (q):", [q[i].solution_value() for i in range(n)])
        print("Value of v (Attacker Utility):", v.solution_value())
    else:
        print("No optimal solution found.")


def problem2_quiz5():
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not available!")
        return

    Rd = [3, 4, 5]  # Defender's reward if defended
    Pd = [-2, -6, -4]  # Defender's penalty if not defended
    Ra = [2, 3, 4]  # Attacker's reward if attacked
    Pa = [-1, -3, -5]  # Attacker's penalty if not attacked

    n = len(Rd)
    M = 1e5
    M2 = 1

    c = [solver.NumVar(0, 1, f'c[{i}]') for i in range(n)]
    q = [solver.NumVar(0, 1, f"q_{i}") for i in range(n)]
    z = [solver.NumVar(0, solver.infinity(), f'z[{i}]') for i in range(n)]
    v = solver.NumVar(0, solver.infinity(), 'v') 

    solver.Maximize(solver.Sum(z[i] for i in range(n)))

    # Constraints
    for i in range(n):
        # zi = defeu(i) * q(i)
        #linearize by splitting the calculation into two parts
        # z[i] = c[i] * Rd[i] * q[i] + (1 - c[i]) * Pd[i] * q[i]
        # solver.Add(z[i] <= M * (1-q[i])) #if qi is low, this bound is small
        # solver.Add(z[i] <= c[i] * Rd[i] + (1 - c[i]) * Pd[i])
        solver.Add(z[i] >= 0)
        # solver.Add(z[i] >= (c[i] * Rd[i] + (1 - c[i]) * Pd[i]) - M * (1 - q[i]))  # Lower bound for z[i]
        solver.Add(z[i] - (c[i] * Rd[i] + (1 - c[i]) * Pd[i]) <= M * q[i])  # Upper bound when q[i] = 0

        # Linearized constraints for v and AttEU
        solver.Add(v - (c[i] * Pa[i] + (1 - c[i]) * Ra[i]) <= (1 - q[i]) * M)  # Upper bound when q[i] = 0
        solver.Add(v - (c[i] * Pa[i] + (1 - c[i]) * Ra[i]) >= 0)  # Lower bound
    solver.Add(solver.Sum(q[i] for i in range(n)) == 1)
    solver.Add(solver.Sum(c[i] for i in range(n)) <= 1)
    status = solver.Solve()

    # Output results
    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found:')
        print(f'Maximized v = {v.solution_value()}')
        for i in range(n):
            print(f'c[{i}] = {c[i].solution_value()}')
            print(f'q[{i}] = {q[i].solution_value()}')
            print(f'z[{i}] = {z[i].solution_value()}')
    else:
        print('The problem does not have an optimal solution.')
