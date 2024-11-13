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


if __name__ == '__main__':
# Call the function to solve the game
    # solve_stackelberg_game(10)
    minimize_sum_with_constraints(m=10)
