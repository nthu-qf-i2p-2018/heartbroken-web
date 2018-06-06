# -*- coding: utf-8 -*-
import random
from itertools import product


class Card:
    @staticmethod
    def deal_cards():
        cards = list(ALL_CARDS)
        random.shuffle(cards)
        return cards

    @staticmethod
    def get_point(card):
        if card.suit == '♥':
            return 1
        elif card.suit == '♠' and card.number == 12:
            return 13
        else:
            return 0

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

        self.point = Card.get_point(self)

    def __str__(self):
        return self.suit + str(self.number)

    def __repr__(self):
        return self.suit + str(self.number)

    def __hash__(self):
        return hash(self.suit) ^ hash(self.number)

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False

        return self.suit == other.suit and self.number == other.number

    def __lt__(self, other):
        if self.suit == other.suit:
            return _number[self.number] < _number[other.number]
        else:
            return _suit[self.suit] < _suit[other.suit]

    def __gt__(self, other):
        if self.suit == other.suit:
            return _number[self.number] > _number[other.number]
        else:
            return _suit[self.suit] > _suit[other.suit]

    def to_json(self):
        return {'suit': self.suit, 'number': self.number}

    @classmethod
    def from_json(cls, json_obj):
        return cls(json_obj['suit'], json_obj['number'])


_number = {
    1: 100, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
    10: 10, 11: 11, 12: 12, 13: 13
}
_suit = {'♣': 0, '♦': 1, '♠': 2, '♥': 3}
ALL_CARDS = {Card(suit, num) for suit, num in product(_suit, _number)}
