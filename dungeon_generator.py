import random
import math

class Node:
    def __init__(self, x, y, id) -> None:
        self.x = x
        self.y = y
        self.id = id

    def is_equal(self, node2) -> bool:
        if (self.x == node2.x) and (self.y == node2.y):
            return True
        return False
    
    def update_id(self, new_id):
        self.id = new_id
    
    def __str__(self) -> str:
        return "({},{}: {})".format(self.x, self.y, self.id)

class Edge:
    def __init__(self, n1, n2) -> None:
        self.nodes = [n1, n2]
        self.calc_weight()

    def calc_weight(self):
        xlen = self.nodes[0].x - self.nodes[1].x
        ylen = self.nodes[0].y - self.nodes[1].y
        self.weight = math.pow(xlen, 2) + math.pow(ylen, 2)

    def is_equal(self, edge2):
        if ((self.nodes[0].is_equal(edge2.nodes[0]) and 
                self.nodes[1].is_equal(edge2.nodes[1])) or
                (self.nodes[0].is_equal(edge2.nodes[1]) and 
                self.nodes[1].is_equal(edge2.nodes[0]))):
            return True
        return False

    def __str__(self) -> str:
        return str(self.nodes[0]) + " " + str(self.nodes[1]) + " : " + str(self.weight )

class Cells:
    def __init__(self) -> None:
        self.empty = '░'
        self.floor = '█'
        self.chest = '▣'
        self.door = '◫'

class Room:
    def __init__(self, 
                 corner_x, 
                 corner_y, 
                 size_x, 
                 size_y,
                 id) -> None:
        self.corner_x = corner_x
        self.corner_y = corner_y
        self.size_x = size_x
        self.size_y = size_y
        self.id = id


