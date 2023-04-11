import discord
import random

async def standard_dungeon(message, client):
    # This is the standard dungeon loop
    while True:
        new_map = str(global_dungeon)
        sent_message = await message.channel.send(new_map)        
        for emoji in ['\U00002B06', '\U00002B07', '\U00002B05', '\U000027A1']:
            await sent_message.add_reaction(emoji)
        await check_reaction(client, sent_message, message)
        new_map = None

async def check_reaction(client, sent_message, message):
    # please note that this only handles the first reaction
    try:
         # Wait for a reaction to be added to the message
        def check(reaction, user):
            return (user != client.user and
                    reaction.message.id == sent_message.id)
        
        reaction, user = await client.wait_for('reaction_add', check=check)
        # return responses.handle_movement(reaction, global_dungeon)
        emoji_r = reaction.emoji
        def movement(emoji):
            if emoji == '\U00002B06' or emoji == '⬆':
                enemy = global_dungeon.move_player("up")
                print("up")
            elif emoji == '\U00002B07' or emoji == '⬇':
                enemy = global_dungeon.move_player("down")
                print("down")
            elif emoji == '\U00002B05' or emoji == '⬅':
                enemy = global_dungeon.move_player("left")
                print("left")
            elif emoji == '\U000027A1' or emoji == '➡':
                enemy = global_dungeon.move_player("right")
                print("right")
            else:
                print("failed to recognize")
                print(emoji.encode('unicode_escape').decode())
            return enemy
        enemy_obj = movement(emoji_r)
        # print(global_dungeon.get_current_map())
        if enemy_obj:
            await message.channel.send(f'Player is now fighting lvl {enemy_obj.character_manager.lvl} {enemy_obj.name}')
            result = fight_enemy(enemy_obj, message, client)
            if result:
                await message.channel.send(f'Player has slain {enemy_obj.name}')
                global_dungeon.remove_creature(enemy_obj)
                movement(emoji_r)
            else:
                await message.channel.send(f'Player has been slain by {enemy_obj.name}')
                global_dungeon.reset_map()


        # return global_dungeon.get_current_map()
    except Exception as e:
        print(e)

async def print_stats(username, message):
    await message.channel.send(f"```{username}'s Stats\nLevel: {global_player.lvl}\nHealth: {global_player.hp}\nStrength: {global_player.str}\nDexterity: {global_player.dex}\nEndurance: {global_player.end}\nCurrent XP: {global_player.xp}```")

async def fight_enemy(creature, message, client):
    await message.channel.send(f'You have encountered an enemy!')
    while global_player.hp > 0 and creature.character_manager.hp > 0:
        await message.channel.send(f'Do you want to !attack, !counter?, or !fight')
        def check(m):
            return m.author == message.author and m.channel == message.channel and m.content in ['!attack', '!counter', '!fight']
        user_move = await client.wait_for('message', check=check)

        if user_move.content == '!attack':
            p_attack = global_player.calc_damage_dealt()
            creature.character_manager.hp -= p_attack

            await message.channel.send(f'Player Attack: {p_attack}\n'
                                       f'Enemy Health: {creature.character_manager.hp}')

            if creature.character_manager.hp <= 0:  # return true when the player beats the enemy
                return True

            c_attack = random.randint(1, creature.character_manager.str)
            p_reduction = global_player.calc_damage_taken(c_attack)
            global_player.hp -= p_reduction

            await message.channel.send(f'Enemy Attack: {c_attack}\n'
                                       f'Player Health: {global_player.hp}')

            if global_player.hp <= 0:  # return false when the creature beats the player
                return False

        elif user_move.content == '!counter':
            chance = random.randint(1, 2)
            if chance == 1:  # 50/50 chance to proc counter
                p_attack = (global_player.calc_damage_dealt() * 2)  # high risk high reward
                creature.character_manager.hp -= p_attack

                await message.channel.send(f'Successful Counter!'
                                           f'Player Attack: {p_attack}'
                                           f'Enemy Health: {creature.character_manager.hp}')

                if creature.character_manager.hp <= 0:  # return true when the player beats the enemy
                    return True

            else:
                c_attack = (random.randint(1, creature.character_manager.str) * 4)  # missed, leaves you wide open for attacks
                p_reduction = global_player.calc_damage_taken(c_attack)
                global_player.hp -= p_reduction

                await message.channel.send(f'Unsuccessful Counter!'
                                           f'Enemy Attack: {p_reduction}'
                                           f'Player Health: {global_player.hp}')

                if global_player.hp <= 0:  # return false when the creature beats the player
                    return False

        elif user_move.content == '!fight':
            while global_player.hp > 0 and creature.character_manager.hp > 0:
                p_attack = global_player.calc_damage_dealt()
                creature.character_manager.hp -= p_attack

                if creature.character_manager.hp <= 0:
                    return True

                c_attack = random.randint(1, creature.character_manager.str)
                p_reduction = global_player.calc_damage_taken(c_attack)
                global_player.hp -= p_reduction

                if global_player.hp <= 0:
                    return False

        else:
            await message.channel.send('Invalid move!')



def run_discord_bot(player_obj, dungeon_obj):
    global global_dungeon
    global global_player
    global_dungeon = dungeon_obj
    global_player = player_obj
    with open("TOKEN.txt", 'r') as tkn:
        TOKEN = tkn.read()
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):

        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        # handle response
        if user_message == '!dungeon':
            await standard_dungeon(message, client)
        elif user_message == '!stat':
            await print_stats(username, message)

    client.run(TOKEN)