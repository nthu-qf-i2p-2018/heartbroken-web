# -*- coding: utf-8 -*-
from agent import Agent
from card import Card
from game import Game
import requests
import json
import os


API_URL = os.environ.get('GAME_WEB_URL', 'http://localhost:8000/getplay')
HEADERS = {'Content-Type': 'application/json'}


class WebAgent(Agent):
    def play(self, cards_you_have, cards_played, heart_broken, info):
        legal_moves = Game.get_legal_moves(cards_you_have, cards_played, heart_broken)
        cards_you_have = [card.to_json() for card in cards_you_have]
        cards_played = [card.to_json() for card in cards_played]
        history = [[(i, card.to_json()) for i, card in round] for round in info.rounds]
        data = {
            'instruction': 'play card',
            'cards_you_have': cards_you_have,
            'cards_played': cards_played,
            'heart_broken': heart_broken,
            'history': history
        }

        result = self._sent_instruction(data)
        card = Card.from_json(result['card'])

        while card not in legal_moves:
            data['msg'] = "Illegal move!"
            result = self._sent_instruction(data)
            card = Card.from_json(result['card'])

        return card

    def pass_cards(self, cards):
        cards = [card.to_json() for card in cards]
        data = {
            'instruction': 'pass card',
            'cards_you_have': cards,
        }
        result = self._sent_instruction(data)
        return [Card.from_json(card_json) for card_json in result['cards']]

    def _sent_instruction(self, data):
        data['user_id'] = self.id
        data = json.dumps(data)
        r = requests.post(API_URL, headers=HEADERS, data=data)
        return r.json()

    

    def close(self, scores):
        data = {
            'instruction': 'end',
            'scores': scores,
        }
        self._sent_instruction(data)
