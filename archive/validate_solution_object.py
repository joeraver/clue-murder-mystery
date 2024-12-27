import json
from operator import truediv

from card import Card
import random
from generate_cards import generate_cards
from guest import Guest


def validate_cards(guilty_guest, guest_data_file, num_cards_per_guest):
    """Validates card distribution and analyzes suggestion statistics."""

    cards = generate_cards("", guest_data_file, num_cards_per_guest)

    with open(guest_data_file, 'r') as f:
        guest_data = json.load(f)

    if guilty_guest not in guest_data:
        raise ValueError(f"Guest '{guilty_guest}' not found in guest data.")

    guest_names = list(guest_data.keys())
    # guest_names.remove(guilty_guest)
    guests = {}
    for guest_name in guest_names:
        guests[guest_name] = (Guest(guest_name, guest_names, cards[guest_name]))

    def card_exonerates(card):
        return card.value != guilty_attributes[card.category]


    #Check if the guilty party can be uniquely identified
    guilty_attributes: dict = guest_data[guilty_guest]

    def determine_best_suggestion(suggester: Guest):
        my_current_suspects = suggester.suspects_notebook
        return random.choice(my_current_suspects)


    def suggest(suggester: Guest, suggestee: Guest, suggested_culprit: str):
        suggestees_cards = suggestee.cards
        print(f"{suggester.name} is asking {suggestee.name} about {suggested_culprit}")
        suggester.notate_suggestion(suggestee.name, suggested_culprit)
        for card in suggestees_cards:
            if card.name == suggested_culprit:
                if card_exonerates(card):
                    suggester.remove_suspect_from_notebook(card.name)
                    for other_card in suggestees_cards:
                        if other_card is card:
                            break
                        try:
                            suggester.notate_suggestion(suggestee.name, other_card.name)
                            if card_exonerates(other_card):
                                print("got that info for free")
                                suggester.remove_suspect_from_notebook(other_card.name)
                        except:
                            continue
                    return card.name
        print("aww no matches")


    # 1. Each guest looks at their own cards and remove suspects from the list.

    for guest_name in guest_names:
        my_cards = cards[guest_name]
        for card in my_cards:
            if card_exonerates(card):
                guests[guest_name].remove_suspect_from_notebook(card.name)

    guests[guilty_guest].suspects_notebook.append(guilty_guest)


    # 2. Each guest makes suggestions to narrow things down.

    def a_culprit_has_been_determined():
        for g in guests.values():
            if len(g.suspects_notebook) == 1:
                return True
        return False

    if a_culprit_has_been_determined():
        print("Someone figured it out without needing any suggestions.")
        return


    # 2. Simulate suggestions to find min, max, and average

    suggestion_counts = []
    num_simulations = 1  # Run multiple simulations to get a good average

    for i in range(num_simulations):
        print("simulation " + str(i))
        #Create a set of random suggestions

        #Initialize the number of guesses each guest has made
        num_guesses_made = {}
        for guest in guest_names:
            num_guesses_made[guest] = 0

        while True: #Continue suggesting until the guilty party is found
            #Check if the suspect can be disproven using the cards
            if a_culprit_has_been_determined():
                print("YAY")
                break #Pretend the suspect disproved the suggestion and move to the next one

            for suggester in guest_names:
                num_guesses_made[suggester] += 1
                try:
                    suggestee, suggested_culprit = guests[suggester].get_next_suggestion()
                except:
                    print("something happened when getting next suggestion")
                suggest(guests[suggester], guests[suggestee], suggested_culprit)



        print(f"\nSuggestion Analysis (based on simulation {i}):")
        print(f"  Minimum suggestions needed: {min(num_guesses_made.values())}")
        print(f"  Maximum suggestions needed: {max(num_guesses_made.values())}")
        print(f"  Average suggestions needed: {sum(num_guesses_made.values()) / len(num_guesses_made)}")

    # print("\nSuggestion Analysis (based on simulations):")
    # print(f"  Minimum suggestions needed: {min(suggestion_counts)}")
    # print(f"  Maximum suggestions needed: {max(suggestion_counts)}")
    # print(f"  Average suggestions needed: {sum(suggestion_counts) / len(suggestion_counts):.2f}")

# Example usage (use the same values as in generate_cards.py):
guilty_guest_name = "Professor Plum" # = input("Enter the name of the guilty guest: ")
num_cards = 6 # = int(input("Enter the number of cards per guest: "))
validate_cards(guilty_guest_name, "guest_data.json", num_cards)