import discord
import random
from discord.ext import commands
from PIL import Image
import creatures_generator
import dungeon_generator
import map_image
import requests
import boss_generator
from gear_generation import Weapon, Armor

maxNum: int  = 50
def enter_boss_dungeon():
    global global_player
    global global_dungeon
    global_dungeon = boss_generator.boss_process(16, global_player.lvl)
    # image = Image.open("output_imgs/base_boss_room.png")
    # image.save("output_imgs/working_dungeon.png")
    
    for i in range(len(global_dungeon.ascii)):
        for j in range(len(global_dungeon.ascii[i])):
            if global_dungeon.ascii[i][j] == dungeon_generator.Cells().player:
                map_image.place_token(
                    "output_imgs/working_dungeon.png", 
                    "dungeon_imgs/Player.png",
                    (i, j),
                    "output_imgs/working_dungeon.png")


def make_new_floor():
    global global_player
    global global_dungeon
    global_dungeon = dungeon_generator.DungeonObj(6, 5, 16)
    map_image.generate_img(global_dungeon.ascii, "output_imgs/base_dungeon.png")
    
    global_dungeon.place_creatures(5, global_player.lvl)

    regenerate_dungeon()
    

def regenerate_dungeon():
    global global_player
    global global_dungeon
    image = Image.open("output_imgs/base_dungeon.png")
    image.save("output_imgs/working_dungeon.png")
    
    for i in range(len(global_dungeon.ascii)):
        for j in range(len(global_dungeon.ascii[i])):
            # check if there is a creature at this position by checking the class of the object
            if isinstance(global_dungeon.ascii[i][j], creatures_generator.Creature):
                if global_dungeon.ascii[i][j].name == "goblin":
                    token_img = "dungeon_imgs/Goblin.jpg"
                elif global_dungeon.ascii[i][j].name == "troll":
                    token_img = "dungeon_imgs/Troll.jpg"
                elif global_dungeon.ascii[i][j].name == "dragon":
                    token_img = "dungeon_imgs/Dragon.jpg"
                elif global_dungeon.ascii[i][j].name == "skeleton":
                    token_img = "dungeon_imgs/Skeleton.jpg"
                elif global_dungeon.ascii[i][j].name == "demon":
                    token_img = "dungeon_imgs/demon1.jpg"
                
                if token_img != "dungeon_imgs/demon1.jpg":
                    map_image.place_token(
                        "output_imgs/working_dungeon.png", 
                        token_img,
                        (i, j),
                        "output_imgs/working_dungeon.png")
                else:
                    map_image.place_token(
                        "output_imgs/working_dungeon.png", 
                        token_img,
                        (i, j),
                        "output_imgs/working_dungeon.png",
                        cell_size=3)
                    
            elif global_dungeon.ascii[i][j] == dungeon_generator.Cells().player:
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
    # check displacement from current position
    for i in range(len(global_dungeon.ascii)):
        for j in range(len(global_dungeon.ascii[i])):
            if global_dungeon.ascii[i][j] == dungeon_generator.Cells().player:
                x_displacement = abs(j - x)
                y_displacement = abs(i - y)
                # get hypotenuse
                hypotenuse = (x_displacement ** 2 + y_displacement ** 2) ** 0.5
                if hypotenuse > global_player.dex:
                    await message.channel.send(f'You are too slow to move there, you only have {global_player.dex} dexterity.')
                    return
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
            if enemy_obj.name != "demon":
                await message.channel.send(f'Player has slain {enemy_obj.name}')
                global_dungeon.remove_creature(enemy_obj)
                for i in range(len(global_dungeon.ascii)):
                    for j in range(len(global_dungeon.ascii[i])):
                        if global_dungeon.ascii[i][j] == dungeon_generator.Cells().player:
                            global_dungeon.ascii[i][j] = dungeon_generator.Cells().floor
                global_dungeon.ascii[y][x] = dungeon_generator.Cells().player
                regenerate_dungeon()
            else:
                # place door in ascii
                global_dungeon.ascii[y][x] = dungeon_generator.Cells().door
                regenerate_dungeon()
                global_player.hp = 100
            global_player.xp += enemy_obj.character_manager.lvl

            await message.channel.send(file=discord.File("output_imgs/working_dungeon.png"))
        else:
            await message.channel.send(f'Player has been slain by {enemy_obj.name}')
            await death_screen(message)
            # global_dungeon.reset_map()
    if global_dungeon.ascii[y][x] == dungeon_generator.Cells().door:
        await message.channel.send("You have reached the next level!")
        await level_up(message, client)
        if global_player.lvl > 0 and global_player.lvl%3 == 0:
            print(global_player.lvl)
            enter_boss_dungeon()
        else:
            make_new_floor()
        await message.channel.send(file=discord.File("output_imgs/working_dungeon.png"))
        return

