import bot
import character_manager
import dungeon_generator
import map_image
import creatures_generator
from PIL import Image

if __name__ == '__main__':
    player_obj = character_manager.CharacterManager(5, 5, 5, 100, 100, 0, 1, None, None)
    dungeon_obj = dungeon_generator.DungeonObj(6, 5, 16)
    map_image.generate_img(dungeon_obj.ascii, "output_imgs/base_dungeon.png")
    image = Image.open("output_imgs/base_dungeon.png")
    image.save("output_imgs/working_dungeon.png")
    
    dungeon_obj.place_creatures(5, player_obj.lvl)
    for i in range(len(dungeon_obj.ascii)):
        for j in range(len(dungeon_obj.ascii[i])):
            # check if there is a creature at this position by checking the class of the object
            if isinstance(dungeon_obj.ascii[i][j], creatures_generator.Creature):
                if dungeon_obj.ascii[i][j].name == "goblin":
                    token_img = "dungeon_imgs/Goblin.jpg"
                elif dungeon_obj.ascii[i][j].name == "troll":
                    token_img = "dungeon_imgs/Troll.jpg"
                elif dungeon_obj.ascii[i][j].name == "dragon":
                    token_img = "dungeon_imgs/Dragon.jpg"
                elif dungeon_obj.ascii[i][j].name == "skeleton":
                    token_img = "dungeon_imgs/Skeleton.jpg"
                    
                map_image.place_token(
                    "output_imgs/working_dungeon.png", 
                    token_img,
                    (i, j),
                    "output_imgs/working_dungeon.png")
            elif dungeon_obj.ascii[i][j] == dungeon_generator.Cells().player:
                map_image.place_token(
                    "output_imgs/working_dungeon.png", 
                    "dungeon_imgs/Player.png",
                    (i, j),
                    "output_imgs/working_dungeon.png")      
    print(str(dungeon_obj))
    bot.run_discord_bot(player_obj, dungeon_obj)