  
def udjt(c, j, t):
    ct = c[t]
    rewardAtTforJ = 1
    penaltyAtTforJ = 0
    return (ct * rewardAtTforJ) + ((1 - ct) * penaltyAtTforJ)

def udj(c, j):
    return sum([udjt(c, j, t) for t in range(len(c))])

def uajt_uncov(c, j, t):
    rewardAtTforJ = 1
    return rewardAtTforJ

def uajt_cov(c, j, t):
    penaltyAtTforJ = 0
    return penaltyAtTforJ

def uajt(ct, j, t):
    rewardAtTforJ = 1
    penaltyAtTforJ = 0
    return ((1 - ct) * rewardAtTforJ) + (ct * penaltyAtTforJ)

def getNextUnsatisfiedBound(b, c):
    #b is a list of [attacker_type, target, bound]
    for constraint in b:
        if udjt(c[constraint[1]], constraint[0], constraint[1]) >= constraint[2]:
            return constraint;
    return None

def sortTargetsByAttackerUtility(T):
    return T

def MIN_COV(i, c, bi):

    cstar = np.zeros(len(c))
    minResources = 0
    
    return c

def ORAGAMI_M(b):
    c = []
    m = 5

    #each b_i is subscripted by an attacker type, no explicit loops for other types, b should have a bound for each attacker type
    currBound = getNextUnsatisfiedBound(b, c)
    while currBound is not None:
        i = currBound[0]
        t = currBound[1]
        b = currBound[2]

        #sort targets in decreasing order of attacker utility
        sortedTargets = sortTargetsByAttackerUtility(c, i)
        left = m - c.sum()
        next = 1

        addedCoverage = [0 for n in len(c)]

        while next <= len(c):
            maxAttackerUtilitySoFar = 0
            attackerUtilityAtNext = uajt(c, i, sortedTargets[next])
            x = 0
            nonInducibleNextTarget = False
            resourcesExceeded = False


            for previ in 1..next:
                previAttackerUtility = uajt(c, i, sortedTargets[previ])
                if previAttackerUtility > maxAttackerUtilitySoFar:
                    maxAttackerUtilitySoFar = previAttackerUtility

            if maxAttackerUtilitySoFar > attackerUtilityAtNext:
                x = maxAttackerUtilitySoFar
                nonInducibleNextTarget = True
            else:
                x = attackerUtilityAtNext


            for t in 1..next:
                attackerUtilityUncoveredTarget = uajt(c, i, sortedTargets[t], 'uncovered')
                attackerUtilityCoveredTarget = uajt(c, i, sortedTargets[t], 'covered')
                addedCoverage[t] = ((x -attackerUtilityUncoveredTarget )/ (attackerUtilityCoveredTarget - attackerUtilityUncoveredTarget)) - c[t]

            if addedCoverage.sum() >= left:
                resourcesExceeded = True
                ratio = [0 for n in len(c)]
                sum_ratio_to_next = 0
                for target in range(len(c)):
                    ratio[t]= 1 / (uajt_uncov(c, i, target) - uajt_cov(c, i, target))
                    if target <= next:
                        sum_ratio_to_next = sum_ratio_to_next + ratio[t]
                for target in range(len(c)):
                    addedCoverage[target] = (ratio[t] * left)/sum_ratio_to_next

            c = c + addedCoverage

            if udj(c, i) >= b:
                c = MIN_COV(i, c, b)
                break
            elif resourcesExceeded or nonInducibleNextTarget:
                return 'infeasible'
            else:
                left = left - addedCoverage.sum()
                next = next + 1
        if next == (len(c) + 1) and left > 0:
            ratio = [0 for n in len(c)]
            sum_ratio_to_next = 0
            for target in range(len(c)):
                ratio[t]= 1 / (uajt_uncov(c, i, target) - uajt_cov(c, i, target))
                if target <= next:
                    sum_ratio_to_next = sum_ratio_to_next + ratio[t]
            for target in range(len(c)):
                addedCoverage[target] = (ratio[t] * left)/sum_ratio_to_next
            c = c + addedCoverage

            if udj(c, i) >= b:
                c = MIN_COV(i, c, b)
            else:
                return 'infeasible'
        else:
            return "infeasible"
        currBound = getNextUnsatisfiedBound(b, c)
    return c