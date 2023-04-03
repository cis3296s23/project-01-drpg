import json
import unittest
from character_manager import CharacterManager
from creatures_generator import Creature
import os

os.chdir('/Users/mikaya/Documents/GitHub/project-01-drpg/')

class TestCreature(unittest.TestCase):

    def test_creature_creation(self):
        creature = Creature(lvl=1)
        self.assertIsNotNone(creature.name)
        self.assertIsNotNone(creature.symbol)
        self.assertIsNotNone(creature.character_manager)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreature)
    unittest.TextTestRunner(verbosity=2).run(suite)



