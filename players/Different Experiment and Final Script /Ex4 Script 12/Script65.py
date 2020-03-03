
from players.player import Player
import random
from players.scripts.DSL import DSL

class Script65(Player):

    def __init__(self):
        self._counter_calls = []
        for i in range(6):
            self._counter_calls.append(0)
            
    def get_counter_calls(self):
        return self._counter_calls 

    def get_action(self, state):
        actions = state.available_moves()
        
        for a in actions:
        
            if DSL.containsNumber(a, 3 ):
                self._counter_calls[0] += 1
                return a
                    
            if DSL.isStopAction(a):
                self._counter_calls[1] += 1
                return a
                    
            if DSL.containsNumber(a, 2 ) and DSL.containsNumber(a, 5 ) and DSL.actionWinsColumn(state,a):
                self._counter_calls[2] += 1
                return a
                    
            if DSL.isDoubles(a) and DSL.isDoubles(a):
                self._counter_calls[3] += 1
                return a
                    
            if DSL.hasWonColumn(state,a):
                self._counter_calls[4] += 1
                return a
                    
            if DSL.hasWonColumn(state,a) and DSL.containsNumber(a, 2 ):
                self._counter_calls[5] += 1
                return a
                    
        return actions[0]
                    