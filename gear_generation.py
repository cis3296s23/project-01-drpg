import json
import random

class Weapon:
    def __init__(self):
        with open('weapons.json', 'r') as f:
            data = json.load(f)
            weapons = random.choice(data['weapons']) # chooses random weapon in json file
            self.name = f"{weapons}"
            self.damage = data['weapons'][weapons]['damage']
            self.speed = data['weapons'][weapons]['speed']

class Armor:
    def __init__(self):
        with open('armors.json', 'r') as f:
            data = json.load(f)
            armors = random.choice(data['armors'])  # chooses random armor in json file
            self.name = f"{armors}"
            self.protection = data['armors'][armors]['protection']
