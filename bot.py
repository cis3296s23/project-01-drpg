import discord
import random
from discord.ext import commands
from PIL import Image
import creatures_generator
import dungeon_generator
import map_image

def regenerate_dungeon():
    dungeon_obj = global_dungeon
    image = Image.open("output_imgs/base_dungeon.png")
    image.save("output_imgs/working_dungeon.png")
    
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

async def handle_move(user_message, message, client):
    # split the message by spaces
    split_message = user_message.split()
    move = split_message[1]
    # convert this into ij coordinates
    y = ord(move[0]) - 97
    x = int(move[1:]) -1
    # check if the move is valid
    if x < 0 or x > 16 or y < 0 or y > 16:
        await message.channel.send("Invalid move, please try again.")
        return
    
    if global_dungeon.ascii[y][x] == dungeon_generator.Cells().empty:
        await message.channel.send("Invalid move, please try again.")
        return
    
    if global_dungeon.ascii[y][x] == dungeon_generator.Cells().floor:
        for i in range(len(global_dungeon.ascii)):
            for j in range(len(global_dungeon.ascii[i])):
                if global_dungeon.ascii[i][j] == dungeon_generator.Cells().player:
                    global_dungeon.ascii[i][j] = dungeon_generator.Cells().floor
        global_dungeon.ascii[y][x] = dungeon_generator.Cells().player
        regenerate_dungeon()
        await message.channel.send(file=discord.File("output_imgs/working_dungeon.png"))
        return
    if isinstance(global_dungeon.ascii[y][x], creatures_generator.Creature):
        enemy_obj = global_dungeon.ascii[y][x]
        result = await fight_enemy(enemy_obj, message, client)
        if result:
            await message.channel.send(f'Player has slain {enemy_obj.name}')
            global_dungeon.remove_creature(enemy_obj)
            for i in range(len(global_dungeon.ascii)):
                for j in range(len(global_dungeon.ascii[i])):
                    if global_dungeon.ascii[i][j] == dungeon_generator.Cells().player:
                        global_dungeon.ascii[i][j] = dungeon_generator.Cells().floor
            global_dungeon.ascii[y][x] = dungeon_generator.Cells().player
            regenerate_dungeon()
            await message.channel.send(file=discord.File("output_imgs/working_dungeon.png"))
        else:
            await message.channel.send(f'Player has been slain by {enemy_obj.name}')
            global_dungeon.reset_map()

    


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
            result = await fight_enemy(enemy_obj, message, client)
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
    await message.channel.send(
        f"```{username}'s Stats\nLevel: {global_player.lvl}\nHealth: {global_player.hp}\nStrength: {global_player.str}\nDexterity: {global_player.dex}\nEndurance: {global_player.end}\nCurrent XP: {global_player.xp}```")


