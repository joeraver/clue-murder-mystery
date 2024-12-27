import json
from operator import truediv

from card import Card
import random
from generate_cards import generate_cards

def validate_cards(guilty_guest, guest_data_file, num_cards_per_guest):
    """Validates card distribution and analyzes suggestion statistics."""

    cards = generate_cards("", guest_data_file, num_cards_per_guest)

    with open(guest_data_file, 'r') as f:
        guest_data = json.load(f)

    if guilty_guest not in guest_data:
        raise ValueError(f"Guest '{guilty_guest}' not found in guest data.")

    guest_names = list(guest_data.keys())
    # guest_names.remove(guilty_guest)

    def reset_card_distribution():

    def card_exonerates(card):
        return card.value != guilty_attributes[card.category]


    #Check if the guilty party can be uniquely identified
    guilty_attributes: dict = guest_data[guilty_guest]

    # Collect all cards dealt out into one list
    all_cards_dealt = []
    for card_set in cards.values():
        all_cards_dealt.extend(card_set)


    def determine_best_suggestee(suggester):
        other_guests = guest_names.copy().remove(suggester)
        return random.choice(guest_names)

    def suggest(suggester:str, suggestee: str, suggested_culprit: str):
        suggestees_cards: list[Card] = cards[suggestee]
        for card in suggestees_cards:
            if card.name == suggested_culprit:
                if card_exonerates(card):
                    remove_suspect_from_notebook(suggester, card.name)


    # 1. Each guest looks at their own cards and remove suspects from the list.

    def remove_suspects_based_on_my_cards(guest_name):
        my_cards = cards[guest_name]
        for card in my_cards:
            if card_exonerates(card):
                remove_suspect_from_notebook(guest_name, card.name)

    for guest in guest_names:
        remove_suspects_based_on_my_cards(guest)
        remove_suspect_from_notebook(guest, guest) # Remove myself as a culprit


    # 2. Each guest makes suggestions to narrow things down.

    def a_culprit_has_been_determined():
        for g in guest_notebooks:
            if len(guest_notebooks[g]) == 1:
                return True
        return False

    if a_culprit_has_been_determined():
        print("Someone figured it out without needing any suggestions.")
        return


    # 2. Simulate suggestions to find min, max, and average


    suggestion_counts = []
    num_simulations = 10  # Run multiple simulations to get a good average
    for i in range(num_simulations):
        print("simulation " + str(i))
        #Create a set of random suggestions
        suggestions_made = []
        #Initialize the number of guesses each guest has made
        num_guesses_made = {}
        for guest in guest_names:
            num_guesses_made[guest] = 0


        while not a_culprit_has_been_determined(): #Continue suggesting until the guilty party is found
            suggester = random.choice(guest_names)
            num_guesses_made[suggester] += 1
            suggestee = determine_best_suggestee(suggester)
            culprit = determine_best_suggestion(suggester)
            suggest(suggester, suggestee, culprit)

        average_suggestions_made = sum(num_guesses_made.values()) / len(num_guesses_made.values())

        print("\nCurrent Simulation Results:")
        print(f"  Minimum suggestions needed: {min(num_guesses_made.values())}")
        print(f"  Maximum suggestions needed: {max(num_guesses_made.values())}")
        print(f"  Average suggestions needed: {average_suggestions_made:.2f}")

        suggestion_counts.append(average_suggestions_made)

    print("\nSuggestion Analysis (based on simulations):")
    print(f"  Minimum suggestions needed: {min(suggestion_counts)}")
    print(f"  Maximum suggestions needed: {max(suggestion_counts)}")
    print(f"  Average suggestions needed: {sum(suggestion_counts) / len(suggestion_counts):.2f}")
# Example usage (use the same values as in generate_cards.py):
guilty_guest_name = "Professor Plum" # = input("Enter the name of the guilty guest: ")
num_cards = 11 # = int(input("Enter the number of cards per guest: "))
validate_cards(guilty_guest_name, "guest_data.json", num_cards)