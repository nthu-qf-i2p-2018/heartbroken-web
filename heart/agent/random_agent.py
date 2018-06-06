# -*- coding: utf-8 -*-
import random
from agent import Agent
from game import Game


class AgentRandom(Agent):
    def play(self, cards_you_have, cards_played, heart_broken, info):
        cards = Game.get_legal_moves(cards_you_have, cards_played, heart_broken)
        return random.choice(cards)

    def pass_cards(self, cards):
        return random.sample(cards, 3)
