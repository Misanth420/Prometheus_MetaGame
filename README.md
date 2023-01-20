 Prometheus_MetaGame Details

This repository was made with the MetaGame DAO discord server in mind specifically. It is barebones and contains a single command 'timeoutpoll'. 

Credits for helping me learn how to create a bot:

https://github.com/richardschwabe 's [youtube tutorial series](https://www.youtube.com/playlist?list=PLESMQx4LeD3N0-KKPPDaToZhBsom2E_Ju)

Also, thanks @Polimyl for suggesting me to go with python instead of javascript. 

# Description
This is a discord.py 2 bot that allows any user with the specified role to create a voting poll and timeout any user(except server owner). Based on the results, the bot will either timeout the tagged user for the specified duration or return the appropriate error, depending on its origin(Vote count, Permissions, ..)

Currently, the bot includes:
- Logging 
- Automatic Cog Loading - Running the bot automatically loads cogs from /cogs
- Load, Unload and Reload commands for cogs
- Slash command utilization via hybrid commands
- Test examples - included in '/test_examples' for future expansion. 

# Setup
1. Create a ```logs``` folder in the root directory. This is needed since error logging is included. Optional if logging is removed from main.py. 
2. Create a ```.env``` file from a copy of ```.env.sample```.
3. Fill out the ```.env``` file with your discord bot token. Check below for instructions on how to get the token if you don't have one.
5. Setup the virtual environment following the instructions on [Discord.py Docs](https://discordpy.readthedocs.io/en/stable/intro.html)
6. Run the ```./main.py``` script to start the bot.

## Additionally:

1. Prefix can be changed in ```./main.py```
2. Required role to call the command can be changed in ```./cogs/timeoutpoll.py```. Currently set to 'Player'
3. Goes without saying but, the bot should be hosted to have it running 24/7

## Discord Bot Token 

It is important to note the Bot requires the following intents enabled in the Discord's developers portal:

1. Presence Intent
2. Server Members Intent
3. Message Content Intent

**Registering the bot and getting the token**

1. Navigate to https://discord.com/developers/applications and login
2. Create a new application by clicking the button in the top right ```New Application```
3. Fill out general info and navigate to the ```Bot``` tab on the right hand side
4. Name your bot and fill out info
5. Make sure you leave ```OAUTH2 CODE GRANT``` disabled
6. Enable intents listed above and save
7. Navigate to the ```OAuth2 - URL GENERATOR``` on the right hand side
8. For SCOPES pick ```bot``` and for BOT PERMISSIONS pick ```Administrator```. It is usually recommended to pick exact permissions if full admin isn't needed. Caution 
9. URL should be generated on the bottom. That is your bot invite link. Use it to invite your newly created bot to the server
10. Back in the ```Bot``` tab, click on ```Reset Token``` to generate your Discord Bot token and store it securely. This token should be placed in the bots ```.env``` file you'll create during setup.