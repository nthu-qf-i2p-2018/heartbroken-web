# -*- coding: utf-8 -*-
from collections import namedtuple
from card import Card

from exception import NotHaveCardException
from exception import PassCardIllegalException, IllegalMoveException

import logging


GameInfo = namedtuple('GameInfo', ['rounds', 'scores'])


class Game:
    def __init__(self, agents=None):
        if agents:
            self.agents = agents
        else:
            from agent import AgentRandom
            self.agents = [AgentRandom(i) for i in range(1, 5)]

    def set_game(self, cards=None):
        if cards:
            self._deal_cards(cards)
        else:
            self._deal_cards(Card.deal_cards())

        self._pass_card(cards)

        self.heart_broken = False
        self.game_info = GameInfo([], [0]*4)
        logging.info("Game set")

    def play(self):
        scores = self.game_info.scores
        # find start turn (the one with ♣2)
        turn = next(i for i, hand in enumerate(self.hands)
                    if Card('♣', 2) in hand)

        for round in range(1, 14):
            logging.info('Round {}'.format(round))

            cards = self.play_a_round(turn)
            lead = cards[0].suit

            # compute score
            cards = [((i+turn) % 4, card) for i, card in enumerate(cards)]
            # find winner
            _, turn = max((card, i) for i, card in cards if card.suit == lead)
            scores[turn] += sum(card.point for i, card in cards)

            # save game history
            self.game_info.rounds.append(cards)

            logging.info(scores)

        # shooting the moon (豬羊變色)
        if 26 in scores:
            i = scores.index(26)
            scores = [26] * 4
            scores[i] = 0
            logging.info('Shooting the moon (豬羊變色)')
            logging.info(scores)

        return scores

    def play_a_round(self, turn):
        cards_played = []

        while len(cards_played) < 4:
            card = self._play_card(cards_played, turn)
            cards_played.append(card)
            turn = (turn + 1) % 4

        return cards_played

    def customize_info(self, turn):
        new_info = [[((i-turn) % 4, card) for i, card in round_info]
                    for round_info in self.game_info.rounds]
        return GameInfo(new_info, list(self.game_info.scores))

    @staticmethod
    def get_legal_moves(cards_you_have, cards_played, heart_broken):
        if Card('♣', 2) in cards_you_have:
            return [Card('♣', 2)]
        elif cards_played:
            suit = cards_played[0].suit
            # follow suit
            cards = [card for card in cards_you_have if card.suit == suit]
            if cards:
                return cards
            else:
                # cannot play point card in the 1st round
                cards = [card for card in cards_you_have
                         if card.point == 0 or len(cards_you_have) != 13]
                if cards:
                    return cards
                return cards_you_have
        else:
            if heart_broken:
                return cards_you_have
            else:
                cards = [card for card in cards_you_have if card.suit != '♥']
                if cards:
                    return cards
                else:
                    return cards_you_have

    def _deal_cards(self, cards):
        self.hands = [set(cards[i*13:(i+1)*13]) for i in range(4)]

    def _pass_card(self, cards):
        cards_to_pass = [set(agent.pass_cards(sorted(hand)))
                         for agent, hand in zip(self.agents, self.hands)]

        # check if legal
        for i, cards in enumerate(cards_to_pass):
            if not cards.issubset(self.hands[i]):
                cards_not_in = set(cards) - self.hands[i]
                raise NotHaveCardException(self.agents[i], cards_not_in)
            if len(cards) != 3:
                raise PassCardIllegalException(self.agents[i], cards)

        for i, hand in enumerate(self.hands):
            card_from = (i - 1) % 4
            card_str = ', '.join(map(str, cards_to_pass[card_from]))
            logging.info("Player #{0} pass {1} to #{2}.".format(
                self.agents[card_from].id, card_str, self.agents[i].id))
            self.hands[i] = hand - cards_to_pass[i] | cards_to_pass[card_from]

    def _play_card(self, cards_played, turn):
        agent, hand = self.agents[turn], self.hands[turn]
        hb = self.heart_broken
        info = self.customize_info(turn)

        card_played = agent.play(sorted(hand), list(cards_played), hb, info)

        # check if the card played is legal
        if card_played not in Game.get_legal_moves(hand, cards_played, hb):
            raise IllegalMoveException(agent, card_played)

        # remove the card played from the player's hand
        hand.remove(card_played)

        logging.info("Player #{0} play: {1}.".format(agent.id, card_played))

        if not self.heart_broken and card_played.suit == '♥':
            self.heart_broken = True
            logging.info("Heart is broken")

        return card_played


if __name__ == '__main__':
    game = Game()
    game.set_game()
    scores = game.play()
    print(scores)
