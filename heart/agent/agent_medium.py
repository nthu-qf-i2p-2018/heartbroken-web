# -*- coding: utf-8 -*-
import random
from agent import Agent
from game import Game
from card import Card
import card


class AgentMedium(Agent):
    def play(self, cards_you_have, cards_played, heart_broken, info):
        #remember cards
        if len(cards_you_have) == 13:
            self.memorize(cards_you_have)
            self.mycard = cards_you_have[:]
        
        #remove cards from memory if a player has played it
        self.remove_played_cards(info.rounds, cards_played)
        
        
        legal_moves = Game.get_legal_moves(cards_you_have, cards_played, heart_broken)
        self.compute_card_rank(legal_moves)
        #good_moves = self.get_good_moves(cards_you_have, cards_played, heart_broken)
        
        return self.get_good_moves(cards_you_have, cards_played, heart_broken, legal_moves)
    
    #return largest card in hand
    def pass_cards(self, cards):
        largest = sorted(cards, key=lambda c: int(c.number==1)*13+c.number,reverse=True)[:3]
        return largest
    
    def memorize(self, cards):
        
        self.memory = {suit:
                       [Card(suit, number)
                       for number in card._number
                       if Card(suit, number) not in cards]
                       for suit in card._suit}
        
    def remove_played_cards(self, cards_lists, cards_played):
        for c in cards_played:
            self.memory[c.suit].remove(c)
        
        for cards_list in cards_lists[::-1]:
            for idx, c in cards_list[::-1]:
                if c in self.mycard:
                    return
                self.memory[c.suit].remove(c)
        
        
    def compute_card_rank(self, cards):
        self.card_rank = {}
        cards_suit = {suit:[] for suit in card._suit}
        for c in cards:
            cards_suit[c.suit].append(c)
        
        for suit in card._suit:
            cards_suit[suit].extend(self.memory[suit])
            cards_suit[suit].sort()
        
        rank = {suit:0 for suit in card._suit}
        for suit in card._suit:
            start = True
            mycard = False
            for c in cards_suit[suit]:
                if start:
                    if c in cards:
                        self.card_rank[c] = rank[suit]
                        mycard = True
                    else:
                        self.card_rank[c] = rank[suit]
                        rank[suit] += 1
                        mycard = False
                    start = False
                
                if c in cards:
                    mycard = True
                    self.card_rank[c] = rank[suit]
                else:
                    if mycard:
                        rank[suit] += 1
                    self.card_rank[c] = rank[suit]
                    mycard = False
                    rank[suit] += 1
                    
    
    def get_good_moves(self, cards_you_have, cards_played, heart_broken, legal_moves):
        cards_suit = {suit:[] for suit in card._suit}
        for c in legal_moves:
            cards_suit[c.suit].append(c)
        if cards_played:
            main_suit = cards_played[0].suit
            max_card = max([c for c in cards_played if c.suit == main_suit])
            score = sum(c.point for c in cards_played)
            
            if score > 0:
                #avoid getting points
                smaller = [c for c in legal_moves if c.suit!=main_suit or c<max_card]
                if smaller:
                    return random.choice(self.largest_cards(smaller))
                
                #you will get points anyway, so play the biggest card in your hand
                if main_suit == '♠' and Card('♠', 12) in self.memory['♠']:
                    candidates = [c for c in legal_moves if c.suit != '♠' or (c.number != 1 and c.number !=13)]
                    if not candidates:
                        candidates = legal_moves[:]
                else:
                    candidates = legal_moves[:]
                    
                return random.choice(self.largest_cards(candidates))
            elif main_suit == '♠':
                # playing any card you want, but don't play ♠13,♠1
                if Card('♠', 12) in self.memory['♠'] and len(cards_played) != 3:
                    candidates = [c for c in legal_moves if c.suit != '♠' or (c.number != 1 and c.number !=13)]
                    if not candidates:
                        candidates = legal_moves[:]

                    return random.choice(self.largest_cards(candidates))
                elif Card('♠', 12) in legal_moves:
                    if max_card > Card('♠', 12):
                        return Card('♠', 12)
                    else:
                        candidates = [c for c in legal_moves if c.suit != '♠' or c.number != 12]
                        if not candidates:
                            return Card('♠', 12)
                                  
                        return random.choice(self.largest_cards(candidates))
                else:
                    return random.choice(self.largest_cards(legal_moves))
            else:
                if Card('♠', 12) in legal_moves:
                    return Card('♠', 12)
                return random.choice(self.largest_cards(legal_moves))
        else:
                                  
            #playing cards that has a chance to give others
            candidates = []
            for suit, cards in cards_suit.items():
                if not cards:
                    continue
                min_card = min(cards, key=lambda c: self.card_rank[c])
                min_card_rank = self.card_rank[min_card]
                smallest_rank = [c for c in cards if self.card_rank[c] == min_card_rank]
                if len(smallest_rank) == len(cards):
                    continue
                candidates.extend([c for c in cards if self.card_rank[c] == min_card_rank])
            
            if candidates:
                return random.choice(candidates)
            
            return random.choice(legal_moves)
                                  
    def largest_cards(self, cards):
        max_card = max(cards, key=lambda c: self.card_rank[c])
        max_card_rank = self.card_rank[max_card]
        largest_rank = [c for c in cards if self.card_rank[c] == max_card_rank]

        return largest_rank
