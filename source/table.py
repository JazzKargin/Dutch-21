from player import Player

class Table:
        '''
        class representing the game table. Holds the players including the Bank. Handles adding/removing players
        identifying winners, etc.
        '''
        def __init__(self):
                self.players = []
        def add_player(self, player):
                self.players.append(player)
        def are_all_players_busted_or_standing(self):
                '''
                called to check if the turns of the players has ended.
                :return: if all players are either busted or standing
                '''
                for p in xrange(1, len(self.players)):
                        if not self.players[p].is_busted_or_standing():
                                return False
                return True

        def is_any_player_standing(self):
                '''
                called to check if Bank should play or not
                :return: if any player left standing
                '''
                for p in xrange(1, len(self.players)):
                        if self.players[p].is_standing():
                                return True
                return False

        def does_player_win_against_bank(self, player, hand_id, bank_player_id=0):
                '''
                if the player satisfies the particular condition to win
                :param player: player to compare scores against the bank
                :param hand_id: which hand of that player
                :param bank_player_id: which player is the Bank in the list of players. Defaults to 0.
                :return: if player wins or not
                '''
                player_scores = player.get_score(hand_id)
                bank_scores = self.players[bank_player_id].get_score(0)
                best_ps = 0
                best_bs = 0
                # find best score of player
                for ps in player_scores:
                        if ps <= 21:
                                if ps > best_ps:
                                        best_ps = ps
                # find best score of bank
                for bs in bank_scores:
                        if bs <= 21:
                                if bs > best_bs:
                                        best_bs = bs
                if best_ps > best_bs:
                        return True
                else:
                        return False

        def clear_for_next_hands(self):
                for player in self.players:
                        player.clear_for_next_hands()

        def remove_players_without_chips(self):
                '''
                called at the end of a round of hands to remove players who has finished up all their chips.
                :return: none
                '''
                self.players = [player for player in self.players if player.chips > 0]

        def __repr__(self):
                output = "Current Status of All Players\n------\n"
                for player in self.players:
                        output += "{}\n".format(player)
                return output

