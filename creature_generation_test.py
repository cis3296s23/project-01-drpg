import json
import unittest
from creatures_generator import Creature

class TestCreature(unittest.TestCase):

    def test_creature_creation(self):
        creature = Creature(lvl=1)
        self.assertIsNotNone(creature.name)
        self.assertIsNotNone(creature.symbol)
        self.assertIsNotNone(creature.character_manager)
        print(creature.name)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreature)
    unittest.TextTestRunner(verbosity=2).run(suite)



