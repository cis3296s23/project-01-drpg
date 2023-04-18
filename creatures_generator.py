from character_manager import CharacterManager
import json
import random
import os
class Creature:

     def __init__(self,lvl=1):
        project_root = os.path.dirname(os.path.abspath(__file__))
        creature_file_path = os.path.join(project_root, 'creatures.json')
        
        with open(creature_file_path) as f:
            data = json.load(f)
            creatures = random.choice(data["creatures"])
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
