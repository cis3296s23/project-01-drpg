import discord
import responses

async def send_message(message, user_message, client, is_private):
    try:
        response = responses.get_response(user_message)
        if response[0] != None:
            sent_message = await message.author.send(response[0]) if is_private else await message.channel.send(response[0])
            if response[1] != None:
                for emoji in response[1]:
                    await sent_message.add_reaction(emoji)
                await check_reaction(client, sent_message)
    except Exception as e:
        print(e)

async def check_reaction(client, sent_message):
    # please not that this only handles the first reaction
    try:
         # Wait for a reaction to be added to the message
        def check(reaction, user):
            return (user != client.user and
                    reaction.message.id == sent_message.id)
        
        reaction, user = await client.wait_for('reaction_add', check=check)
        responses.handle_movement(reaction.emoji)
    except Exception as e:
        print(e)


def run_discord_bot():
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
        sent_message = None
        if user_message[0] == '?':
            user_message = user_message[1:]
            sent_message = await send_message(message, user_message, client, is_private=True)
        else:
            sent_message = await send_message(message, user_message, client, is_private=False)

    client.run(TOKEN)