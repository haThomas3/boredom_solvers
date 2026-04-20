import random
import itertools


def create_deck(num_decks=1):
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = list(itertools.product(ranks, suits)) * num_decks
    random.shuffle(deck)
    return deck

def deal_initial_cards(deck, num_players):
    players_hands = {f'Player {i + 1}': [deck.pop(), deck.pop()] for i in range(num_players)}
    dealer_hand = [deck.pop(), deck.pop()]
    return players_hands, dealer_hand

def card_value(card):
    rank, _ = card
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11  # We'll adjust for aces later
    else:
        return int(rank)

def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    # Adjust for aces
    aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def dealer_action(deck, dealer_hand):
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    return dealer_hand

def play_interactive_blackjack(num_decks=1, initial_balance=1000):
    balance = initial_balance
    deck = create_deck(num_decks)
    print(f"Deck created with {len(deck)} cards.")

    while balance > 0:
        if len(deck) < 10:  # Reshuffle if deck is running low
            deck = create_deck(num_decks)
            print("Deck reshuffled.")

        bet = int(input(f"Your balance is ${balance}. Enter your bet: "))

        if bet > balance:
            print("You cannot bet more than your current balance.")
            continue

        player_hand, dealer_hand = deal_initial_cards(deck, 1)
        player_hand = player_hand['Player 1']

        print(f"Dealer's hand: [{dealer_hand[0]}, ('?', '?')]")

        # Player's turn
        player_hand, action = interactive_player_action(deck, player_hand)
        player_value = hand_value(player_hand)

        # Double the bet if double down action was chosen
        if action == 'd':
            bet *= 2

        # Check if the player has busted
        if player_value > 21:
            print("You busted! Dealer wins.")
            balance -= bet
        else:
            # Dealer's turn
            dealer_hand = dealer_action(deck, dealer_hand)
            dealer_value = hand_value(dealer_hand)

            # Reveal dealer's hand
            print(f"Dealer's hand: {dealer_hand}, Dealer's value: {dealer_value}")

            # Results
            if dealer_value > 21 or player_value > dealer_value:
                print("You win!")
                balance += bet
            elif player_value < dealer_value:
                print("Dealer wins.")
                balance -= bet
            else:
                print("It's a draw.")

        if balance <= 0:
            print("You're out of money! Game over.")
            break

    print(f"You finished with a balance of ${balance}.")

def interactive_player_action(deck, player_hand):
    while True:
        print(f"Your hand: {player_hand}, Current value: {hand_value(player_hand)}")
        action = input("Choose action: (h)it, (s)tand, (d)ouble down: ").lower()
        if action == 'h':
            player_hand.append(deck.pop())
            print(f"Your hand: {player_hand}, Current value: {hand_value(player_hand)}")  # Move print here
            if hand_value(player_hand) > 21:
                break
        elif action == 's':
            break
        elif action == 'd':
            player_hand.append(deck.pop())
            print(f"Your hand after doubling down: {player_hand}, Current value: {hand_value(player_hand)}")  # Move print here
            break
    return player_hand, action

if __name__ == '__main__':
    play_interactive_blackjack(6, 10000)
