import discord
import responses

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        if response[0] != None:
            sent_message = await message.author.send(response[0]) if is_private else await message.channel.send(response[0])
            if response[1] != None:
                for emoji in response[1]:
                    await sent_message.add_reaction(emoji)
    except Exception as e:
        print(e)

async def add_reaction(message, emoji):
    try:
        pass
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

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)