async def level_up(message, client):
    global_player.lvl += 1
    # ask the player what they want to level up
    msg = await message.channel.send("What would you like to level up?")
    # react with three emojis
    for emoji in [ '💪', '🏃', '🔰']:
            await msg.add_reaction(emoji)
    def check(reaction, user):
        return (user != client.user and
                reaction.message.id == msg.id)

    reaction, user = await client.wait_for('reaction_add', check=check)
    # return responses.handle_movement(reaction, global_dungeon)
    emoji_r = reaction.emoji
    if emoji_r == '💪':
        global_player.str += 1
        global_player.str *= (1 + global_player.xp/10)
    elif emoji_r == '🏃':
        global_player.dex += 1
        global_player.dex *= (1 + global_player.xp/10)

    elif emoji_r == '🔰':
        global_player.end += 1
        global_player.end *= (1 + global_player.xp/10)
    global_player.xp = 0
    
    await message.channel.send(f'Player has leveled up to level {global_player.lvl}!')
    

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
                await death_screen(message)
                global_dungeon.reset_map()

        # return global_dungeon.get_current_map()
    except Exception as e:
        print(e)

async def death_screen(message):
    embed = discord.Embed(title="Flames extinguished", color=0x00000000)

    with open('death.gif', 'wb') as f:
        response = requests.get('https://media.giphy.com/media/TbONGqAdpTWQW3Hz5V/giphy.gif')
        f.write(response.content)

    with open("death.gif", 'rb') as gif:
        file = discord.File(gif)
        embed.set_image(url="attachment://death.gif")

    await message.channel.send(embed=embed, file=file)

async def print_stats(username, message):
    embed = discord.Embed(title="The Bearer of Fire", color=0x00990000)

    with open('knight.gif', 'wb') as f:
        response = requests.get('https://i.imgur.com/gVmZvEE.gif')
        f.write(response.content)

    with open("knight.gif", 'rb') as gif:
        file = discord.File(gif)
        embed.set_image(url="attachment://knight.gif")

    embed.add_field(name=f"{username}'s Stats", value="", inline=False)
    embed.add_field(name="Level:", value=f"{global_player.lvl}", inline=True)
    embed.add_field(name="Health:", value=f"{round(global_player.hp, 2)} / {global_player.maxHP}", inline=True)
    embed.add_field(name="Strength:", value=f"{round(global_player.str,2)}", inline=True)
    embed.add_field(name="Dexterity:", value=f"{round(global_player.dex,2)}", inline=True)
    embed.add_field(name="Endurance:", value=f"{round(global_player.end,2)}", inline=True)
    embed.add_field(name="Souls:", value=f"{round(global_player.souls, 2)}", inline=True)

    await message.channel.send(embed=embed, file=file)

async def print_enemy_stats(creature, message):
    token_img = "none"
    if creature.name == "goblin":
        token_img = "https://media.discordapp.net/attachments/1090076585824092161/1100204082595111003/Goblin.jpg"
    elif creature.name == "troll":
        token_img = "https://media.discordapp.net/attachments/1090076585824092161/1100204082985185451/Troll.jpg"
    elif creature.name == "dragon":
        token_img = "https://media.discordapp.net/attachments/1090076585824092161/1100204082343456828/Dragon.jpg?width=395&height=395"
    elif creature.name == "skeleton":
        token_img = "https://media.discordapp.net/attachments/1090076585824092161/1100204082783862924/Skeleton.jpg?width=395&height=395"
    elif creature.name == "demon":
        token_img = "https://cdn.discordapp.com/attachments/1090076585824092161/1100212512680587395/demon1.jpg"

    embed = discord.Embed(title="Adversary", color=0x00990099)

    embed.add_field(name=f"{creature.name}'s Stats", value="", inline=False)
    embed.add_field(name="Level:", value=f"{creature.character_manager.lvl}", inline=True)
    embed.add_field(name="Health:", value=f"{creature.character_manager.hp}", inline=True)
    embed.add_field(name="Strength:", value=f"{creature.character_manager.str}", inline=True)
    embed.add_field(name="Dexterity:", value=f"{creature.character_manager.dex}", inline=True)
    embed.add_field(name="Endurance:", value=f"{creature.character_manager.end}", inline=True)
    embed.set_image(url=token_img)

    await message.channel.send(embed=embed)

