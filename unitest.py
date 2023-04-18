import unittest
from gear_generation import Weapon, Armor
from character_manager import CharacterManager
from creatures_generator import Creature
import json
import os


class Test(unittest.TestCase):
   
    def test_weapon_creation(self):
        weapon = Weapon()
        self.assertIsNotNone(weapon.name)
        self.assertIsNotNone(weapon.damage)
        self.assertIsNotNone(weapon.speed)

    def test_armor_creation(self):
        armor = Armor()
        self.assertIsNotNone(armor.name)
        self.assertIsNotNone(armor.protection)

if __name__ == '__main__':
    unittest.main()
