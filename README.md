# Prometheus_MetaGame Details

This repository was made with the MetaGame DAO discord server in mind specifically. It is barebones and contains a single command 'timeoutpoll'. 

Credits for helping me learn how to create a bot:

https://github.com/richardschwabe 's youtube tutorial series: https://www.youtube.com/playlist?list=PLESMQx4LeD3N0-KKPPDaToZhBsom2E_Ju

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
2. Create a ```.env``` file from a copy of ```.env.sample```
3. Fill out the ```.env``` file with your discord bot token
4. ```GUILD_ID``` not needed since it's server specific; there are no commands that require it currently.
5. Run the ```./main.py``` script to start the bot

Additionally:

1. Prefix can be changed in ```./main.py```
2. Required role to call the command can be changed in ```./cogs/timeoutpoll.py```. Currently set to 'Player'
3. Goes without saying but, the bot should be hosted to have it running 24/7