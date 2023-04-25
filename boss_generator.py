import dungeon_generator
import map_image
import creatures_generator

class BossDungeon:
    def __init__(self, ascii) -> None:
        self.ascii = ascii

def generate_boss_room_data(size, lvl):
    # we need an odd sized room
    if size % 2 == 0:
        size += 1
    
    # generate a new map that's just a square
    boss_dungeon = [[dungeon_generator.Cells().floor for x in range(size)] for y in range(size)]
    # with a buffer of 1 square around the edge
    for x in range(size):
        for y in range(size):
            if x == 0 or x == size-1 or y == 0 or y == size-1:
                boss_dungeon[x][y] = dungeon_generator.Cells().empty

    # place a player token in the bottom row center
    boss_dungeon[size-2][int(size/2)] = dungeon_generator.Cells().player

    return boss_dungeon

def generate_boss_room_image(data):
    # generate the gridmap image, place large "boss token" in the center
    
    pass

def kill_update():
    # when you kill the boss, drop a door
    pass

def boss_process(size, lvl):
    boss_dungeon = generate_boss_room_data(16, 5)
    map_image.generate_img(boss_dungeon, "output_imgs/base_dungeon.png")
    # place a "boss" object in the center square
    boss = creatures_generator.Creature(lvl, demon=True)
    boss_dungeon[int(size/2)][int(size/2)] = boss
    map_image.place_token("output_imgs/base_dungeon.png",
                          "dungeon_imgs/demon1.jpg",
                          (int(size/2), int(size/2)),
                          "output_imgs/working_dungeon.png",
                          cell_size=3)
    bd = BossDungeon(boss_dungeon)
    return bd


if __name__ == "__main__":
    boss_process(16, 5)