class DungeonObj:
    def __init__(self, 
                 num_rooms, 
                 max_room_size,
                 dungeon_size) -> None:
        self.num_rooms = num_rooms
        self.max_room_size = max_room_size
        self.dungeon_size = dungeon_size
        self.buffer = 1 # NOTE: buffer between rooms
        self.cells = Cells()
        self.rooms = []
        self.final_edges = []
        
        # fill new dungeon with blanks
        self.ascii = [
            [self.cells.empty for i in range(self.dungeon_size)] for j in range(self.dungeon_size)
        ]


    def __str__(self):
        string = ""
        for i in range(self.dungeon_size):
            for j in range(self.dungeon_size):
                string += self.ascii[i][j]
            string += "\n"
        return string


    def place_rooms(self):
        pass
        # iterate through num_rooms
        for i in range(self.num_rooms):
            valid = False
            while not valid:
                # generate room size in appropriate ranges
                size_x = random.randint(2, self.max_room_size)
                size_y = random.randint(2, self.max_room_size)
                
                # generate 4th quadrant corner
                corner_x = random.randint(0, self.dungeon_size-2)
                corner_y = random.randint(0, self.dungeon_size-2)
                
                # check that this is a valid placement
                valid = True
                if (corner_y+size_y+self.buffer > self.dungeon_size) or (corner_x+size_x+self.buffer > self.dungeon_size):
                    valid = False
                    continue
                for j in range(corner_y-self.buffer, corner_y+size_y+self.buffer):
                    for k in range(corner_x-self.buffer, corner_x+size_x+self.buffer):
                        if self.ascii[j][k] != self.cells.empty:
                            valid = False

            # place room, add to list
            self.rooms.append(Room(corner_x, corner_y, size_x, size_y, i))

            for j in range(corner_y, corner_y+size_y):
                    for k in range(corner_x, corner_x+size_x):
                        self.ascii[j][k] = self.cells.floor


    def calc_boruvka(self):
        all_nodes = []
        open_edges = []
        closed_edges = []
        
        # create nodes
        check_index = 0
        for room in self.rooms:
            for i in range(room.corner_y, room.corner_y+room.size_y):
                # NOTE: I know this sucks but I can't think of where a function would go
                
                # left side
                add_node = True
                new_node = Node(room.corner_x, i, room.id)
                for j in all_nodes[check_index:]:
                    if new_node.is_equal(j):
                        add_node = False
                if add_node:
                    all_nodes.append(new_node)
                
                # right side
                add_node = True
                new_node = Node(room.corner_x+room.size_x-1, i, room.id)
                for j in all_nodes[check_index:]:
                    if new_node.is_equal(j):
                        add_node = False
                if add_node:
                    all_nodes.append(new_node)
            
            for i in range(room.corner_x, room.corner_x+room.size_x):
                
                # top row
                add_node = True
                new_node = Node(i, room.corner_y, room.id)
                for j in all_nodes[check_index:]:
                    if new_node.is_equal(j):
                        add_node = False
                if add_node:
                    all_nodes.append(new_node)
                
                # bottom row
                add_node = True
                new_node = Node(i, room.corner_y+room.size_y-1, room.id)
                for j in all_nodes[check_index:]:
                    if new_node.is_equal(j):
                        add_node = False
                if add_node:
                    all_nodes.append(new_node)
            
        # create edges between nodes
        for node1 in all_nodes:
            for node2 in all_nodes:
                if node1.id != node2.id:
                    open_edges.append(Edge(node1, node2))
        

        # BEGIN BORUVKA
        # create component register
        components = {}
        for i in range(len(self.rooms)):
            components[i] = None
        
        solved = False
        while not solved:
            # iterate through edges
            for edge in open_edges:
                c1 = edge.nodes[0].id
                c2 = edge.nodes[1].id
                # print(c1, c2)

                # handle empties
                if not components[c1]:
                    components[c1] = edge
                if not components[c2]:
                    components[c2] = edge
                
                # handle better options
                if edge.weight < components[c1].weight:
                    components[c1] = edge
                if edge.weight < components[c2].weight:
                    components[c2] = edge
            # for comp in range(len(components)):
            #     sss = "{}".format(comp) + " : " + str(components[comp])
            #     print(sss)
            
            # merge connected components
            new_components = []
            for i in components:
                try:
                    c1 = components[i].nodes[0].id
                    c2 = components[i].nodes[1].id
                except AttributeError as error:
                    print(components)
                    print(open_edges)
                    return
                
                if not len(new_components):
                    new_components.append([c1, c2])
                else:
                    indicies = []
                    for j in range(len(new_components)):
                        if c1 in new_components[j] or c2 in new_components[j]:
                            indicies.append(j)
                    if len(indicies) == 0:
                        new_components.append([c1, c2])
                    else:
                        if c1 not in new_components[indicies[0]]:
                            new_components[indicies[0]].append(c1)
                        if c2 not in new_components[indicies[0]]:
                            new_components[indicies[0]].append(c2)
                        if len(indicies) != 1:
                            for k in indicies:
                                for l in new_components[k]:
                                    if l not in new_components[0]:
                                        new_components[0].append(l)
                            new_components[k] = []
            
            # finalize new components list
            new_components = [comp for comp in new_components if len(comp) != 0]

            # add closed edges and remove from open list
            for e in components:
                # print(components[e])
                closed_edges.append(components[e])
            for edge_idx in range(len(open_edges)):
                for comp_idx in range(len(components)):
                    if open_edges[edge_idx].is_equal(components[comp_idx]):
                        open_edges[edge_idx] == None
            open_edges = [e for e in open_edges if e != None]

            # update components dict
            updated_components_dict = {}
            for i in range(len(new_components)):
                updated_components_dict[i] = None
            components = updated_components_dict

            # update node refs for remaining open edges
            for edge_idx in range(len(open_edges)):
                for comp_idx in range(len(new_components)):
                    for itera in range(2):
                        if open_edges[edge_idx].nodes[itera].id in new_components[comp_idx]:
                            open_edges[edge_idx].nodes[itera].update_id(comp_idx)
            
            # remove any edges that connect to the same component
            for edge_idx in range(len(open_edges)):
                if open_edges[edge_idx].nodes[0].id == open_edges[edge_idx].nodes[1].id:
                    open_edges[edge_idx] = None
            open_edges = [e for e in open_edges if e != None]
            
            # check if we have a solution
            if len(new_components) == 1:
                solved = True

        self.final_edges = closed_edges             
            

    def place_paths(self):
        for edge in self.final_edges:
            n1 = edge.nodes[0]
            n2 = edge.nodes[1]
            cur_x = n1.x
            cur_y = n1.y
            while cur_x != n2.x:
                if cur_x < n2.x:
                    cur_x += 1
                elif cur_x > n2.x:
                    cur_x -= 1
                try:
                    self.ascii[cur_y][cur_x] = self.cells.floor
                except:
                    print("ERROR:")
                    print("n1: ({},{})".format(n1.x, n1.y))
                    print("n2: ({},{})".format(n2.x, n2.y))
                    print("cur: ({},{})".format(cur_x, cur_y))
            
            while cur_y != n2.y:
                if cur_y < n2.y:
                    cur_y += 1
                elif cur_y > n2.y:
                    cur_y -= 1
                try:
                    self.ascii[cur_y][cur_x] = self.cells.floor
                except:
                    print("ERROR:")
                    print("n1: ({},{})".format(n1.x, n1.y))
                    print("n2: ({},{})".format(n2.x, n2.y))
                    print("cur: ({},{})".format(cur_x, cur_y))

    def generate(self):
        # try:
        self.place_rooms()
        self.calc_boruvka()
        self.place_paths()
        # except Exception as e:
        #     print(e)
        #     self.generate()

def main():
    dungeon = DungeonObj(6, 5, 32)
    cur = dungeon.generate()
    print(dungeon)

if __name__ == "__main__":
    # random.seed(3)
    main()