#
#     ▄███████▄    ▄████████  ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄████████     ███        ▄█    █▄       ▄████████ ███    █▄     ▄████████ 
#    ███    ███   ███    ███ ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ▀█████████▄   ███    ███     ███    ███ ███    ███   ███    ███ 
#    ███    ███   ███    ███ ███    ███ ███   ███   ███   ███    █▀     ▀███▀▀██   ███    ███     ███    █▀  ███    ███   ███    █▀  
#    ███    ███  ▄███▄▄▄▄██▀ ███    ███ ███   ███   ███  ▄███▄▄▄         ███   ▀  ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███    ███   ███        
#  ▀█████████▀  ▀▀███▀▀▀▀▀   ███    ███ ███   ███   ███ ▀▀███▀▀▀         ███     ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███    ███ ▀███████████ 
#    ███        ▀███████████ ███    ███ ███   ███   ███   ███    █▄      ███       ███    ███     ███    █▄  ███    ███          ███ 
#    ███          ███    ███ ███    ███ ███   ███   ███   ███    ███     ███       ███    ███     ███    ███ ███    ███    ▄█    ███ 
#   ▄████▀        ███    ███  ▀██████▀   ▀█   ███   █▀    ██████████    ▄████▀     ███    █▀      ██████████ ████████▀   ▄████████▀  
#                 ███    ███                                                                                                   
#




import discord 
from discord.ext import commands
import settings
import colorama
from colorama import Back, Fore, Style
colorama.init(autoreset=True)
    
logger = settings.logging.getLogger("bot")
    
def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"{Fore.YELLOW}USER: {Fore.WHITE}{bot.user}  {Fore.YELLOW}ID: {Fore.WHITE}{bot.user.id}")
        
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
                print(f"{Back.GREEN}{Fore.WHITE}{Style.BRIGHT}Extension loaded:", end="")
                print(f"{f' cogs.{cog_file.name[:-3]}'}")

        
        for cmd_file in settings.CMDS_DIR.glob("*.py"):
            if cmd_file.name != "__init__.py":                
                await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
                print(f"{Back.GREEN}{Fore.WHITE}{Style.BRIGHT}Command loaded:", end="") 
                print(f"{f' cmds.{cmd_file.name[:-3]}'}")
        await bot.tree.sync()
        
    @bot.command()
    async def load(ctx, cog: str):
        await bot.load_extension(f"cogs.{cog.lower()}")
        print(f"{Back.YELLOW}{ctx.author} Loaded {cog.lower()} Class")
        
    @bot.command()
    async def unload(ctx, cog: str):
        await bot.unload_extension(f"cogs.{cog.lower()}")
        print(f"{Back.YELLOW}{ctx.author} Unloaded {cog.lower()} Class")
        
    @bot.command()
    async def reload(ctx, cog: str):
        await bot.reload_extension(f"cogs.{cog.lower()}")
        print(f"{Back.YELLOW}{ctx.author} Reloaded {cog.lower()} Class")

    @bot.command()
    async def reloadcmd(ctx, cmd: str):
        await bot.reload_extension(f"cogs.{cmd.lower()}")

        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()