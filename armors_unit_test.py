import json
import unittest
from gear_generation import Armor
import os

os.chdir('/Users/mikaya/Documents/GitHub/project-01-drpg/')

class TestArmor(unittest.TestCase):
    def test_armor_creation(self):
        armor = Armor()
        self.assertIsNotNone(armor.name)
        self.assertIsNotNone(armor.protection)

if __name__ == '__main__':
    unittest.main()