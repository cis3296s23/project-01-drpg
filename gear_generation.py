import json
import random
import os

class Weapon:
    def __init__(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        weapons_file_path = os.path.join(project_root, 'weapons.json')
        
        with open(weapons_file_path) as f:
            data = json.load(f)
            weapons = data['weapons']
            weapon_data = random.choice(weapons)
            self.name = weapon_data['name']
            self.damage = weapon_data['damage']
            self.speed = weapon_data['speed']

class Armor:
    def __init__(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        armors_file_path = os.path.join(project_root, 'armors.json')
        
        with open(armors_file_path) as f:
            data = json.load(f)
            armors = data['armors']
            armor_data = random.choice(armors)
            self.name = armor_data['name']
            self.protection = armor_data['protection']