async def help_cmd(message):
    await message.channel.send(
        "```!dungeon - spawn dungeon map to play\n!move - to move within dungeon, call !move and the desired coordinates\nex. !move d3\nNotes - to fight, walk over to an opponent\n!stat - User current status\nFight commands - !fight, !counter, !auto\nFight is a single turn attack, counter is chance to dodge and deal great damage, Auto is to run the fight automatically```")


async def fight_enemy(creature, message, client):
    await message.channel.send(f'You have encountered an enemy!')
    await print_enemy_stats(creature, message)
    while global_player.hp > 0 and creature.character_manager.hp > 0:
        if global_player.souls >= 10 * global_player.lvl:
            await message.channel.send(
                f'The Embers of your soul are burning viciously!\n Choose your special move! ``!armory  !final attack  !life steal``')

            def check(msg):
                return msg.author == message.author and msg.channel == message.channel and msg.content in ['!armory',
                                                                                                           '!final attack',
                                                                                                           '!life steal']

            user_move = await client.wait_for('message', check=check)

            if user_move.content == '!life steal':
                p_attack = global_player.calc_damage_dealt()
                creature.character_manager.modifyHP(p_attack)
                global_player.increaseHP(p_attack)

                embed = discord.Embed(title="Life Steal", color=0x00990000)
                embed.add_field(name="", value="All souls you have collected, indiscriminate, become yours..")
                embed.add_field(name="Player Attack:", value=f"{round(p_attack, 2)}", inline=True)
                embed.add_field(name="Player Health:", value=f"{round(global_player.hp, 2)} / {global_player.maxHP}",
                                inline=True)
                embed.add_field(name="Enemy Health:",
                                value=f"{round(creature.character_manager.hp, 2)} / {creature.character_manager.maxHP}",
                                inline=True)
                embed.set_image(
                    url="https://static.wikia.nocookie.net/bleach/images/e/e2/ZankanoTachiMinami.png/revision/latest?cb=20160923173429&path-prefix=fr")

                global_player.souls -= 10 * global_player.lvl

                await message.channel.send(embed=embed)

                if creature.character_manager.hp <= 0:  # return true when the player beats the enemy
                    global_player.souls += creature.character_manager.lvl * 10
                    return True

            elif user_move.content == '!armory':
                weapon = Weapon()
                armor = Armor()
                global_player.weapon = weapon
                global_player.armor = armor

                embed = discord.Embed(title="Forged from Fire", color=0x00990000)
                embed.add_field(name="", value="All souls you have collected, indiscriminate, become your armory...",
                                inline=False)
                embed.add_field(name="Weapon:", value=f"{weapon.name}", inline=True)
                embed.add_field(name="Weapon Damage / Speed", value=f"{weapon.damage} / {weapon.speed}", inline=True)
                embed.add_field(name="Armor:", value=f"{armor.name}", inline=True)
                embed.add_field(name="Armor Protection:", value=f"{armor.protection}", inline=True)
                embed.set_image(url="https://i.pinimg.com/originals/37/16/9c/37169c9719cc83821177216cdb19a323.jpg")

                global_player.souls -= 10 * global_player.lvl

                await message.channel.send(embed=embed)

            elif user_move.content == '!final attack':
                p_attack = (global_player.calc_damage_dealt() * global_player.lvl)
                creature.character_manager.modifyHP(p_attack)

                embed = discord.Embed(title="Longsword of the Remnant Flame", color=0x00990000)
                embed.add_field(name="",
                                value="All souls you have collected, indiscriminate, become your sword... \n With a swift swing of your sword, your enemies are no more.")
                embed.add_field(name="Player Attack:", value=f"{round(p_attack, 2)}", inline=True)
                embed.add_field(name="Enemy Health:",
                                value=f"{round(creature.character_manager.hp, 2)} / {creature.character_manager.maxHP}",
                                inline=True)
                embed.set_image(
                    url="https://e1.pxfuel.com/desktop-wallpaper/505/750/desktop-wallpaper-genryusai-shigekuni-yamamoto.jpg")

                global_player.souls -= 10 * global_player.lvl

                await message.channel.send(embed=embed)

                if creature.character_manager.hp <= 0:  # return true when the player beats the enemy
                    global_player.souls += creature.character_manager.lvl * 10
                    return True

        await message.channel.send(f'Do you want to ``!fight  !counter  !auto``')

        def check(m):
            return m.author == message.author and m.channel == message.channel and m.content in ['!fight', '!counter',
                                                                                                 '!auto']

        user_move = await client.wait_for('message', check=check)

        if user_move.content == '!fight':
            p_attack = global_player.calc_damage_dealt()
            creature.character_manager.modifyHP(p_attack)

            embed = discord.Embed(title="Player Turn!", color=0x00990000)
            embed.add_field(name="Player Attack:", value=f"{round(p_attack,2)}", inline=True)
            embed.add_field(name="Enemy Health:", value=f"{round(creature.character_manager.hp,2)} / {creature.character_manager.maxHP}", inline=True)

            await message.channel.send(embed=embed)

            if creature.character_manager.hp <= 0:  # return true when the player beats the enemy
                global_player.souls += creature.character_manager.lvl * 10
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
                p_attack = (global_player.calc_damage_dealt() * global_player.lvl)  # high risk high reward
                creature.character_manager.modifyHP(p_attack)

                embed = discord.Embed(title="Successful counter!", color=0x00990000)
                embed.add_field(name="Player Attack:", value=f"{round(p_attack,2)}", inline=True)
                embed.add_field(name="Enemy Health:", value=f"{round(creature.character_manager.hp,2)} / {creature.character_manager.maxHP}", inline=True)

                await message.channel.send(embed=embed)

                if creature.character_manager.hp <= 0:  # return true when the player beats the enemy
                    global_player.souls += creature.character_manager.lvl * 10
                    return True

            else:
                c_attack = (random.randint(1,
                                           creature.character_manager.str) * 2)  # missed, leaves you wide open for attacks
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

            with open('battle.gif', 'wb') as f:
                response = requests.get('https://i.imgur.com/cTGkXEE.gif')
                f.write(response.content)

            with open("battle.gif", 'rb') as gif:
                file = discord.File(gif)
                embed.set_image(url="attachment://battle.gif")

            msg = await message.channel.send(embed=embed, file=file)

            while global_player.hp > 0 and creature.character_manager.hp > 0:
                p_attack = global_player.calc_damage_dealt()
                creature.character_manager.modifyHP(p_attack)

                embed.set_field_at(index=0, name="Player Attack:", value=f"{round(p_attack, 2)}")
                embed.set_field_at(index=1, name="Enemy Health:", value=f"{round(creature.character_manager.hp, 2)} / {creature.character_manager.maxHP}")

                await msg.edit(embed=embed)

                if creature.character_manager.hp <= 0:
                    embed.set_field_at(index=3, name="Player Health:",
                                       value=f"{round(global_player.hp, 2)} / {global_player.maxHP}")
                    embed.set_field_at(index=2, name="Enemy Attack:", value="0")
                    await msg.edit(embed=embed)
                    global_player.souls += creature.character_manager.lvl * 10
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
                                       value=f"{round(creature.character_manager.hp, 2)} / {creature.character_manager.maxHP}")
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
        channel = client.get_channel(1090076422699233331)
        embed = discord.Embed(title="DungeonRPG", color=0x00990000)
        embed.add_field(name="", value="O, Inheritor of the Frenzied Flame. For so long, they have tried to extinguish thy light. This accursed dungeon they so desperately cling to, believing it could tame your fire. Climb the floors and incinerate all who oppose you, for glory and victory will be yours when you set the world that casted you out aflame. You, alone, are the honored one.", inline=True)

        with open('agravain.gif', 'wb') as f:
            response = requests.get('https://media.tenor.com/AfntJE4H984AAAAd/agravain.gif')
            f.write(response.content)

        with open("agravain.gif", 'rb') as gif:
            file = discord.File(gif)
            embed.set_image(url="attachment://agravain.gif")
            embed.add_field(name="", value="To begin, type !dungeon or !help for instructions", inline=False)

            await channel.send(embed=embed, file=file)

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
        elif user_message == '!help':
            await help_cmd(message)
        # check if message begins with "!move"
        elif user_message.startswith('!move'):
            await handle_move(user_message, message, client)


    client.run(TOKEN)