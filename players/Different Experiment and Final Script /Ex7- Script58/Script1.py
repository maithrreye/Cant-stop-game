
from players.player import Player
import random
from players.scripts.DSL import DSL

class Script1(Player):

    def __init__(self):
        self._counter_calls = []
        for i in range(4):
            self._counter_calls.append(0)
            
    def get_counter_calls(self):
        return self._counter_calls 

    def get_action(self, state):
        actions = state.available_moves()
        
        for a in actions:
        
            if DSL.hasWonColumn(state,a) and DSL.isStopAction(a):
                self._counter_calls[0] += 1
                return a
                    
            if DSL.isDoubles(a):
                self._counter_calls[1] += 1
                return a
                    
            if DSL.isStopAction(a) and DSL.isStopAction(a):
                self._counter_calls[2] += 1
                return a
                    
            if DSL.containsNumber(a, 4 ):
                self._counter_calls[3] += 1
                return a
                    
        return actions[0]
                    