import random
from card import Card
from hand import Hand

class Deck:
    '''
    class representing the deck the game is played on. Might contain multiple standard card decks of 52.
    '''
    unshuffled_deck = [Card(value, suit_id) for value in range(1, 14) for suit_id in range(1, 5)]

    def __init__(self, num_decks=1):
        self.deck = self.unshuffled_deck * num_decks
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        '''
        deals the top card on the deck.
        :return: the top card on the deck
        '''
        return self.deck.pop()

    def deal_hand(self):
        '''
        deals the first card into a hand
        :return: a hand with one card
        '''
        return Hand([self.deal_card()])

