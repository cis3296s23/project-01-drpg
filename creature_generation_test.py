import json
import random
from character_manager import CharacterManager
from creatures_generator import Creature







def main():
    creature = Creature(lvl=1)
    print(f"Name: {creature.name}")
    print(f"Symbol: {creature.symbol}")
    print(f"Strength: {creature.character_manager.str}")
    print(f"Endurance: {creature.character_manager.end}")
    print(f"Dexterity: {creature.character_manager.dex}")
    print(f"HP: {creature.character_manager.hp}")
    
    
    print(f"Level: {creature.character_manager.lvl}")
    print(f"Weapon: {creature.character_manager.weapon}")
    print(f"Armor: {creature.character_manager.armor}")

if __name__ == '__main__':
    main()


