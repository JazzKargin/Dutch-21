class Card:
    '''
    class representing a card of the deck. A card has one of the pre-defined values and suits.
    '''
    value_to_name = {1:"Ace", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven",8:"Eight", 9:"Nine", 10:"Ten", 11:"Jack", 12:"Queen", 13:"King"}
    suit_id_to_name = {1:"Clubs", 2:"Diamonds", 3:"Hearts", 4:"Spades"}

    def __init__(self, value, suit_id):
        self.value = value
        self.suit_id = suit_id

    def __repr__(self):
        return "%s of %s" % (self.value_to_name[self.value], self.suit_id_to_name[self.suit_id])

    def get_score(self):
        '''
        Computes the possible point score of a card according to the rules of the game.
        :return: a list of possible scores. Possibility comes from aces.
        '''
        if self.value <= 10:
            if self.value == 1:
                return [1, 11]
            else:
                return [self.value]
        else:
            painted = self.value - 10
            return [painted]

