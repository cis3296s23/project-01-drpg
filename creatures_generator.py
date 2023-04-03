from character_manager import CharacterManager
import json
import random

class Creature:
    def __init__(self, lvl):
        self.character_manager = CharacterManager()
        with open('creatures.json', 'r') as f:
            data = json.load(f)
            creatures = random.choice(data['creatures'])
            self.name = f"{creatures['adjective']} {creatures['noun']}"
            self.symbol = creatures['symbol']
            self.hp = creatures['hp'] * lvl
            self.attack = creatures['attack'] * lvl
            self.defense = creatures['defense'] * lvl
