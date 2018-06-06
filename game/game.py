# -*- coding: utf-8 -*-
from collections import namedtuple
from card import Card


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
        print("Game set")

    def _deal_cards(self, cards):
        self.hands = [set(cards[i*13:(i+1)*13]) for i in range(4)]

    def _pass_card(self, cards):
        cards_to_pass = [set(agent.pass_cards(sorted(hand)))
                         for agent, hand in zip(self.agents, self.hands)]

        # check if legal
        for i, cards in enumerate(cards_to_pass):
            if set(cards).issubset(self.hands[i]):
                # TODO: throw PassCardIllegalException
                pass

        for i, hand in enumerate(self.hands):
            self.hands[i] = hand - cards_to_pass[i] | cards_to_pass[(i - 1) % 4]

    def play_a_round(self, turn):
        cards_played = []

        while len(cards_played) < 4:
            agent, hand = self.agents[turn], self.hands[turn]

            card_played = agent.play(sorted(hand), list(cards_played), self.heart_broken, self.game_info)
            legal_moves = Game.get_legal_moves(self.hands[turn], cards_played, self.heart_broken)

            if card_played not in legal_moves:
                # throw IllegalMoveExceptioin
                pass

            print("Player #{0} play: {1}.".format(agent.id, card_played))

            if card_played.suit == '♥':
                self.heart_broken = True

            hand.remove(card_played)
            cards_played.append(card_played)

            turn = (turn + 1) % 4

        return cards_played

    def play(self):
        scores = self.game_info.scores
        turn = next(i for i, hand in enumerate(self.hands) if Card('♣', 2) in hand)
        for round in range(1, 14):
            print('Round', round)
            cards = self.play_a_round(turn)
            lead_suit = cards[0].suit

            # add Player id to the card
            cards = [((i+turn) % 4, card) for i, card in enumerate(cards)]

            # find winner
            card, turn = max((card, i) for i, card in cards if card.suit == lead_suit)

            # compute score
            scores[turn] += sum(card.point for i, card in cards)

            # save game history
            self.game_info.rounds.append(cards)

            print(scores)

        # shooting the moon (豬羊變色)
        if 26 in scores:
            i = scores.index(26)
            scores = [26] * 4
            scores[i] = 0

        return scores

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
                cards = [card for card in cards_you_have if card.point == 0 or len(cards_you_have) != 13]
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


if __name__ == '__main__':
    game = Game()
    game.set_game()
    scores = game.play()
