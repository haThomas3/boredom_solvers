import random

# Define cards
CARD_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_SUITS = ['S', 'H', 'D', 'C']
COLORS = {'S': 'B', 'C': 'B', 'H': 'R', 'D': 'R'}


def create_deck():
    """Creates a full deck of cards."""
    return [[value, suit] for value in CARD_VALUES for suit in CARD_SUITS]


def pick_card(deck, used_cards=None):
    """
    Picks a random card and makes sure it has not already been used.
    """
    available = [card for card in deck if card not in (used_cards or [])]
    if not available:
        print("No more cards in the deck! Restarting the game...")
        return None
    return random.choice(available)


def get_card_value(card):
    """Returns the numeric index value of a card."""
    return CARD_VALUES.index(card[0])


def calculate_probability(deck, condition):
    """
    Calculates the probability of a specific condition.
    For example: above, below, or color.
    """
    return len([card for card in deck if condition(card)]) / len(deck)


def replay(deck, used_cards):
    """Resets the game state."""
    print("You lost! Restarting the game...")
    return create_deck(), []


def play():
    """Main game loop."""
    deck = create_deck()
    used_cards = []
    winners = []

    while True:
        print("Welcome to the game of glory!")

        if winners:
            print("Hall of Fame:", ", ".join(winners))

        # First card
        first_card = pick_card(deck, used_cards)
        used_cards.append(first_card)
        print(f"The first card is: {first_card[0]} {first_card[1]}")

        # First guess
        guess = input("Above or Below? (above/below): ").strip().lower()

        while True:
            second_card = pick_card(deck, used_cards)
            if get_card_value(second_card) != get_card_value(first_card):
                break  # Avoids equal card values

        used_cards.append(second_card)
        print(f"The second card is: {second_card[0]} {second_card[1]}")

        # Check first guess
        first_value = get_card_value(first_card)
        second_value = get_card_value(second_card)

        if guess == "above" and second_value <= first_value or \
                guess == "below" and second_value >= first_value:
            deck, used_cards = replay(deck, used_cards)
            continue

        # Second guess
        print("Nice! Next round.")
        guess = input("Above, Below, or Between? (above/below/between): ").strip().lower()

        third_card = pick_card(deck, used_cards)
        used_cards.append(third_card)
        print(f"The third card is: {third_card[0]} {third_card[1]}")

        min_value = min(first_value, second_value)
        max_value = max(first_value, second_value)
        third_value = get_card_value(third_card)

        if guess == "above" and third_value <= max_value or \
                guess == "below" and third_value >= min_value or \
                guess == "between" and not (min_value <= third_value <= max_value):
            deck, used_cards = replay(deck, used_cards)
            continue

        # Color guess
        print("Excellent! Let's test your luck further.")
        color_guess = input("Pick a color (R/B): ").strip().upper()

        fourth_card = pick_card(deck, used_cards)
        used_cards.append(fourth_card)
        print(f"The fourth card is: {fourth_card[0]} {fourth_card[1]}")

        if COLORS[fourth_card[1]] != color_guess:
            deck, used_cards = replay(deck, used_cards)
            continue

        # Suit guess
        shape_guess = input("Pick a suit (S/H/D/C): ").strip().upper()

        fifth_card = pick_card(deck, used_cards)
        used_cards.append(fifth_card)
        print(f"The fifth card is: {fifth_card[0]} {fifth_card[1]}")

        if fifth_card[1] != shape_guess:
            deck, used_cards = replay(deck, used_cards)
            continue

        # Number/value guess
        number_guess = input("Pick a value (2-10, J, Q, K, A): ").strip().upper()

        sixth_card = pick_card(deck, used_cards)
        used_cards.append(sixth_card)
        print(f"The sixth card is: {sixth_card[0]} {sixth_card[1]}")

        if sixth_card[0] != number_guess:
            deck, used_cards = replay(deck, used_cards)
            continue

        # Victory
        print("Congratulations! You've won this round!")
        winners.append(input("Enter your name to join the Hall of Fame: "))

        deck, used_cards = replay(deck, used_cards)


# Run the game
play()
