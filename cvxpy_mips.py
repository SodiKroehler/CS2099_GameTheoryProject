import cvxpy as cp
import numpy as np


# def create_data_model():
#     data = {}
#     data['nTargets'] = 3
#     data['nAtters'] = 3
#     data['defenderValues'] = [1, 1, 1]
#     data['attackerValues'] = [1]
#     data['attackerHitAbility'] = [1]
#     data['m'] = 2
#     data['dstar'] = [0, 0, 0] #curr max defender utility for each attacker
#     data['b'] = [0, 0, 0] #lower bound for each def util for each att
#     data['c'] = [0, 0, 0] #defender current coverage vector
#     data['k'] = [0, 0, 0] #attacker previous best utility

#     return data

class Game:
    nTargets = 3
    nAtters = 3
    defenderValues = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    attackerValues = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    attackerHitAbility = [1,1,1]
    m = 20
    dstar = [0, 0, 0] #curr max defender utility for each attacker
    b = [0, 0, 0] #lower bound for each def util for each att
    c = [0, 0, 0] #defender current coverage vector
    k = [0, 0, 0] #attacker previous best utility


def milp_solver(currJ):
    # _ = create_data_model()
    _ = Game()
    M = 1e5
    epsi = 1e-5

    maxCanHit = sum(_.attackerHitAbility)

    q = cp.Variable(_.nTargets) # attacker coverage
    c = cp.Variable(_.nTargets) # defender coverage  
    d = cp.Variable(_.nAtters) # defender coverage  
    # d_curr = cp.Variable(_.dstar[currJ]) # defender utility for current objective
    k_curr = cp.Variable() # attacker utility for current objective

    constraints = []
    for t in range(_.nTargets):
        constraints.append(k_curr - (_.attackerValues[t][currJ] * q[t]) <= M * (1 - q[t]))
        constraints.append(0 <= k_curr - (_.attackerValues[t][currJ] * q[t]))
        constraints.append(d[currJ] - (_.defenderValues[t][currJ] * q[t]) <= M * (1 - q[t]))
        # constraints.append(0 <= d[currJ] - (_.defenderValues[t][currJ] * q[t]))
        constraints.append(q[t] >= 0)
        # constraints.append(q[t] <= 1)
        constraints.append(q[t] <= (epsi + ((maxCanHit - c[t])/maxCanHit)))
        constraints.append(q[t] >= (epsi - ((maxCanHit - c[t])/maxCanHit)))
        # constraints.append(q[t] >= ((maxCanHit - c[t])/_.nTargets))
        constraints.append(0 <= c[t])
        constraints.append(c[t] <= 1)


    for j in range(_.nAtters):
        if j > currJ:
            d[j] >= _.b[j] #meet lower bounds for other attackers
        elif j < currJ:
            d[j] = _.dstar[j] #meet previously maximized utilities


    constraints.append(sum(q) <= 1)
    constraints.append(sum(q) >= 1)
    constraints.append(sum(c) <= _.m)

    objective = cp.Maximize(d[currJ])

    problem = cp.Problem(objective, constraints)
    problem.solve()

    print("Status:", problem.status)
    print("Optimal attacker coverage (q):")
    print(q.value)
    print("Optimal defender coverage (c):")
    print(c.value)
    print("Optimal defender payoff (d):")
    print(d.value)
    print("Optimal attacker type j payoff:")
    print(k_curr.value)


def iterative_constraints_alg():
    _ = Game()
    
    


if __name__ == "__main__":
    milp_solver(0)
    # milp_solver(1)
    # milp_solver(2)
    # iterative_constraints_alg()