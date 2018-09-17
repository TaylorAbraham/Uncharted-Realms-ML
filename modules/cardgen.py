import numpy as np
import random
import json
from requests.exceptions import ConnectionError
from urllib.error import URLError
# Local libraries
import modules.namegen as namegen
import modules.imagegen as imagegen
import modules.mlnetwork as mlnetwork

csv_name = 'data/cards.csv'

HP_vals = [1]*3 + [2]*5 + [3]*5 + [4]*4 + [5]*3 + [6]*2 + [7]*2 + [8] + [9] + [10]
EFFs = ['Charge'] * 15 + ['Ward'] * 15

# This is a class so that the current_id is static
class IdGenerator:
    current_id = 0
    @classmethod
    def generate_id(cls):
        cls.current_id += 1
        return cls.current_id

# Generates a single new card
def generate_card():
    card_dict = {'NAME': [], 'POW': [], 'HP': [], 'IMG': [], 'EFF': []}
    names = []

    # Generate base card attributes, to be costed later

    # If we ran out of names, generate a new batch of 15
    if(names == []):
        try:
            names = namegen.generate_names()
        except ConnectionError:
            print("Could not connect to name generation service")

    if(names == []):
        # If name service could not be connected to
        name = "UNDEFINED"
    else:
        name = random.choice(names)
        names.remove(name)
    card_dict['NAME'].append(name)

    # HP is flat out a random int
    HP = random.choice(HP_vals)
    card_dict['HP'].append(HP)

    # Power is generated based on a gaussian distribution centred at the HP value
    POW = int(round(HP + np.random.normal(0, HP/2, 1)[0], 0))
    if(POW < 0):
        POW = 0
    card_dict['POW'].append(POW)

    try:
        img = imagegen.generate_image_url(name)
    except URLError:
        print("Could not connect to DeviantArt for image fetching")
        img = ""
    card_dict['IMG'].append(img)

    card_dict['EFF'].append(random.choice(EFFs))

    results = mlnetwork.predict_costs(card_dict)

    # Build the JSON for the response
    for index, card in results.iterrows():
        generated_card = {}
        generated_card['id'] = IdGenerator.generate_id()
        generated_card['name'] = card['NAME']
        generated_card['pow'] = card['POW']
        generated_card['hp'] = card['HP']
        generated_card['clk'] = card['CLK']
        generated_card['eff'] = card['EFF']
        generated_card['img'] = card['IMG']

    return generated_card
