import json
import itertools
import random
from generate_cards import generate_cards

def validate_cards(guilty_guest, guest_data_file, num_cards_per_guest):
    """Validates card distribution and analyzes suggestion statistics."""

    cards = generate_cards(guilty_guest, guest_data_file, num_cards_per_guest)

    with open(guest_data_file, 'r') as f:
        guest_data = json.load(f)

    if guilty_guest not in guest_data:
        raise ValueError(f"Guest '{guilty_guest}' not found in guest data.")

    guest_names = list(guest_data.keys())

    guest_names.remove(guilty_guest)  # Remove the guilty guest

    # 1. Check if the guilty party can be uniquely identified
    guilty_attributes = guest_data[guilty_guest]

    # Collect all cards dealt out into one list
    all_cards_dealt = []
    for card_set in cards.values():
        all_cards_dealt.extend(card_set)

    # Function to check if a guest could be the guilty party
    def is_possible_guilty(guest, attributes, cards_to_check):
        if guest == guilty_guest:
            return False #The guilty guest cannot have any cards about themselves
        for category, value in attributes.items():
            has_contradicting_card = False
            for other_guest, card_text in cards_to_check:
                if other_guest == guest:
                    card_category = card_text.split("'s ")[1].split(" is ")[0]
                    card_value = card_text.split(" is ")[1]
                    if card_category == category and card_value != value:
                        has_contradicting_card = True
                        break
            if has_contradicting_card:
                return False
        return True

    possible_suspects = []
    for guest, attributes in guest_data.items():
        if guest == guilty_guest:
            continue #Don't include the real guilty party in this check
        if is_possible_guilty(guest, guilty_attributes, all_cards_dealt):
            possible_suspects.append(guest)

    if len(possible_suspects) == 0:
        print("The guilty party can be uniquely identified through card elimination.")
    else:
        print("ERROR: The guilty party cannot be uniquely identified. The following guests also match the clues:")
        print(possible_suspects)
        print("Increase the number of cards per guest and run this script again.")
        return  # Stop further analysis if the cards are invalid

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

        for suggester in guest_names:
            for suspect in guest_names:
                if suspect != suggester:
                    suggestions_made.append((suggester, suspect))
        random.shuffle(suggestions_made)


        while True: #Continue suggesting until the guilty party is found
            current_suggestion = suggestions_made.pop()
            suggester = current_suggestion[0]
            suspect = current_suggestion[1]
            num_guesses_made[suggester] += 1

            if suspect == guilty_guest:
                suggestion_counts.append(num_guesses_made[suggester])
                break #Guilty party was found, end this simulation

            #Check if the suspect can be disproven using the cards
            if not is_possible_guilty(suspect, guilty_attributes, cards[suspect]):
                continue #Pretend the suspect disproved the suggestion and move to the next one
            else:
                suggestions_made.append(current_suggestion) #Put the suggestion back in the list and try it again later

    print("\nSuggestion Analysis (based on simulations):")
    print(f"  Minimum suggestions needed: {min(suggestion_counts)}")
    print(f"  Maximum suggestions needed: {max(suggestion_counts)}")
    print(f"  Average suggestions needed: {sum(suggestion_counts) / len(suggestion_counts):.2f}")

# Example usage (use the same values as in generate_cards.py):
guilty_guest_name = input("Enter the name of the guilty guest: ")
num_cards = int(input("Enter the number of cards per guest: "))
validate_cards(guilty_guest_name, "guest_data.json", num_cards)