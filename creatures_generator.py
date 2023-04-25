from character_manager import CharacterManager
import json
import random

class Creature:

    def __init__(self, lvl, demon=False):
        with open('creatures.json', 'r') as f:
            data = json.load(f)
            if not demon:
              creatures = random.choice(data["creatures"][:-1])
            else:
              # select demon from creatures.json
              creatures = data["creatures"][-1]
            self.name = creatures['name']
            self.symbol = creatures['symbol']
            self.character_manager = CharacterManager(
              str=creatures['str'] * lvl,
              end=creatures['end'] * lvl,
              dex=creatures['dex'] * lvl,
              hp=creatures['hp'] * lvl,
              maxHP=creatures['maxHP'] * lvl,
              xp=0,
              lvl=lvl
            )
    
    def __str__(self) -> str:
        return self.symbol
