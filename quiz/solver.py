from ortools.linear_solver import pywraplp

def solve_stackelberg_game(m):
    # Initialize the solver
    solver = pywraplp.Solver.CreateSolver('GLOP')  # GLOP is used for linear programming

    # Define decision variables for the leader
    x1 = solver.NumVar(0, m, 'x1')  # x1 ranges from 0 to 10
    x2 = solver.NumVar(0, m, 'x2')  # x2 ranges from 0 to 10
    x3 = solver.NumVar(0, m, 'x3')  # x3 ranges from 0 to 10

    # # Define follower's pure strategy response based on the sum of x1, x2, and x3
    # # sum_x = x1 + x2 + x3
    # # y = 2 * sum_x + 1  # Pure strategy: y = 2(sum_x) + 1
    # # y = max(x1, x2, x3)

    # max_x = solver.NumVar(0, m, 'max_x')  # max_x is constrained by the same range as x1, x2, x3

    # # Add constraints to model max_x as the maximum of x1, x2, and x3
    # solver.Add(max_x >= x1)
    # solver.Add(max_x >= x2)
    # solver.Add(max_x >= x3)

    solver.Add(x1 + x2 + x3 <= m)

    #follower function
    #follower always selects the target with the lowest coverage, but experiences the same utility no matter which target
    #so leader needs to minimize all xs, with the lower constraint that for each target (c_x * 1), and the follower
    #so follower constraint is max(x1, x2, x3)

    # Leader's objective function: maximize 5(x1 + x2 + x3) - y,
    # which is equivalent to maximize 5(x1 + x2 + x3) + max_x
    objective = solver.Objective()
    objective.SetCoefficient(x1, 1)
    objective.SetCoefficient(x2, 1)
    objective.SetCoefficient(x3, 1)
    # objective.SetOffset(-1)  # Constant offset based on y expression
    objective.SetCoefficient(max_x, 1)
    objective.SetMinimization()

    # Solve the optimization problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f'Optimal solution found:')
        print(f'Leader\'s optimal x1: {x1.solution_value()}')
        print(f'Leader\'s optimal x2: {x2.solution_value()}')
        print(f'Leader\'s optimal x3: {x3.solution_value()}')
        print(f'Maximum of x1, x2, x3 (max_x): {max_x.solution_value()}')
        print(f'Follower\'s response y: {2 * (x1.solution_value() + x2.solution_value() + x3.solution_value()) + 1}')
        print(f'Leader\'s optimal objective value: {5 * (x1.solution_value() + x2.solution_value() + x3.solution_value()) - (2 * (x1.solution_value() + x2.solution_value() + x3.solution_value()) + 1)}')
    else:
        print('The problem does not have an optimal solution.')

def minimize_sum_with_constraints(m):
    # Initialize the solver
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Define decision variables for x1, x2, and x3 with lower bounds of 1 (thresholds)
    x1 = solver.NumVar(1, solver.infinity(), 'x1')
    x2 = solver.NumVar(1, solver.infinity(), 'x2')
    x3 = solver.NumVar(1, solver.infinity(), 'x3')

    # Add constraint: x1 + x2 + x3 <= m
    solver.Add(x1 + x2 + x3 <= m)

    # Objective: Minimize x1 + x2 + x3
    objective = solver.Objective()
    objective.SetCoefficient(x1, 1)
    objective.SetCoefficient(x2, 1)
    objective.SetCoefficient(x3, 1)
    objective.SetMinimization()

    # Solve the optimization problem
    status = solver.Solve()

    # if status == pywraplp.Solver.OPTIMAL:
    #     print(f'Optimal solution found:')
    #     print(f'Optimal x1: {x1.solution_value()}')
    #     print(f'Optimal x2: {x2.solution_value()}')
    #     print(f'Optimal x3: {x3.solution_value()}')
    #     print(f'Sum of x1, x2, x3: {x1.solution_value() + x2.solution_value() + x3.solution_value()}')
    # else:
    #     print('The problem does not have an optimal solution.')

    if status == pywraplp.Solver.OPTIMAL:
        return {
            'x1': x1.solution_value(),
            'x2': x2.solution_value(),
            'x3': x3.solution_value(),
            'sum': x1.solution_value() + x2.solution_value() + x3.solution_value()
        }
    else:
        return None




