import random
import dungeon_generator


def get_response(message: str) -> str:
    p_message = message.lower()

    # if p_message == 'hello':
    #     return 'Hello World'

    if message == '!roll':
        return str(random.randint(1, 6))

    # if p_message == '!help':
    #     return '`This is a help message that you can modify.`'

    if p_message == '!map':
        return dungeon_generator.generator_output()



    # return 'I didn\'t understand what you wrote. Try typing "!help".'