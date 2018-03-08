from card import *
from hand import *
from deck import *
from player import *
from table import *

if __name__ == "__main__":
    print "Welcome to 21!\n"

    # Get from user how many players there are
    while True:
        try:
            number_of_players = int(raw_input("How many players would you like? Please enter a number.\n"))
            if number_of_players < 1:
                raise ValueError
            break
        except ValueError:
            print("Ops! That can't be the number of players. Try again...")

    print "\n"
    table = Table()
    # create Bank and players
    for p in xrange(0, number_of_players+1):
        if p == 0:
            p_name = "Bank"
        else:
            p_name = "Player " + str(p)
        table.add_player(Player(p_name))
        print "{} is created.".format(p_name)

    print "Each player has {} chips.".format(DEFAULT_CHIPS)

    # loop for round of hands. It goes on until all players lose all their chips.
    while len(table.players) > 1:
        # to follow ui easily
        enter = raw_input("New round of hands is beginning. Press Enter to continue.\n")

        # one deck for every 3 player
        number_of_decks = (len(table.players) -2) / 3 + 1
        print "The game will be played with {} deck(s).\n".format(number_of_decks)

        deck = Deck(number_of_decks)
        print "Deck is shuffled.\n"

        #Deal first cards
        for player in table.players:
            player.new_hand(deck.deal_hand())
        print "The first cards are dealt.\n"
        print "Taking turns to put in bets.\n"


        #Ask and receive first bets
        for p in xrange(1, len(table.players)): # Start from 1, Bank does not bet
            print "{}'s turn. Here is your hand:".format(table.players[p].name)
            print (table.players[p].hands[0])
            print "and current possible scores for it: {}".format(table.players[p].get_score(0))
            print "\n"
            # get first bets
            while True:
                try:
                    bet = int(raw_input("{}, you have {} chips left. How many chips do you bet? Please enter a number between 1 and {}.\n".format(table.players[p].name, table.players[p].chips, table.players[p].chips)))
                    if bet < 1 or bet > table.players[p].chips:
                        raise ValueError
                    break
                except ValueError:
                    print("\nOps! That can't be bet. Try again...")
            table.players[p].chips -= bet
            table.players[p].current_bet = bet
            print "\n"

        #Deal second cards
        for player in table.players:
            player.add_card_to_hand(deck.deal_card())
        print "The second cards are dealt.\n"

        print "Taking turns to play.\n"

        #Ask and receive action until all players are busted or standing.
        while not table.are_all_players_busted_or_standing():
            p = 1 # Bank does not play yet.
            while p < len(table.players):
                # busted players don't play
                if table.players[p].is_busted():
                    print "{} is busted. So skipping.\n".format(table.players[p].name)
                    p += 1
                    continue
                # once standing players don't play
                if table.players[p].is_standing():
                    print "{} is standing. So skipping.\n".format(table.players[p].name)
                    p += 1
                    continue

                # Let user know about whose turn it is, hand and scores
                print "{}'s turn. Here is your hand:".format(table.players[p].name)
                print (table.players[p].hands[0])
                print "and current possible scores for it: {}".format(table.players[p].get_score(0))
                if table.players[p].is_splitted:
                    # then print the second hand as well
                    print "This is your splitted hand:"
                    print (table.players[p].hands[1])
                    print "and current possible scores for it: {}".format(table.players[p].get_score(1))
                print "\n"

                # Get from player the action(s)
                while True:
                    if table.players[p].can_split():
                        # a split is possible
                        input_text = "{}, please choose one of the following actions. A split is also possible." \
                                     "\n(h)it\t(s)tand\ts(p)lit\n".format(table.players[p].name)
                    elif table.players[p].is_splitted:
                        # then this player plays two times, one hand each.
                        input_text = "{}, please choose one of the following actions for each of your hands. " \
                                     "One letter for your first hand and one letter for your splitted hand. " \
                                     "Two letters without space. " \
                                     "If one of your hands is busted or standing that action won't be applied." \
                                     "Another split is not possible.\n(h)it\t(s)tand\n".format(table.players[p].name)
                    else:
                        # this player cannot split and did not split.
                        input_text = "{}, please choose one of the following actions. A split is not possible.\n(h)it\t(s)tand\n".format(table.players[p].name)
                    try:
                        action = raw_input(input_text)
                        if table.players[p].is_splitted:
                            if not len(action) == 2:
                                raise ValueError
                        elif not len(action) == 1:
                            raise ValueError
                        for a in xrange(0, len(action)): #loop through each action a in action
                            if not action[a] == "h" and not action[a] == "s" and (table.players[p].can_split() and not action[a] == "p"):
                                raise ValueError
                        break
                    except ValueError:
                        print("\nOps! That is not a valid action. Try again...")

                there_is_split = False #if there is split then the current player will play again

                # loop through each action a in action to apply the action
                for a in xrange(0, len(action)):
                    if table.players[p].is_busted(a) or table.players[p].is_standing_l[a]:
                        # If one of your hands is busted or standing that action won't be applied.
                        continue
                    if action[a] == "h":
                        table.players[p].hit(deck.deal_card(), a)
                        print "{} hits.".format(table.players[p].name)

                        # print hand again
                        print "{}'s new hand:".format(table.players[p].name)
                        print (table.players[p].hands[0])
                        print "and current possible scores for it: {}".format(table.players[p].get_score(0))
                        if table.players[p].is_splitted:
                            # then print the second hand as well
                            print "This is her splitted hand:"
                            print (table.players[p].hands[1])
                            print "and current possible scores for it: {}".format(table.players[p].get_score(1))
                        print "\n"

                        if table.players[p].is_busted():
                            # busted after hitting.
                            print "{} is BUSTED! He is out until the end of this round of hands."\
                                .format(table.players[p].name)
                    elif action[a] == "s":
                        table.players[p].is_standing_l[a] = True
                        print "{} stands.".format(table.players[p].name)
                    else: # if action[a] == "p" and table.players[p].can_split()
                        try:
                            table.players[p].split(deck)
                        except ValueError:
                            print "ERROR: split is used without can_split. Skipping this player for now."
                        else:
                            print "{} splits. Then automatically hits for each hand. " \
                                  "Now {} plays again!".format(table.players[p].name, table.players[p].name)
                            there_is_split = True

                print "\n"
                if not there_is_split:
                    p += 1 #next player if no split

        # print player status
        print table

        # to follow ui easily
        enter = raw_input("Players are done with turns. Bank is going to play. Press Enter to continue.\n")

        #Make the bank play, only if there are players who are not busted.
        bank_status = 1 # 1: No other player standing, Bank wins. 2: Bank stands. 3: Bank is busted. Standing players win.
        if table.is_any_player_standing():
            # Bank's turn
            while min(table.players[0].get_score(0)) <= 16:
                # show bank's hand and score
                print "{}'s turn. Here is {}'s hand:".format(table.players[0].name, table.players[0].name)
                print (table.players[0].hands[0])
                print "and current possible scores for it: {}\n".format(table.players[0].get_score(0))

                # Bank hits.
                table.players[0].hit(deck.deal_card())
                print "{} hits.\n".format(table.players[0].name)

            print "{}'s turn. Here is Bank's hand:".format(table.players[0].name)
            print (table.players[0].hands[0])
            print "and current possible scores for it: {}\n".format(table.players[0].get_score(0))

            if table.players[0].is_busted():
                # Bank is busted
                bank_status = 3
                print "{} is BUSTED! She lost!".format(table.players[0].name)

            else:
                # Bank is standing
                table.players[0].is_standing_l[0] = True
                bank_status = 2
                print "{} stands. Checking scores...".format(table.players[0].name)
        else:
            # No need for the bank to play. She wins.
            bank_status = 1
            print "There is no need for {} to play. No player left standing. So, {} wins!".format(table.players[0].name, table.players[0].name)

        # to follow ui easily
        enter = raw_input("Bank is done with her turns. Press Enter to continue.\n")

        #Decide on who wins and give players chips accordingly.
        if bank_status == 1:
            for p in xrange(1, len(table.players)):
                table.players[p].get_busted()
        elif bank_status == 2:
            for p in xrange(1, len(table.players)):
                if table.players[p].is_standing():
                    for hand_id in xrange(0, len(table.players[p].hands)):
                        if table.does_player_win_against_bank(table.players[p], hand_id):
                            table.players[p].make_win()
                            print "{} wins against the {}!".format(table.players[p].name, table.players[0].name)
                        else:
                            table.players[p].get_busted()
                            print "{} loses against the {}!".format(table.players[p].name, table.players[0].name)

        elif bank_status == 3:
            for p in xrange(1, len(table.players)):
                if table.players[p].is_standing():
                    table.players[p].make_win()
                    print "Since the {} is busted, {} wins!".format(table.players[0].name, table.players[p].name)

        print "\nChips updated.\n"

        for p in xrange(1, len(table.players)):
            if table.players[p].chips <= 0:
                print "{} has no chips left. She is out of game.\n".format(table.players[p].name)

        # arrange players and hands for the next round of hands.
        table.remove_players_without_chips()
        table.clear_for_next_hands()

        print table

    # all players except the Bank is out.
    print "All players have lost their chips completely. The {} wins forever!".format(table.players[0].name)
	