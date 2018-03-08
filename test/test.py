import source.card as ca
import source.hand as ha
import source.deck as de
import source.player as pl
import source.table as ta

# Pytest tutorial:
# To be tested, every class name must start with Test, and every method name must start with test
# Do not forget to install pytest in advance either by calling
# pip install pytest
# or by calling
# pip install -r requirements.txt
#, which installs all the requirements and dependencies from the requirements.txt


class TestCard:
    card_ten_hearts = ca.Card(10, 3)
    card_five_hearts = ca.Card(5, 3)

    card_ten_diamonds = ca.Card(10, 2)
    card_ace_spade = ca.Card(1, 3)

    def test_value_of_card(self):
        assert TestCard.card_ace_spade.get_score()[0] == 1
        assert TestCard.card_ace_spade.get_score()[1] == 11
        assert TestCard.card_ten_hearts.get_score()[0] == 10

    def test_repr_of_card(self):
        assert TestCard.card_ace_spade.__repr__() == 'Ace of Hearts'

class TestDeck:

    def test_deck(self):
        dummy_deck = de.Deck(1)
        assert len(dummy_deck.unshuffled_deck) == 52
        assert len(dummy_deck.deck) == 52


class TestHand:

    def test_get_score(self):
        cards = [TestCard.card_ace_spade, TestCard.card_ten_hearts]
        h = ha.Hand(cards)
        assert h.get_score()[0] == 11
        assert h.get_score()[1] == 21
        assert h.can_split() == False

    def test_can_split(self):
        cards = [TestCard.card_ace_spade, TestCard.card_ten_hearts]
        h = ha.Hand(cards)
        assert h.can_split() == False

        cards = [TestCard.card_ace_spade, TestCard.card_ace_spade]
        h.cards = cards
        assert h.can_split() == True

    def test_busted(self):
        cards = [TestCard.card_ten_diamonds, TestCard.card_ten_hearts]
        h = ha.Hand(cards)
        assert h.is_busted() == False

        cards.append(TestCard.card_five_hearts)
        h.cards = cards
        assert h.is_busted() == True

class TestPlayer:
    dummy_player = pl.Player("dummy", 100)
    dummy_player_2 = pl.Player("dummy2", 50)

    def test_hit(self):
        cards = [TestCard.card_ten_diamonds, TestCard.card_ten_hearts]
        self.dummy_player.new_hand(ha.Hand(cards))
        self.dummy_player.hit(TestCard.card_five_hearts)
        assert len(self.dummy_player.hands[0].cards) == 3

    def test_split(self):
        cards = [TestCard.card_ten_diamonds, TestCard.card_ten_hearts]
        deck = de.Deck(1)
        self.dummy_player_2.new_hand(ha.Hand(cards))
        self.dummy_player_2.split(deck)

        assert self.dummy_player_2.is_splitted == True
        assert self.dummy_player_2.can_split() == False
        assert self.dummy_player_2.hands[0].cards[0].value == TestCard.card_ten_diamonds.value
        assert self.dummy_player_2.hands[1].cards[0].value == TestCard.card_ten_hearts.value

class TestTable:
    dummy_table = ta.Table()

    def test_clear_for_next_hands(self):
        self.dummy_table.add_player(TestPlayer.dummy_player)
        self.dummy_table.add_player(TestPlayer.dummy_player_2)
        self.dummy_table.clear_for_next_hands()
        assert TestPlayer.dummy_player.hands == []
        assert TestPlayer.dummy_player_2.hands == []

    def test_does_player_win_against_bank(self):
        cards = [TestCard.card_ten_diamonds, TestCard.card_ten_hearts]
        cards2 = [TestCard.card_ten_diamonds, TestCard.card_five_hearts]
        TestPlayer.dummy_player.new_hand(ha.Hand(cards))
        TestPlayer.dummy_player_2.new_hand(ha.Hand(cards2))
        assert TestPlayer.dummy_player.get_score() == [20]
        assert TestPlayer.dummy_player_2.get_score() == [15]
        self.dummy_table.add_player(TestPlayer.dummy_player)
        self.dummy_table.add_player(TestPlayer.dummy_player_2)
        assert self.dummy_table.does_player_win_against_bank(TestPlayer.dummy_player_2, 0, 0) == False
