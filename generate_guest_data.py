import json
import random

def generate_guest_data(names_file, output_file):
    """Generates unique attribute combinations for each guest and saves to JSON."""

    with open(names_file, 'r') as f:
        guest_names = [line.strip() for line in f]

    attributes = {
        "Work": ["US Government", "Weapons Manufacturing", "Broadway"],
        "Favorite Food": ["Monkey's Brains", "Crepes Suzette", "Beef Wellington"],
        "Favorite Drink": ["Dirty Martini", "Mint Julep", "Manhattan"],
        "Where they live": ["Washington D.C.", "Connecticut", "Paris"]
    }

    all_combinations = []
    for work in attributes["Work"]:
        for food in attributes["Favorite Food"]:
            for drink in attributes["Favorite Drink"]:
                for location in attributes["Where they live"]:
                    all_combinations.append({
                        "Work": work,
                        "Favorite Food": food,
                        "Favorite Drink": drink,
                        "Where they live": location
                    })

    random.shuffle(all_combinations)  # Randomize to ensure uniqueness

    guest_data = {}
    for i, name in enumerate(guest_names):
        guest_data[name] = all_combinations[i]

    with open(output_file, 'w') as outfile:
        json.dump(guest_data, outfile, indent=4)

# Example usage:
generate_