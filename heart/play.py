# -*- coding: utf-8 -*-
from game import Game
from agent import AgentRandom, AgentMedium, MyAgent, WebAgent
import sys


if __name__ == '__main__':
    user_id = sys.argv[1]
    wa = WebAgent(user_id)
    game = Game(
        [wa, AgentRandom('Superman'),
         AgentMedium('Batman'), MyAgent('Spiderman')]
    )

    game.set_game()
    scores = game.play()
    wa.close(scores)
    print(scores)
