import unittest
import dungeon_generator

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

if __name__ == "__main__":
    unittest.main()