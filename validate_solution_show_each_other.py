import json
from operator import truediv

from card import Card
import random
from generate_cards import generate_cards
from guest import Guest


def validate_cards(guilty_guest, guest_data_file, num_cards_per_guest):
    """Validates card distribution and analyzes suggestion statistics."""

    with open(guest_data_file, 'r') as f:
        guest_data = json.load(f)

    if guilty_guest not in guest_data:
        raise ValueError(f"Guest '{guilty_guest}' not found in guest data.")

    guest_names = list(guest_data.keys())
    # guest_names.remove(guilty_guest)
    guests = {}

    #Check if the guilty party can be uniquely identified
    guilty_attributes: dict = guest_data[guilty_guest]

    def initialize_guests_and_cards():
        cards = generate_cards("", guest_data_file, num_cards_per_guest)
        for guest_name in guest_names:
            guests[guest_name] = Guest(guest_name, guest_names, cards[guest_name])
        for guest in guests.values():
            guest.look_at_own_cards(guilty_attributes)
        guests[guilty_guest].suspects_notebook.append(guilty_guest)


    def suggest(suggester: Guest, suggestee: Guest, suggested_culprit: str):
        suggestees_cards = suggestee.cards
        suggester.notate_suggestion(suggestee.name, suggested_culprit)
        for card in suggestees_cards:
            if card.name == suggested_culprit:
                if card.exonerates(guilty_attributes):
                    suggester.remove_suspect_from_notebook(card.name)
                    for other_card in suggestees_cards:
                        if other_card is card:
                            break
                        try:
                            if a_culprit_has_been_determined(me = suggester):
                                break
                            suggester.notate_suggestion(suggestee.name, other_card.name)
                            if other_card.exonerates(guilty_attributes):
                                suggester.remove_suspect_from_notebook(other_card.name)
                        except:
                            continue
                    return card.name

    # Each guest makes suggestions to narrow things down.

    def a_culprit_has_been_determined(me = None):
        if me is not None:
            if len(guest.suspects_notebook) == 1:
                return True
        for g in guests.values():
            if len(g.suspects_notebook) == 1:
                return True
        return False

    if a_culprit_has_been_determined():
        print("Someone figured it out without needing any suggestions.")
        return


    # Simulate suggestions to find min, max, and average

    suggestion_counts = []
    num_simulations = 100  # Run multiple simulations to get a good average

    for i in range(num_simulations):
        print("simulation " + str(i))
        #Create a set of random suggestions
        initialize_guests_and_cards()
        #Initialize the number of guesses each guest has made
        num_guesses_made = {}
        for guest in guest_names:
            num_guesses_made[guest] = 0

        while not a_culprit_has_been_determined(): #Continue suggesting until the guilty party is found

            for suggester in guest_names:
                if a_culprit_has_been_determined():
                    break
                num_guesses_made[suggester] += 1
                try:
                    suggestee, suggested_culprit = guests[suggester].get_next_suggestion()
                except:
                    print("something happened when getting next suggestion")
                suggest(guests[suggester], guests[suggestee], suggested_culprit)

        average_suggestions_made = sum(num_guesses_made.values()) / len(num_guesses_made.values())
        print(f"\nSuggestion Analysis (based on simulation {i}):")
        print(f"  Minimum suggestions needed: {min(num_guesses_made.values())}")
        print(f"  Maximum suggestions needed: {max(num_guesses_made.values())}")
        print(f"  Average suggestions needed: {average_suggestions_made}")
        suggestion_counts.append(average_suggestions_made)

    print("\nSuggestion Analysis (based on simulations):")
    print(f"  Minimum suggestions needed: {min(suggestion_counts)}")
    print(f"  Maximum suggestions needed: {max(suggestion_counts)}")
    print(f"  Average suggestions needed: {sum(suggestion_counts) / len(suggestion_counts):.2f}")

# Example usage (use the same values as in generate_cards.py):
guilty_guest_name = "Professor Plum" # = input("Enter the name of the guilty guest: ")
num_cards = 6 # = int(input("Enter the number of cards per guest: "))
validate_cards(guilty_guest_name, "guest_data.json", num_cards)