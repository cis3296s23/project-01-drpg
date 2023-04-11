import json
import random

class Weapon:
    def __init__(self):
        with open('weapons.json') as f:
            data = json.load(f)
            weapons = data['weapons']
            weapon_data = random.choice(weapons)
            self.name = weapon_data['name']
            self.damage = weapon_data['damage']
            self.speed = weapon_data['speed']

class Armor:
    def __init__(self):
        with open('armors.json', 'r') as f:
            data = json.load(f)
            armors = random.choice(data['armors'])  # chooses random armor in json file
            self.name = f"{armors}"
            self.protection = data['armors'][armors]['protection']