def problem1_quiz():
    # Initialize the solver
    solver = pywraplp.Solver.CreateSolver('GLOP')

    
    # xa = solver.NumVar(0, 1, 'xa')
    # xb = solver.NumVar(0, 1, 'xb')

    #player2
    xc = solver.NumVar(0, 1, 'xc')
    xd = solver.NumVar(0, 1, 'xd')
    xe = solver.NumVar(0, 1, 'xe')
    v = solver.NumVar(-solver.infinity(), solver.infinity(), 'v')

    # Constraints
    # solver.Add(v <= 3 * xa - 2 * xb)
    # solver.Add(v <= 4 * xa - xb)
    # solver.Add(v <= -xa + 2 * xb)
    # solver.Add(xa + xb == 1)
    # solver.Maximize(v)
    # status = solver.Solve()

    #player 2
    solver.Add(v <= -3 * xc + -4 * xd + xe)
    solver.Add(v <= 2 * xc + xd + -2 * xe)
    solver.Add(xc + xd + xe == 1)
    solver.Maximize(v)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f'Optimal solution found:')
        # print(f'Optimal x1: {x.solution_value()}')
        # print(f'Optimal x2: {xb.solution_value()}')
        print(f'Optimal x1: {xc.solution_value()}')
        print(f'Optimal x2: {xd.solution_value()}')
        print(f'Optimal x2: {xe.solution_value()}')

        # print(f'Sum of x1, x2, x3: {x1.solution_value() + x2.solution_value() + x3.solution_value()}')
    else:
        print('The problem does not have an optimal solution.')


def DefEU(i, ci):
    rewards = [3, 4, 5]
    penalties = [-2, -6, -4]
    reward = rewards[i] * ci
    penalty = penalties[i] * (1 - ci)
    return reward + penalty

def AttEU(i, ci):
    rewards = [2, 3, 4]
    penalties = [-1, -3, -5]
    reward = penalties[i]* ci
    penalty =  rewards[i] * (1 - ci)
    return reward + penalty


def problem2_quiz():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    M = 15000

    q = [solver.BoolVar(f'q[{i}]') for i in range(3)]
    c = [solver.NumVar(0, 1, f'c[{i}]') for i in range(3)]
    v = solver.NumVar(-solver.infinity(), solver.infinity(), 'v')

    solver.Maximize(solver.Sum(DefEU(i, c[i]) * q[i] for i in range(3)))

    for i in range(3):
        # 0 <= v - AttEU[i] <= (1 - q[i]) * M
        solver.Add(v - AttEU(i, c[i]) >= 0)
        solver.Add(v - AttEU(i, c[i]) <= (1 - q[i]) * M)
    solver.Add(solver.Sum(c[i] for i in range(3)) <= 1)
    solver.Add(solver.Sum(q[i] for i in range(3)) == 1)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found!")
        print(f"v = {v.solution_value()}")
        print("q values:", [q[i].solution_value() for i in range(n)])
        print("c values:", [c[i].solution_value() for i in range(n)])
    else:
        print("No optimal solution found.")

def problem2_quiz2():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    n = 3
    M = 100000
    Pa = [-1, -3, -5]
    Ra = [2,3,4] 
    Pd = [-2,-6,-4]
    Rd = [3,4,5] 


    c = [solver.NumVar(0, 1, f"c_{i}") for i in range(n)]
    q = [solver.IntVar(0, 1, f"q_{i}") for i in range(n)]
    v = solver.NumVar(0, solver.infinity(), "v")


    AttEU = [c[i] * Pa[i] + (1 - c[i]) * Ra[i] for i in range(n)]
    DefEU = [c[i] * Rd[i] + (1 - c[i]) * Pd[i] for i in range(n)]

    objective = solver.Objective()
    for i in range(n):
        DefEU_i = c[i] * Rd[i] + (1 - c[i]) * Pd[i]
        objective.SetCoefficient(q[i], DefEU_i)
    objective.SetMaximization()

    # Constraints
    for i in range(n):
        # 0 ≤ v - AttEU(i) ≤ (1 - q_i) * M
        solver.Add(v - AttEU[i] <= (1 - q[i]) * M, f"Upper_Bound_AttEU_{i}")
        solver.Add(v - AttEU[i] >= 0, f"Lower_Bound_AttEU_{i}")

    # Sum of defender probabilities must be <= 1
    solver.Add(sum(c) <= 1, "Defender_Probability_Sum")

    # Exactly one target must be attacked
    solver.Add(sum(q) == 1, "Attacker_Probability_Sum")

    # Solve the problem
    status = solver.Solve()

    # Output results
    if status == pywraplp.Solver.OPTIMAL:
        print("Status: OPTIMAL")
        print("Objective Value:", solver.Objective().Value())
        print("Defender's Allocation:", [c[i].solution_value() for i in range(n)])
        print("Attacker's Target:", [q[i].solution_value() for i in range(n)])
        print("Value of v:", v.solution_value())
    else:
        print("No optimal solution found.")

