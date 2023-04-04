import bot
import character_manager
import dungeon_generator

if __name__ == '__main__':
    player_obj = character_manager.CharacterManager(5, 5, 5, 100, 0, 1, None, None)
    dungeon_obj = dungeon_generator.DungeonObj(10, 8, 32)
    dungeon_obj.place_creatures(5, player_obj.lvl)
    print(str(dungeon_obj))
    bot.run_discord_bot(player_obj, dungeon_obj)