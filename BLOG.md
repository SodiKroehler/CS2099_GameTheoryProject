four methods:

BASE: baseline: random distribution
SCSOP: single csop: maximize U_d_1 - aka minimize player utilities
DCSOP: double csop: minimize player utility, maximize player reward
DCSOPT: double csop thresh = minimize player utility, maximize player reward, per-target thresholds.



utilty of player i for target t = thresh_t - r_t
reward for player i for target t = manually defined 

## Variable Declarations:
n is the number of attackers, i think this is synonymous with attacker types, ie we are only considering one attacker of each type
t is a target, T is all targets
m resources to cover
defender's strategy is an array C where each c represent coverage on target t, paper has it as lte 1
attacker i has strategy a which is array where each value represents prob of attacking t

U for defender is a n by T matrix, 


## iterative epsi solving method:
we have 2 objectives
when we maximize the second, we want to maximize defender utility subject to:

can't go less than previously found objective for this obj
have to satisfy lower bounds (dont understand yet)
condition 1 is this, prev d util - current utilty at a target and coverage value for that target has to be less


reading through the oragami thing again, i'm not sure it will work because we don't have binary covered or not covered state. 
-- actually this isn't true, the amount of hit points dont do anything to the coverage actually, they just affect the probabilty of attack. a target is covered if hit points > sum(damage attacker j can do ) over all aTypes j and uncovered otherwise.
still would like to solve using both milps and oragami if possible? it says it's just an efficiency thing, and it might help to work through each way equally.

## milps again
c is the coverage vector, is ntargets long
q is the prob of attacker per target, is ntargets wide and natts long
d is defender utility, is ntargets wide and natts long

dont think that ortools can deal with matricies, could form them into lists?
also could use a matrix form optimizer and want to do this for the practice

### CVXPY
d[t][j] is 1 * (however valuable that target is) * (wether or not that target's hit points is higher than the sum of all attackers ability, which is a constant)
or sum(canHit)

a[t][j] is canHit * value[t]

attackers have different value per target, but no preferences about q.
thus we can say for this problem that q = 1 if canHit and 0 if cant, making each attr utility be value[t][j] (constant) * q[t]
where q[t] = maxCanHit (constant) - c[t] but is also greater than 0
if c[t] is more than the maxCanHit, then q[t] is 0.
if c[t] is 0, then q[t] is maxCanHit

so if k[j] was the previous lower bound on utility,

in the paper, n is the number of attacker types, but the list of bounds is also n. this makes me think that they are not actually considering attacker types to have different values, but rather each attacker type to depict each possible optimization type. going off this being true and making alterations to match

however, in our problem statement, we are first optimizing on least coverage (malignant) and secondarily on a social choice funciton, which we can represent as a value on the target.
aka it doesnt change
aka each lower bound is for a specific attacker type, for a specific target
we absolutely have to maximize per attacker type.