"""
File:    blackjack.py
Author:  Mofe Okonedo
E-mail:  eokoned1@umbc.edu
Description:
Game of Black Jack with a special twist!
"""

import random  # initializing random

SUITS = ['\u2660', '\u2663', '\u2661', '\u2662']  # UNICODE for the SUIT
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


def create_deck(num_decks, num_retrievers):  # creates the deck
    retriever_card_counter = 0
    deck = []  # empty list
    for i in range(num_decks):  # iterates through the number of decks
        for suit in SUITS:
            for rank in RANKS:
                card = (rank, suit)  # sets card into a tuple so it can't be changed
                deck.append(card)
        for j in range(num_retrievers):
            deck[retriever_card_counter] = ('R', '*')
            retriever_card_counter += 1

    return deck


def shuffle_deck(deck):
    random.shuffle(deck)  # we shuffle the deck by using the random import


def deal_card(deck):
    card = deck.pop(0)
    return card


def compute_hand_value(hand):
    num_aces = 0  # initialize the number of aces, hand value and retriever count
    hand_value = 0
    retriever_count = 0

    for card in hand:
        if card[0] == 'A':  # The first time we will check if it has an Ace to increment by 1
            num_aces += 1

    for card in hand:
        if card[0] in {'J', 'Q', 'K'}:  # if that card face is a Jack, Queen or King it's worth 10 so we increment it
            # by that
            hand_value += 10
        elif card[0] == 'A':
            hand_value += 11  # increment the hand_value by 11 if an Ace is found
        elif card[0] == 'R':
            retriever_count += 1
            return 21
        else:
            hand_value += int(card[0])

    while hand_value > 21 and num_aces > 0:  # while the hand value is less than 21 and anyone has any aces subtract
        # that the hand value by 10 and subtract the number of aces by 1
        hand_value -= 10
        num_aces -= 1

    while retriever_count > 0 and hand_value > 21:
        hand_value -= 10
        retriever_count -= 1

    if 'A' in [card[0] for card in hand] and hand_value + 10 <= 21:
        hand_value += 10

    return hand_value


def play_player_turn(deck, player_hand): # function that handles the players turn
    while True:
        print(f"Your hand is: ", end="")
        for card in player_hand:
            print(f"{card[0]}{card[1]} ", end="")  # prints the players suits, ranks
        hand_value = compute_hand_value(player_hand)
        print(f"and has value {hand_value}")
        if hand_value > 21:  # if the players hand value exceeds 21, they automatically bust
            print("You have busted, sorry.")
            return 'bust'
        elif hand_value == 21:
            print("Player Black Jack!")
            return
        choice = input("What would you like to do? [hit, stay] ").strip().lower()  # input validation
        if choice == 'hit':
            player_hand.append(deal_card(deck)) # append a random card from the deck into the players hand
        elif choice == 'stay':
            print(f"Your hand is: ", end="") # if you enter stay then say what the players hand is
            for card in player_hand:
                print(f"{card[0]}{card[1]} ", end="")
            print(f"and has value {hand_value}")
            return 'stay'
        else:
            print("Invalid choice. Please enter 'hit' or 'stay'.") # for if the user does not enter hit or stay


def play_dealer_turn(deck, dealer_hand): # dealer function
    dealer_hand_string = ''
    for element in dealer_hand:
        dealer_hand_string += "".join(list(element)) + " " # join the list of elements together

    print(f"The Dealer's hand is {dealer_hand_string} with a value of {compute_hand_value(dealer_hand)}")
    while compute_hand_value(dealer_hand) < 17: # while the dealer hand value is less than 17 the dealer will draw
        dealer_hand.append(deal_card(deck))
        dealer_hand_string += "".join(dealer_hand[-1]) + " "
        print(f"Dealer hits: {dealer_hand_string} with a value of {compute_hand_value(dealer_hand)}")
    if compute_hand_value(dealer_hand) > 21: # if the dealers hand value goes over 21 they bust
        print(f"Dealer busts! Dealer's hand value is {compute_hand_value(dealer_hand)}")
        return 'bust'
    elif compute_hand_value(dealer_hand) == 21: # if the dealer gets 21 they get a Black Jack
        print("Dealer Black Jack!")
        return
    else:
        print(f"Dealer stays with hand value {compute_hand_value(dealer_hand)}") # if the dealer stays show the hand
        # value
        return 'stay'


def game_loop(num_decks, num_retrievers):  # play game function that runs the game
    play_again = True

    deck = create_deck(num_decks, num_retrievers)
    shuffle_deck(deck)
    quatloos = 100 # our quatloos starts with 100
    while play_again: # while the loop is true tell the user how many quatloos they have and have them bet,
        # if they bet more quatloos than what they have then prompt them to bet an amount that is the same or less
        print(f"You have {quatloos} quatloos, how many would you like to bet?", end=' ')
        bet = int(input())
        if bet > quatloos:
            print("You don't have enough quatloos for that bet. Try again.")
        else:
            player_hand = [deal_card(deck), deal_card(deck)]
            dealer_hand = [deal_card(deck), deal_card(deck)]
            print(f"Dealer's card is: \u2588\u2588 {dealer_hand[0][0]}{dealer_hand[0][1]}") # unicode that hides the
            # dealers two cards so that the player has to guess whether to hit or stay
            player_status = play_player_turn(deck, player_hand)
            if player_status == 'bust': # if the player bust they lose how many quatloos they bet
                quatloos -= bet
            else:
                dealer_status = play_dealer_turn(deck, dealer_hand)
                if dealer_status == 'bust': # if the dealer busts the player wins meaning you gain however many
                    # quatloos was bet
                    quatloos += bet
                else:
                    if compute_hand_value(player_hand) > compute_hand_value(dealer_hand): # if our hand value is more
                        # than the dealers hand value we win and gain however many quatloos we bet
                        print("You win!")
                        quatloos += bet
                    elif compute_hand_value(player_hand) < compute_hand_value(dealer_hand):
                        print("Dealer wins!") # if our hand value is less than the dealers then we lose
                        quatloos -= bet
                    else:
                        print("It's a tie!") # if it's none of these conditions it's a tie and we don't lose or gain
        play = input("Would you like to play again? [y/yes] ")
        if play.lower().strip() not in ["y", "yes"] or quatloos <= 0: # if we don't enter y or yes in the list then
            # we don't play again
            play_again = False # making play again false and the while loop not run
            print(f"You ended the game with {quatloos} quatloos") # tells us how many quatloos we ended the game with


if __name__ == '__main__': # main function
    play_again = True

    print("How many decks of cards would you like to use?", end=' ')
    num_decks = int(input())
    print("What seed would you like to use?", end=' ')
    seed = input()
    random.seed(seed)
    print("How many Retriever cards would you like to add?", end=' ')
    num_retrievers = int(input())
    game_loop(num_decks, num_retrievers)
