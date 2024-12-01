from docplex.mp.model import Model

def solve_csop_cplex(m, n, T, a, b, c, d, d_star, k, U_d, U_a, Z=1e6):
    # Create the model
    model = Model(name="CSOP")
    # m is number of resources
    # n is number of attacker types: 3 for us
    # T is set of targets : 2 for us

    # a is attacker coverage : n x T matrix, each val is prob of attacker x attacking target t
    # k is attacker payoff : n x 1 matrix, each val is payoff for attacker x attacking target t
    # need to edit after reproduction, k needs to grow to k x T matrix


    # b is objective bounds
    # c is defender coverage
    # d is defender payoff
    # d_star is maximized defender payoff

    # U_d is defender payoff structure
    # U_a is attacker payoff structure
    # Z is a large number


    # Variables
    d_vars = {j: model.continuous_var(name=f"d_{j}", lb=0) for j in range(1, n + 1)}
    c_vars = {t: model.continuous_var(name=f"c_{t}", lb=0, ub=1) for t in T}
    a_vars = {(j, t): model.binary_var(name=f"a_{j}_{t}") for j in range(1, n + 1) for t in T}

    # Objective function: Maximize d_lambda (assuming d_lambda is d_1 for simplicity)
    model.maximize(d_vars[1])

    # Constraints
    # Constraint (2)
    for j in range(1, n + 1):
        for t in T:
            model.add_constraint(
                d_vars[j] - U_d[j][t] * c_vars[t] <= Z * (1 - a_vars[j, t]),
                f"Constraint_2_{j}_{t}"
            )

    # Constraint (3)
    for j in range(1, n + 1):
        for t in T:
            model.add_constraint(
                k[j] - U_a[j][t] * c_vars[t] <= Z * (1 - a_vars[j, t]),
                f"Constraint_3_{j}_{t}"
            )

    # Constraint (4)
    for j in range(1, n + 1):
        if j <= m:
            model.add_constraint(d_vars[j] == d_star[j], f"Constraint_4_{j}")

    # Constraint (5)
    for j in range(m + 1, n + 1):
        model.add_constraint(d_vars[j] >= b[j], f"Constraint_5_{j}")

    # Constraint (6)
    for j in range(1, n + 1):
        for t in T:
            model.add_constraint(a_vars[j, t] >= 0, f"Constraint_6_{j}_{t}")

    # Constraint (7)
    for j in range(1, n + 1):
        model.add_constraint(
            model.sum(a_vars[j, t] for t in T) == 1,
            f"Constraint_7_{j}"
        )

    # Constraint (8)
    for t in T:
        model.add_constraint(c_vars[t] >= 0, f"Constraint_8a_{t}")
        model.add_constraint(c_vars[t] <= 1, f"Constraint_8b_{t}")

    # Constraint (9)
    model.add_constraint(
        model.sum(c_vars[t] for t in T) <= m,
        "Constraint_9"
    )

    # Solve the problem
    solution = model.solve()

    # Check if a solution was found
    if solution:
        d_result = {j: d_vars[j].solution_value for j in range(1, n + 1)}
        c_result = {t: c_vars[t].solution_value for t in T}
        a_result = {(j, t): a_vars[j, t].solution_value for j in range(1, n + 1) for t in T}

        return {
            "status": "Optimal",
            "objective_value": model.objective_value,
            "d": d_result,
            "c": c_result,
            "a": a_result,
        }
    else:
        return {
            "status": "No Solution Found"
        }

# Example usage with placeholder inputs
m = 2  # Number of defender resources
n = 3  # Number of attacker types
T = [1, 2]  # Set of targets
a = [[0, 1], [1, 0], [1, 1]]  # Attacker coverage
b = [0, 1, 1]  # Objective bounds
c = [0.5, 0.5]  # Defender coverage
d = [0, 0, 0]  # Defender payoff
d_star = [1, 1, 1]  # Maximized defender payoff
k = [1, 2, 3]  # Attacker payoff
U_d = [[1, 2], [2, 1], [1, 1]]  # Defender payoff structure
U_a = [[1, 2], [2, 1], [1, 1]]  # Attacker payoff structure

result = solve_csop_cplex(m, n, T, a, b, c, d, d_star, k, U_d, U_a)
print(result)


def iterative_e_const():
