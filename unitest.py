import json
import unittest
import dungeon_generator
from gear_generation import Armor, Weapon
from character_manager import CharacterManager
from creatures_generator import Creature
from boss_generator import BossDungeon, generate_boss_room_data, boss_process
from PIL import Image, ImageDraw, ImageFont
from map_image import generate_img, place_token
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)


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

class TestBossGenerator(unittest.TestCase):
    def test_generate_boss_room_data(self):
        size = 16
        lvl = 5
        boss_dungeon = generate_boss_room_data(size, lvl)
        self.assertIsNotNone(boss_dungeon)
        self.assertEqual(len(boss_dungeon), size + 1)  # because size is incremented by 1 if it's even

    def test_boss_process(self):
        size = 16
        lvl = 5
        boss_dungeon_obj = boss_process(size, lvl)
        self.assertIsInstance(boss_dungeon_obj, BossDungeon)
        self.assertIsNotNone(boss_dungeon_obj.ascii)

class TestMapImage(unittest.TestCase):
    def test_generate_img(self):
        dungeon_obj = dungeon_generator.DungeonObj(6, 5, 16)
        output_file = "output_imgs/test_dungeon.png"
        generate_img(dungeon_obj.ascii, output_file)
        
        self.assertTrue(os.path.isfile(output_file))
        os.remove(output_file)

    def test_place_token(self):
        original_image = "output_imgs/test_dungeon.png"
        token_image = "dungeon_imgs/Goblin.jpg"
        token_pos = (1, 1)
        modified_image = "output_imgs/test_dungeon_with_goblin.png"
        
        dungeon_obj = dungeon_generator.DungeonObj(6, 5, 16)
        generate_img(dungeon_obj.ascii, original_image)
        
        place_token(original_image, token_image, token_pos, modified_image)
        
        self.assertTrue(os.path.isfile(modified_image))
        os.remove(modified_image)
        os.remove(original_image)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestArmor('test_armor_creation'))
    suite.addTest(TestCreature('test_creature_creation'))
    suite.addTest(TestWeapon('test_weapon_creation'))
    suite.addTest(TestDungeonGen('test_merge_components'))
    suite.addTest(TestBossGenerator('test_generate_boss_room_data'))
    suite.addTest(TestBossGenerator('test_boss_process'))
    suite.addTest(TestMapImage('test_generate_img'))
    suite.addTest(TestMapImage('test_place_token'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
