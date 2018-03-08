from card import Card

class Hand:
	'''
	class representing a hand in the game. A hand is a list of cards.
	'''
	def __init__(self, cards):
		self.cards = cards

	def get_score(self):
		'''
		computes the possible scores of a hand. Each card's possible score is added to
		 each other in possible combinations. The more aces in a hand, the longer is the possible score list
		:return: a list of possible scores of a hand
		'''
		sum_score = [0]
		for card in self.cards:
			sum_list = []
			score_list = card.get_score()
			for s1 in score_list:
				for s2 in sum_score:
					sum_list.append(s1 + s2)
			sum_score = sum_list
		return sum_score

	def can_split(self):
		'''
		shows if the split action can be used by this hand
		:return:
		'''
		if len(self.cards) == 2 and self.cards[0].value == self.cards[1].value:
			return True
		else:
			return False

	def is_busted(self):
		'''
		shows if this hand is busted.
		:return:
		'''
		scores = self.get_score()
		for s in scores:
			if s <= 21:
				return False
		return True

	def __repr__(self):
		return str(self.cards)

