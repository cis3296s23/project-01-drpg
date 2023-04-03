import random
import dungeon_generator

dungeon_obj = dungeon_generator.generator_output()

def get_response(message: str) -> str:
    """
    This function will return a tuple.
    The first element, if any, will be the actual text of the message
    The second element will be a list containing any emoji reacts
    """
    p_message = message.lower()

    # if p_message == 'hello':
    #     return 'Hello World'

    # if message == '!roll':
    #     return str(random.randint(1, 6))

    # if p_message == '!help':
    #     return '`This is a help message that you can modify.`'

    if p_message == '!map':
        response_str = dungeon_obj.get_current_map()
        # up, down, left, right
        emojis = ['\U00002B06', '\U00002B07', '\U00002B05', '\U000027A1']
        return (response_str, emojis)
    
    if p_message == "_get_map_internal":
        response_str = dungeon_generator.get_current_map()
        # up, down, left, right
        emojis = []
        return (response_str, emojis)



    # return 'I didn\'t understand what you wrote. Try typing "!help".'

def handle_movement(emoji) -> None:
    if emoji == '\U00002B06':
        dungeon_obj.move_player("up")
    elif emoji == '\U00002B07':
        dungeon_obj.move_player("down")
    elif emoji == '\U00002B05':
        dungeon_obj.move_player("left")
    elif emoji == '\U000027A1':
        dungeon_obj.move_player("right")
    else:
        pass
    return dungeon_obj.get_current_map()