async def fight_enemy(creature, message, client):
    await message.channel.send(f'You have encountered an enemy!')
    while global_player.hp > 0 and creature.character_manager.hp > 0:
        await message.channel.send(f'Do you want to [!fight / !counter / !auto]')

        def check(m):
            return m.author == message.author and m.channel == message.channel and m.content in ['!fight', '!counter',
                                                                                                 '!auto']

        user_move = await client.wait_for('message', check=check)

        if user_move.content == '!fight':
            p_attack = global_player.calc_damage_dealt()
            creature.character_manager.modifyHP(p_attack)

            embed = discord.Embed(title="Player Turn!", color=0x00990000)
            embed.add_field(name="Player Attack:", value=f"{p_attack}", inline=True)
            embed.add_field(name="Enemy Health:", value=f"{creature.character_manager.hp} / {creature.character_manager.maxHP}", inline=True)

            await message.channel.send(embed=embed)

            if creature.character_manager.hp <= 0:  # return true when the player beats the enemy
                return True

            c_attack = random.randint(1, creature.character_manager.str)
            p_reduction = global_player.calc_damage_taken(c_attack)
            global_player.modifyHP(p_reduction)

            embed = discord.Embed(title="Enemy Turn!", color=0x00990099)
            embed.add_field(name="Enemy Attack:", value=f"{round(p_reduction,2)}", inline=True)
            embed.add_field(name="Player Health:", value=f"{round(global_player.hp,2)} / {global_player.maxHP}", inline=True)

            await message.channel.send(embed=embed)

            if global_player.hp <= 0:  # return false when the creature beats the player
                return False

        elif user_move.content == '!counter':
            chance = random.randint(1, 2)
            if chance == 1:  # 50/50 chance to proc counter
                p_attack = (global_player.calc_damage_dealt() * 2)  # high risk high reward
                creature.character_manager.modifyHP(p_attack)

                embed = discord.Embed(title="Successful counter!", color=0x00990000)
                embed.add_field(name="Player Attack:", value=f"{p_attack}", inline=True)
                embed.add_field(name="Enemy Health:", value=f"{creature.character_manager.hp} / {creature.character_manager.maxHP}", inline=True)

                await message.channel.send(embed=embed)

                if creature.character_manager.hp <= 0:  # return true when the player beats the enemy
                    return True

            else:
                c_attack = (random.randint(1,
                                           creature.character_manager.str) * 4)  # missed, leaves you wide open for attacks
                p_reduction = global_player.calc_damage_taken(c_attack)
                global_player.modifyHP(p_reduction)

                embed = discord.Embed(title="Unsuccessful Counter!", color=0x00990099)
                embed.add_field(name="Enemy Attack:", value=f"{round(p_reduction,2)}", inline=True)
                embed.add_field(name="Player Health:", value=f"{round(global_player.hp,2)} / {global_player.maxHP}", inline=True)

                await message.channel.send(embed=embed)

                if global_player.hp <= 0:  # return false when the creature beats the player
                    return False

        elif user_move.content == '!auto':
            embed = discord.Embed(title="In Battle!", color=0x00990000)
            embed.add_field(name="Player Attack:", value="0", inline=True)
            embed.add_field(name="Enemy Health:", value="0", inline=True)
            embed.add_field(name="Enemy Attack:", value="0", inline=True)
            embed.add_field(name="Player Health:", value="0", inline=True)

            msg = await message.channel.send(embed=embed)

            while global_player.hp > 0 and creature.character_manager.hp > 0:
                p_attack = global_player.calc_damage_dealt()
                creature.character_manager.modifyHP(p_attack)

                embed.set_field_at(index=0, name="Player Attack:", value=f"{p_attack}")
                embed.set_field_at(index=1, name="Enemy Health:", value=f"{creature.character_manager.hp} / {creature.character_manager.maxHP}")

                await msg.edit(embed=embed)

                if creature.character_manager.hp <= 0:
                    embed.set_field_at(index=3, name="Player Health:",
                                       value=f"{round(global_player.hp, 2)} / {global_player.maxHP}")
                    embed.set_field_at(index=2, name="Enemy Attack:", value="0")
                    await msg.edit(embed=embed)
                    return True

                c_attack = random.randint(1, creature.character_manager.str)
                p_reduction = global_player.calc_damage_taken(c_attack)
                global_player.modifyHP(p_reduction)

                embed.set_field_at(index=2, name="Enemy Attack:", value=f"{round(p_reduction, 2)}")
                embed.set_field_at(index=3, name="Player Health:",
                                   value=f"{round(global_player.hp, 2)} / {global_player.maxHP}")

                await msg.edit(embed=embed)

                if global_player.hp <= 0:
                    embed.set_field_at(index=1, name="Enemy Health:",
                                       value=f"{creature.character_manager.hp} / {creature.character_manager.maxHP}")
                    embed.set_field_at(index=0, name="Player Attack:", value="0")
                    await msg.edit(embed=embed)
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
            await message.channel.send(file=discord.File("output_imgs/working_dungeon.png"))
        elif user_message == '!stat':
            await print_stats(username, message)
        # check if message begins with "!move"
        elif user_message.startswith('!move'):
            await handle_move(user_message, message, client)


    client.run(TOKEN)