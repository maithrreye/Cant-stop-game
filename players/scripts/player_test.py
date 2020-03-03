from players.player import Player
from players.scripts.DSL import DSL

class PlayerTest(Player):

    def get_action(self, state):
        actions = state.available_moves()
        
        for a in actions:
            if DSL.hasWonColumn(state,a) and DSL.isStopAction(a):
                return a
        return actions[0]

