from character_manager import CharacterManager
import json
import random

class Creature:

    def __init__(self, lvl):
        with open('/Users/mikaya/Documents/GitHub/project-01-drpg/creatures.json', 'r') as f:
            data = json.load(f)
            creatures = random.choice(data['creatures'])
            self.name = f"{creatures}"
            self.symbol = creatures['symbol']
            self.character_manager = CharacterManager(
              str=creatures['str'] * lvl,
              end=creatures['end'] * lvl,
              dex=creatures['dex'] * lvl,
              hp=creatures['hp'] * lvl,
              xp=0,
              lvl=lvl
            )
