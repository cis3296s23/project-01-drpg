import random
import math
import creatures_generator

class Node:
    def __init__(self, x, y, id=None) -> None:
        self.x = x
        self.y = y
        if id:
            self.id = id

    def is_equal(self, node2) -> bool:
        if (self.x == node2.x) and (self.y == node2.y):
            return True
        return False
    
    def assign_id(self, new_id):
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
    
class Component:
    def __init__(self, id) -> None:
        self.id = id
        self.nodes = []
        self.cheapest_edge = None

    def set_id(self, id):
        self.id = id
    
    def add_node(self, node: Node):
        node.assign_id(self.id)
        self.nodes.append(node)

    def update_ids(self):
        for node in self.nodes:
            node.assign_id(self.id)

    def set_cheapest_edge(self, edge):
        self.cheapest_edge = edge

    def get_cheapest_edge(self):
        return self.cheapest_edge

class Cells:
    def __init__(self) -> None:
        self.empty = '░'
        self.floor = '█'
        self.chest = '▣'
        self.door = '◫'
        self.player = 'P'

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
        self.dungeon_size = dungeon_size - (dungeon_size % 2)
        self.buffer = 1 # NOTE: buffer between rooms
        self.cells = Cells()
        self.rooms = []
        self.final_edges = []
        self.player_start = None
        
        # fill new dungeon with blanks
        self.reset_map()

        self.place_rooms()
        # return str(self)
        self.calc_boruvka()
        if self.final_edges != []:
            self.place_paths()
            self.get_start_pos()
            self.ascii[self.player_start[0]][self.player_start[1]] = self.cells.player


    def __str__(self):
        string = ""
        for i in range(int(self.dungeon_size/2)):
            for j in range(self.dungeon_size):
                string += str(self.ascii[i][j])
            string += "\n"
        return string
    
    def reset_map(self):
        self.ascii = [
            [self.cells.empty for i in range(int(self.dungeon_size))] for j in range(int(self.dungeon_size/2))
        ]

    def get_start_pos(self):
        for i in range(len(self.ascii)):
            for j in range(len(self.ascii)):
                if self.ascii[i][j] == self.cells.floor:
                    self.player_start = (i, j)

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
                corner_y = random.randint(0, int(self.dungeon_size/2)-2)
                
                # check that this is a valid placement
                valid = True
                if (corner_y+size_y+self.buffer >= int(self.dungeon_size/2)) or (corner_x+size_x+self.buffer >= self.dungeon_size):
                    valid = False
                if valid:
                    for j in range(corner_y-self.buffer, corner_y+size_y+self.buffer):
                        for k in range(corner_x-self.buffer, corner_x+size_x+self.buffer):
                            if self.ascii[j][k] != self.cells.empty:
                                valid = False

            # place room, add to list
            self.rooms.append(Room(corner_x, corner_y, size_x, size_y, i))

            for j in range(corner_y, corner_y+size_y):
                    for k in range(corner_x, corner_x+size_x):
                        self.ascii[j][k] = self.cells.floor

    def _boruvka_update_node_ids(self, edges, nodes):
        id_map = []
        
        for edge in edges:
            id1 = edge.nodes[0].id
            id2 = edge.nodes[1].id

            appearances = []
            for index0 in range(len(id_map)):
                if id1 in id_map[index0] or id2 in id_map[index0]:
                    appearances.append(index0)
            
            if len(appearances) == 0:
                id_map.append([id1, id2])
            
            else:
                id_map[appearances[0]].append(id1)
                id_map[appearances[0]].append(id2)
                if len(appearances) > 1:
                    for index0 in appearances:
                        if index0 != appearances[0]:
                            for id0 in id_map[index0]:
                                id_map[appearances[0]].append(id0)
                            id_map[index0] = []
                id_map[appearances[0]] = [*set(id_map[appearances[0]])]
        
        for node in nodes:
            for idx in range(len(id_map)):
                if node.id in id_map[idx]:
                    node.id = idx*10
        for node in nodes:
            if node.id /10 > 1:
                node.id /=10
        return nodes


    def _boruvka_generate_nodes(self):
        nodes_list = []
        # create nodes
        check_idx = 0

        def pick_node(all_nodes, check_index, new_node):
            add_node = True
            for j in all_nodes[check_index:]:
                if new_node.is_equal(j):
                    add_node = False
            if add_node:
                all_nodes.append(new_node)
            return all_nodes
        
        for room in self.rooms:
            for i in range(room.corner_y, room.corner_y+room.size_y):                
                # left side
                new_node = Node(room.corner_x, i)
                new_node.assign_id(room.id)
                nodes_list = pick_node(nodes_list, check_idx, new_node)
                
                # right side
                new_node = Node(room.corner_x+room.size_x-1, i)
                new_node.assign_id(room.id)
                nodes_list = pick_node(nodes_list, check_idx, new_node)
            
            for i in range(room.corner_x, room.corner_x+room.size_x):
                
                # top row
                new_node = Node(i, room.corner_y)
                new_node.assign_id(room.id)
                nodes_list = pick_node(nodes_list, check_idx, new_node)
                
                # bottom row
                new_node = Node(i, room.corner_y+room.size_y-1)
                new_node.assign_id(room.id)
                nodes_list = pick_node(nodes_list, check_idx, new_node)
        
        return nodes_list

    def _boruvka_is_preferred_over(self, e1: Edge, e2: Edge):
        if e2 == None:
            return True
        if e1.weight < e2.weight:
            return True
        return False

    def calc_boruvka(self):
        verticies = self._boruvka_generate_nodes()
        E_prime = []
        components = {}

        # BEGIN BORUVKA
        completed = False
        
        while not completed:
            # Find the connected components of F and assign to each vertex its component id
            old_edges = []
            for c in components:
                edge = components[c].get_cheapest_edge()
                old_edges.append(edge)
  
            verticies = self._boruvka_update_node_ids(old_edges, verticies)
            
            components = {}
            for vertex in verticies:
                if vertex.id not in components.keys():
                    components[vertex.id] = Component(vertex.id)
                components[vertex.id].add_node(vertex)

            # Initialize the cheapest edge for each component to "None"
            for c in components:
                components[c].set_cheapest_edge(None)
            # for each edge uv in E, where u and v are in different components of F:
            for u in verticies:
                for v in verticies:
                    if u.id != v.id:
                        uv = Edge(u,v)
                        u_component = components[u.id]
                        v_component = components[v.id]
                        
                        # let wx be the cheapest edge for the component of u
                        wx = u_component.get_cheapest_edge()
                        # if is-preferred-over(uv, wx) then
                        if self._boruvka_is_preferred_over(uv, wx):
                            # Set uv as the cheapest edge for the component of u
                            u_component.set_cheapest_edge(uv)
                            components[u.id] = u_component
                        # let yz be the cheapest edge for the component of v
                        yz = v_component.get_cheapest_edge()
                        # if is-preferred-over(uv, yz) then
                        if self._boruvka_is_preferred_over(uv, yz):
                            # Set uv as the cheapest edge for the component of v
                            v_component.set_cheapest_edge(uv)
                            components[v.id] = v_component
            
            # if all components have cheapest edge set to "None" then
            all_none = True
            for c in components:
                if components[c].get_cheapest_edge() != None:
                    all_none = False
                    # for each component whose cheapest edge is not "None" do
                    # Add its cheapest edge to E'
                    E_prime.append(components[c].get_cheapest_edge())
            if all_none:
                # no more trees can be merged -- we are finished
                completed = True

        self.final_edges = E_prime           
            

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

    def check_valid_move(self, p):
        if (p[0] < 0 or 
            p[1] < 0 or 
            p[0] > len(self.ascii) or 
            p[1] > len(self.ascii[0])):
            return False
        elif (self.ascii[p[0]][p[1]] == self.cells.empty):
            return False
        return True
        
    def move_player(self, dir):
        # self.reset_map()
        print("move player called")
        # get player pos
        player_pos = None
        for i in range(len(self.ascii)):
            for j in range(len(self.ascii)):
                if self.ascii[i][j] == self.cells.player:
                    player_pos = (i,j)
        print(player_pos)
        # check that to_pos is valid
        up = (player_pos[0]-1, player_pos[1])
        down = (player_pos[0]+1, player_pos[1])
        left = (player_pos[0], player_pos[1]-1)
        right = (player_pos[0], player_pos[1]+1)
        mov = None
        
        if dir == "up" and self.check_valid_move(up):
            mov = up
        elif dir == "down" and self.check_valid_move(down):
            mov = down
        elif dir == "left" and self.check_valid_move(left):
            mov = left
        elif dir == "right" and self.check_valid_move(right):
            mov = right
        else:
            print("invalid move")
            # handle this somehow
            pass
        # swap tiles
        if mov:
            if mov != self.cells.floor:
                return self.ascii[mov[0]][mov[1]]
            else:
                self.ascii[player_pos[0]][player_pos[1]] = self.cells.floor
                self.ascii[mov[0]][mov[1]] = self.cells.player
        else:
            print("INVALID MOVE ERROR")

    def place_creatures(self, n, player_level):
        # places n creatures on the map
        for i in range(n):
            new_creature = creatures_generator.Creature(player_level)
            valid = False
            while not valid:
                x = random.randint(0, len(self.ascii)-1)
                y = random.randint(0, len(self.ascii[0])-1)
                if self.ascii[x][y] == self.cells.floor:
                    self.ascii[x][y] = new_creature
                    valid = True


    def get_current_map(self):
        return str(self)

if __name__ == "__main__":
    # random.seed(3)
    # print(generator_output())
    pass