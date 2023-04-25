import json
import unittest
from gear_generation import Armor, Weapon
from character_manager import CharacterManager
from creatures_generator import Creature

import dungeon_generator



class TestArmor(unittest.TestCase):
    def test_armor_creation(self):
        armor = Armor()
        self.assertIsNotNone(armor.name)
        self.assertIsNotNone(armor.protection)

class TestCreature(unittest.TestCase):
    def test_creature_creation(self):
        creature = Creature(lvl=1)
        self.assertIsNotNone(creature.name)
        self.assertIsNotNone(creature.symbol)
        self.assertIsNotNone(creature.character_manager)

class TestWeapon(unittest.TestCase):
    def test_weapon_creation(self):
        weapon = Weapon()
        self.assertIsNotNone(weapon.name)
        self.assertIsNotNone(weapon.damage)
        self.assertIsNotNone(weapon.speed)

class TestDungeonGen(unittest.TestCase):
    
    def test_merge_components(self):
        nodes = [
            dungeon_generator.Node(0,0,1),
            dungeon_generator.Node(0,0,2),
            dungeon_generator.Node(0,0,2),
            dungeon_generator.Node(0,0,2),
            dungeon_generator.Node(0,0,3),
            dungeon_generator.Node(0,0,3),
            dungeon_generator.Node(0,0,4),
            dungeon_generator.Node(0,0,4),
            dungeon_generator.Node(0,0,4),
            dungeon_generator.Node(0,0,5),
            dungeon_generator.Node(0,0,5),
            dungeon_generator.Node(0,0,5),
        ]
        edges = [
            # 1, 2
            dungeon_generator.Edge(nodes[0], nodes[1]),
            # 3, 5
            dungeon_generator.Edge(nodes[4], nodes[9]),
            # 4, 2
            # dungeon_generator.Edge(nodes[6], nodes[2]),
            # 3, 4
            dungeon_generator.Edge(nodes[4], nodes[6]),
        ]
        c = dungeon_generator.DungeonObj(4, 4, 16)
        e = c._boruvka_update_node_ids(edges, nodes)
        # result should be in two groups: (1,2,4) and (3, 5)
        for j in e:
            print(str(j))



def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestArmor('test_armor_creation'))
    suite.addTest(TestCreature('test_creature_creation'))
    suite.addTest(TestWeapon('test_weapon_creation'))
    suite.addTest(TestDungeonGen('test_merge_components'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