def problem2_quiz3():
    solver = pywraplp.Solver.CreateSolver('GLOP')

    xc = solver.NumVar(0, 1, 'x1')
    xd = solver.NumVar(0, 1, 'x2')
    xe = solver.NumVar(0, 1, 'x3')
    v = solver.NumVar(-solver.infinity(), solver.infinity(), 'v')

    # Constraints
    # solver.Add(v <= 3 * xa - 2 * xb)
    # solver.Add(v <= 4 * xa - xb)
    # solver.Add(v <= -xa + 2 * xb)
    # solver.Add(xa + xb == 1)
    # solver.Maximize(v)
    # status = solver.Solve()

    #player 2
    solver.Add(v <= -3 * xc + -4 * xd + xe)
    solver.Add(v <= 2 * xc + xd + -2 * xe)
    solver.Add(xc + xd + xe == 1)
    solver.Maximize(v)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f'Optimal solution found:')
        # print(f'Optimal x1: {x.solution_value()}')
        # print(f'Optimal x2: {xb.solution_value()}')
        print(f'Optimal x1: {xc.solution_value()}')
        print(f'Optimal x2: {xd.solution_value()}')
        print(f'Optimal x2: {xe.solution_value()}')

        # print(f'Sum of x1, x2, x3: {x1.solution_value() + x2.solution_value() + x3.solution_value()}')
    else:
        print('The problem does not have an optimal solution.')

def problem2_quiz4():

    # Data from the table
    Rd = [3, 4, 5]  # Defender's reward if defended
    Pd = [-2, -6, -4]  # Defender's penalty if not defended
    Ra = [2, 3, 4]  # Attacker's reward if attacked
    Pa = [-1, -3, -5]  # Attacker's penalty if not attacked

    n = len(Rd)
    M = 1e5

    # Create the solver
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        raise Exception("Solver not available.")

    # Decision variables
    c = [solver.NumVar(0.0, 1.0, f"c_{i}") for i in range(n)]  # Defender allocation
    q = [solver.NumVar(0, 1, f"q_{i}") for i in range(n)]     # Attacker target
    # q = [solver.IntVar(0, 1, f"q_{i}") for i in range(n)]     # Attacker target
    d = [solver.NumVar(0, solver.infinity(), f'd[{i}]') for i in range(n)]
    v = solver.NumVar(0.0, solver.infinity(), "v")           # Value of v
    # k = solver.NumVar(0.0, solver.infinity(), "k")           # Attacker payoff
    


    # Objective: Maximize the defender's expected utility
    # objective = solver.Objective()
    solver.Maximize(solver.Sum(d[i] for i in range(n)))
    # for i in range(n):
    #     # Defender utility: c[i] * Rd[i] + (1 - c[i]) * Pd[i]
    #     objective.SetCoefficient(q[i], c[i] * Rd[i] + Pd[i])  # Linearized coefficient for q[i]
    # objective.SetMaximization()

    # Constraints
    for i in range(n):
        # Attacker utility: c[i] * Pa[i] + (1 - c[i]) * Ra[i]
        # Linearized: v - c[i] * (Pa[i] - Ra[i]) - Ra[i] ≤ (1 - q[i]) * M
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



if __name__ == '__main__':
# Call the function to solve the game
    # solve_stackelberg_game(10)
    # minimize_sum_with_constraints(m=10)

    problem2_quiz5()
    # problem2_quiz4()


