import json
import unittest
from gear_generation import Weapon
import os

os.chdir('/Users/mikaya/Documents/GitHub/project-01-drpg/')
class Test(unittest.TestCase):
    def test_weapon_creation(self):
        weapon = Weapon()
        self.assertIsNotNone(weapon.name)
        self.assertIsNotNone(weapon.damage)
        self.assertIsNotNone(weapon.speed)
if __name__ == '__main__':
    unittest.main()