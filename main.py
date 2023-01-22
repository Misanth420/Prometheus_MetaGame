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
        print()
        logger.info(f"\n\
{Style.BRIGHT}{Fore.YELLOW}USER:{Style.RESET_ALL} {Fore.CYAN}{bot.user}{Style.RESET_ALL}\n\
{Style.BRIGHT}{Fore.YELLOW}ID:{Style.RESET_ALL} {Fore.WHITE}{bot.user.id}{Style.RESET_ALL}")    
        
        print()
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
        try:
            await bot.load_extension(f"cogs.{cog.lower()}")
            await ctx.send("`MATRIX LOADED`")
            print(
    f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} loaded >>{Fore.CYAN}{cog.lower()}{Fore.GREEN}<< successfully!")            
        
        except Exception as e:
            await ctx.send("`MATRIX FAILED`")
            print(
    f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to load >>{Fore.CYAN}{ctx.message.content[6:]}{Fore.YELLOW}<< . Check if spelled correctly")

        
    @bot.command()
    async def unload(ctx, cog: str):
        try:
            await bot.unload_extension(f"cogs.{cog.lower()}")
            await ctx.send("`MATRIX UNLOADED`")
            print(
    f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} unloaded >>{Fore.CYAN}{cog.lower()}{Fore.GREEN}<< successfully!")
        except Exception as e:
            await ctx.send("`MATRIX FAILED`")
            print(
    f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to unload >>{Fore.CYAN}{ctx.message.content[8:]}{Fore.YELLOW}<< . Check if spelled correctly")
        
    @bot.command()
    async def reload(ctx, cog: str):
        try:
            await bot.reload_extension(f"cogs.{cog.lower()}")
            await ctx.send("`MATRIX RELOADED`")
            print(
    f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} reloaded >>{Fore.CYAN}{cog.lower()}{Fore.GREEN}<< successfully!")
        except Exception as e:
            await ctx.send("`MATRIX FAILED`")
            print(
    f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to reload >>{Fore.CYAN}{ctx.message.content[8:]}{Fore.YELLOW}<< . Check if spelled correctly")



    @bot.command()
    async def reloadcmd(ctx, cmd: str):
        try:
            await bot.reload_extension(f"cogs.{cmd.lower()}")
            await ctx.send("`LOCK N LOAD`")
            print(
    f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.GREEN} USER >>{ctx.author}<< reloaded >>{cmd.lower()}<< successfully!")
        except Exception as e:
            await ctx.send("`RELOAD JAMMED`")
            print(
    f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to reload '{ctx.message.content}'. Check if spelled correctly")



        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()