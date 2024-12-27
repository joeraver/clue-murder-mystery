import random

def distribute_cards(players, all_cards, cards_per_player):
    num_players = len(players)

    # Create a dictionary to track available cards for each player
    available_cards = {i: [] for i in range(num_players)}
    for card in all_cards:
        target_player_id = card[0]
        for player_index in range(num_players):
            if player_index + 1 != target_player_id: # Card is not about the current player
                available_cards[player_index].append(card)

    # Distribute cards to each player
    for player_index, player in enumerate(players):

        random.shuffle(available_cards[player_index]) # Shuffle available cards

        #Take cards if available, ensuring no duplicates
        while len(player.hand) < cards_per_player and available_cards[player_index]:
            card = available_cards[player_index].pop()
            if card not in player.hand:
                player.hand.append(card)

        # If player still needs cards after exhausting unique cards for them,
        # start taking cards from other players' pools, but still avoid duplicates
        if len(player.hand) < cards_per_player:

            other_player_indices = list(set(range(num_players)) - {player_index})
            random.shuffle(other_player_indices)

            for other_index in other_player_indices:
                random.shuffle(available_cards[other_index])
                while len(player.hand) < cards_per_player and available_cards[other_index]:
                    card = available_cards[other_index].pop()
                    if card not in player.hand and card[0] != player.player_id:
                        player.hand.append(card)


def print_game_state(players):
    for player in players:
        print(f"\nPlayer {player.player_id}:")
        print(f"  Attributes: {player.attributes}")
        print(f"  Hand:")
        for card in player.hand:
            print(f"    - Player {card[0]}, {card[1]}, Attribute Index {card[2]+1} is {card[3]}")

def main():
    num_players = 20  # Parameterized number of players
    num_categories = 2  # Parameterized number of categories
    num_attributes_per_category = 4  # Parameterized number of attributes per category
    cards_per_player = 6  # Parameterized number of cards per player

    players = create_players(num_players, num_categories, num_attributes_per_category)
    all_cards = generate_cards(players, cards_per_player)
    distribute_cards(players, all_cards, cards_per_player)
    print_game_state(players)

if __name__ == "__main__":
    main()