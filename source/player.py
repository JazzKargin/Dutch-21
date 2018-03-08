import copy
from hand import Hand

DEFAULT_CHIPS = 20

class Player:
    '''
    class representing a player in the game. A player is a collection of hands changing every play,
    has also a name and chips to bet.
    '''
    def __init__(self, name="Player 1", chips=DEFAULT_CHIPS):
        self.name = name
        self.chips = chips
        self.current_bet = 0
        self.hands = []
        self.is_splitted = False
        self.is_standing_l = [False]

    def new_hand(self, hand):
        self.hands.append(hand)

    def add_card_to_hand(self, card, hand_id=0):
        self.hands[hand_id].cards.append(card)

    def hit(self, card, hand_id=0):
        '''
        called when player chooses to hit after second or more cards, meaning that she got dealt another card.
        :param card: the dealt card from the deck to be added to player's hand
        :param hand_id: which hand of the player is hitting. If she had splitted before, she has two hands.
        :return: none
        '''
        self.hands[hand_id].cards.append(card)

    def is_busted(self, hand_id=0):
        if self.hands == []:
            return False
        return self.hands[hand_id].is_busted()

    def is_busted_or_standing(self):
        for hand_id in xrange(0, len(self.hands)):
            if not self.is_busted(hand_id) and not self.is_standing_l[hand_id]:
                return False
        return True

    def is_standing(self):
        if self.hands == []:
            return False
        for hand_id in xrange(0, len(self.hands)):
            if not self.is_standing_l[hand_id]:
                return False
        return True

    def can_split(self):
        if self.is_splitted:
            return False
        else:
            return self.hands[0].can_split()

    def split(self, deck):
        '''
        called when player chooses to hit after receiving second card and if she is able to split.
        Removes the second card from the hand and adds to a new hand.
        :param deck: deck to deal cards after split. Because has to hit after split.
        :return: none
        '''
        if self.can_split():
            second_card = copy.deepcopy(self.hands[0].cards[1])
            del self.hands[0].cards[1]
            self.new_hand(Hand([second_card]))
            self.is_splitted = True
            self.is_standing_l.append(False)
            # has to hit after split
            self.hit(deck.deal_card(), 0)
            self.hit(deck.deal_card(), 1)
        else:
            raise ValueError('split is used without can_split')

    def get_score(self, hand_id=0):
        if self.hands == []:
            return [0]
        return self.hands[hand_id].get_score()

    def get_busted(self):
        # chips lost already
        self.current_bet = 0

    def make_win(self):
        self.chips += self.current_bet*2 # winning rate: 2 times of the bet.
        self.current_bet = 0

    def clear_for_next_hands(self):
        '''
        called when a round of hands has ended, to start new round of hands.
        :return: none
        '''
        self.current_bet = 0
        self.hands = []
        self.is_splitted = False
        self.is_standing_l = [False]

    def __repr__(self):
        player_str = self.name
        if self.is_busted():
            player_str += " BUSTED"
        elif self.is_standing():
            player_str += " STANDING"
        return "Player: {}\nChips left: {}\nCurrent Bet: {}\nCards: {}\nScore: {}\n".format(player_str, self.chips, self.current_bet, self.hands, self.get_score())

