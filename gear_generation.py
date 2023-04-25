import json
import random
import os
class Weapon:
    def __init__(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        weapons_file_path = os.path.join(project_root, 'weapons.json')
        with open(weapons_file_path) as f:
            data = json.load(f)
            weapon = random.choice(data['weapons']) # chooses random weapon in json file
            self.name = weapon['name']
            self.damage = weapon['damage']
            self.speed = weapon['speed']
class Armor:
    def __init__(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        armors_file_path = os.path.join(project_root, 'armors.json')
        with open(armors_file_path) as f:
            data = json.load(f)
            armor = random.choice(data['armors']) # chooses random weapon in json file
            self.name = armor['name']
            self.protection = armor['protection']
