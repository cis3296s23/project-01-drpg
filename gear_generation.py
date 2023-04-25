import json
import random

class Weapon:
    def __init__(self):
        with open('weapons.json', 'r') as f:
            data = json.load(f)
            weapon = random.choice(data['weapons']) # chooses random weapon in json file
            self.name = weapon['name']
            self.damage = weapon['damage']
            self.speed = weapon['speed']
class Armor:
    def __init__(self):
        with open('armors.json', 'r') as f:
            data = json.load(f)
            armor = random.choice(data['armors']) # chooses random weapon in json file
            self.name = armor['name']
            self.protection = armor['protection']
