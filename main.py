# from strategies import S_RAND, Strategy
import random
import math
    
class Player:
    def __init__(self, name):
        self.name = name
        self.player_sigma = []
        self.utils = []


    def set_utils(self, util_array):
        self.utils = util_array

    def set_sigma(self, targets):
        player_strat = [0,0,0]
        #BASE:, cuz a player will always pick the target with minimum coverage
        for i in range(len(targets.targets)):
            player_strat[i] = targets.max_c - targets.coverage[i]
        if sum(player_strat) == 0:
            self.player_sigma = [1/len(player_strat) for i in player_strat]
        else:
            self.player_sigma = [float(i)/sum(player_strat) for i in player_strat]

    def get_reward(self, targets, target_name):
        # if strategy is BASE
        curr_sigma = self.player_sigma[targets.targets.index(target_name)]
        curr_reward = self.utils[targets.targets.index(target_name)]
        return curr_sigma * curr_reward


class Targets:
    def __init__(self, m):
        self.max_c = 0
        self.m = m
        self.num_targets = 3
        self.targets = ["t1", "t2", "t3"]
        self.coverage = [0,0,0]
        self.taus = [0,0,0]

    def add_coverage(self, c, target_name = None):
        if target_name:
            self.coverage[self.targets.index(target_name)] += c
            self.max_c += c
        else:
            for i in range(len(c)):
                self.coverage[i] += c[i]
            self.max_c += sum(c)
    
    def get_coverage(self, target_name):
        return self.coverage[self.targets.index(target_name)]

    def get_targets(self):
        target_dict = {}
        for i in range(len(self.targets)):
            target_dict[self.targets[i]] = self.coverage[i]


    
class GameMaster():
    def __init__(self, m):
        
        self.targets = Targets(3)
        self.players = []
        self.c = [0,0,0]
        self.m = m

    def add_player(self, name, util):
        player = Player(name)
        player.set_utils(util)
        self.players.append(player)

    def set_C(self):
        randc = [random.randint(1, 10) for i in range(3)]
        randc = [math.floor(i / sum(randc) * self.m) for i in randc]#only can distribute up to m
        self.targets.add_coverage(randc)
        self.c = randc
        return randc
    
    def get_C(self):
        return self.c
            
    def get_summed_rewards(self):
        total = 0
        for i in range(len(self.players)):
            for t in self.targets.targets:
                total += self.players[i].get_reward(self.targets, t)
        return total
   


#  if this file is run, run the following code:
if __name__ == '__main__':
    game = GameMaster(15)
    game.add_player("p1", [1,2,3])
    game.add_player("p2", [1,3,2])
    game.add_player("p3", [3,2,1])
    game.set_C()
    print(game.get_C())
    for p in game.players:
        p.set_sigma(game.targets)
    
    print(game.get_summed_rewards())


    # scenario 1: dumb player utiltiies, malevolent, single objective game master
    U_c^d = U