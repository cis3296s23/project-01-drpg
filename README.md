# DungeonRPG
Dungeon RPG is a Discord bot that allows players to engage in combat and have fun on the Discord platform using the Discord API Framework utilizing Python as the programming language 

# How to run
 - Download the latest release
 - Open the code in an IDE/terminal and move files into the directory of the project
 - Setup Discord bot as shown in [Technical Information](#technical-information)
```
create a file called TOKEN.txt in the directory and place the API token there.
```
- Install Discord API
  - Go to terminal, and enter below
```
pip install discord.py
pip install pillow
```
-  Run main.py, and the discord bot should run in the server

# Technical Information 

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
6. Tick the permissions required for your bot to function under "Bot Permissions" (All permissions or simply the Admin permissions)
7. Bot owners must have 2FA enabled for certain actions and permissions when added in servers that have Server-Wide 2FA enabled
8. Now the resulting URL can be used to add your bot to a server. Copy and paste the URL into your browser, choose a server to invite the bot to(will only allow the bot to be invited to servers where you have the "Manage Server" permissions). Then click "Authorize".

## How To Play
- !help - get the help message
- !dungeon - spawn dungeon map to play
- !move - to move within dungeon, call !move and the desired coordinates (ex. !move d3)
Notes - to fight, walk over to an opponent
Fight commands - !fight, !counter, !auto
Fight is a single turn attack, counter is chance to dodge and deal great damage, Auto is to run the fight automatically
Get to the door to beat the level and level up!
