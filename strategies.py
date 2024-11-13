import random as rand
from main import Strategy

class Strategy:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy

    def c_t(self, targets, utility):
        C = []
        # for t in targets:
        #     C.append(rand.randint(1, 10))
        for t in targets:
            C.append(self.strategy(t, players, ))
        return C

    def __str__(self):
        return f"Strategy {self.name} with function {self.strategy}"
    
class PlayerStrategy():
    def __init__(self, name, utility):
        self.name = name
        self.utility = utility

    def u_i_t(self, target_idx):
        return self.utility(target_idx)

    def __str__(self):
        return f"Strategy {self.name} with function {self.strategy}"
    

def random_Strategy(target, player, m):
    return rand.randint(1, 10)

S_RAND = Strategy("Random", random_Strategy)
