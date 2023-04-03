import unittest
from gear_generation import Weapon, Armor
import os

os.chdir('/Users/mikaya/Documents/GitHub/project-01-drpg/')

class TestWeaponAndArmor(unittest.TestCase):

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
