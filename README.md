# DungeonRPG
Dungeon RPG is a Discord bot that allows players to engage in combat and have fun on the Discord platform using the Discord API Framework utilizing Python as the programming language 

# How to run
 - Download the latest [release](https://github.com/cis3296s23/DungeonHuntingRPG/releases)
 - Open the code in an IDE/terminal and move files into the directory of the project
 - Setup Discord bot as shown in [Technical Information](#technical-information)
 - Right click the channel you want your Discord bot to be in and copy the Channel ID
```
create a file called TOKEN.txt in the directory and place the API token there.
```
- Install Discord API
  - Go to terminal, and enter below
```
pip install discord.py 
```
-  Run main.py, and the discord bot should run in the server
-  **CAUTION TO DEVELOPERS**: remember to erase the token from TOKEN = 'erase token here' before releasing any changes to public, not doing so will require you to create a new discord bot token

# Technical Information 

## Enable Developer Mode

1. Open the discord application.
2. On the bottom left corner of the application, click the cog wheel settings icon.
3. Go to the "Advanced" section and tick on "Developer Mode".

## Setup Discord Bot

1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications) and click New Application
2. Create a name then navigate to the Bot tab then click Add Bot
3. Press Reset Token and then Copy your bot's token

## Add Discord Bot to Server

1. Make sure you're logged on to the [Discord website](https://discord.com/).
2. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).
3. Click on your bot's page.
4. Go to the "OAuth2" tab.
5. Tick the "bot" checkbox under "scopes".
6. Tick the permissions required for your bot to function under "Bot Permissions" (Please be aware of the consequences of required your bot to have the "Administrator" permission).
7. Bot owners must have 2FA enabled for certain actions and permissions when added in servers that have Server-Wide 2FA enabled
8. Now the resulting URL can be used to add your bot to a server. Copy and paste the URL into your browser, choose a server to invite the bot to(will only allow the bot to be invited to servers where you have the "Manage Server" permissions). Then click "Authorize".


