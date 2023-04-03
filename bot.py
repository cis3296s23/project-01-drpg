import discord
import responses

def initialize_bot(player_obj, dungeon_obj):
    global_dungeon = dungeon_obj
    global_player = player_obj

async def standard_dungeon(message, client):
    # This is the standard dungeon loop
    sent_message = await message.channel.send(str(global_dungeon))
    for emoji in ['\U00002B06', '\U00002B07', '\U00002B05', '\U000027A1']:
            await sent_message.add_reaction(emoji)
    new_map = None
    while True:
        while not new_map:
            new_map = await check_reaction(client, sent_message)
        sent_message = await message.channel.send(new_map)
        for emoji in ['\U00002B06', '\U00002B07', '\U00002B05', '\U000027A1']:
            await sent_message.add_reaction(emoji)
        new_map = None

async def check_reaction(client, sent_message):
    # please note that this only handles the first reaction
    try:
         # Wait for a reaction to be added to the message
        def check(reaction, user):
            return (user != client.user and
                    reaction.message.id == sent_message.id)
        
        reaction, user = await client.wait_for('reaction_add', check=check)
        return responses.handle_movement(reaction, global_dungeon)
        # emoji = reaction
        # if emoji == '\U00002B06':
        #     global_dungeon.move_player("up")
        # elif emoji == '\U00002B07':
        #     global_dungeon.move_player("down")
        # elif emoji == '\U00002B05':
        #     global_dungeon.move_player("left")
        # elif emoji == '\U000027A1':
        #     global_dungeon.move_player("right")
        # else:
        #     pass
        # print(global_dungeon.get_current_map())
        
        # return global_dungeon.get_current_map()
    except Exception as e:
        print(e)

async def print_stats(client):
    pass
    # print the stats here, get them from the global object

def fight_enemy(player, creature):
    # for now, we will just keep rolling stats until someone dies
    pass


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
            await print_stats(client)

    client.run(TOKEN)