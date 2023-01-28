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

from settings import (
    DISCORD_API_SECRET,
    D_GUILD_ID,
    COGS_DIR,
    TESTCOGS_DIR,
    CMDS_DIR,
    logging,
)

import database
import peewee
from models.guild import Guild

import colorama
from colorama import Back, Fore, Style

colorama.init(autoreset=True)

logger = logging.getLogger("bot")


def run():

    if not database.mgdb.table_exists(table_name="guild"):
        database.mgdb.create_tables([Guild])
        print("db created")
    else:
        try:
            guild = Guild.get(Guild.guild_id == D_GUILD_ID)
            prefix = guild.guild_prefix
            print(f"db found and prefix set to {prefix}")
        except peewee.DoesNotExist:
            guild = Guild.create(
                Guild.guild_id == D_GUILD_ID, Guild.guild_prefix == "!"
            )
            print(f"guild entry created and prefix set to default: {prefix}")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @bot.event
    async def on_ready():
        print()
        logger.info(
            f"\n\
{Style.BRIGHT}{Fore.YELLOW}USER:{Style.RESET_ALL} {Fore.CYAN}{bot.user}{Style.RESET_ALL}\n\
{Style.BRIGHT}{Fore.YELLOW}ID:{Style.RESET_ALL} {Fore.WHITE}{bot.user.id}{Style.RESET_ALL}"
        )

        print()
        for cog_file in COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
                print(
                    f"{Back.GREEN}{Fore.WHITE}{Style.BRIGHT}Extension loaded:", end=""
                )
                print(f"{f' cogs.{cog_file.name[:-3]}'}")

        for testcog_file in TESTCOGS_DIR.glob("*.py"):
            if testcog_file.name != "__init__.py":
                await bot.load_extension(f"testcogs.{testcog_file.name[:-3]}")
                print(
                    f"{Back.GREEN}{Fore.WHITE}{Style.BRIGHT}TEST Extension loaded:",
                    end="",
                )
                print(f"{f' tcogs.{testcog_file.name[:-3]}'}")

        for cmd_file in CMDS_DIR.glob("*.py"):
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
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} loaded >>{Fore.CYAN}{cog.lower()}{Fore.GREEN}<< successfully!"
            )

        except Exception as e:
            await ctx.send("`MATRIX FAILED`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to load >>{Fore.CYAN}{ctx.message.content[6:]}{Fore.YELLOW}<< . Check if spelled correctly"
            )

    @bot.command()
    async def unload(ctx, cog: str):
        try:
            await bot.unload_extension(f"cogs.{cog.lower()}")
            await ctx.send("`MATRIX UNLOADED`")
            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} unloaded >>{Fore.CYAN}{cog.lower()}{Fore.GREEN}<< successfully!"
            )
        except Exception as e:
            await ctx.send("`MATRIX FAILED`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to unload >>{Fore.CYAN}{ctx.message.content[8:]}{Fore.YELLOW}<< . Check if spelled correctly"
            )

    @bot.command()
    async def reload(ctx, cog: str):
        try:
            await bot.reload_extension(f"cogs.{cog.lower()}")
            await ctx.send("`MATRIX RELOADED`")
            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} reloaded >>{Fore.CYAN}{cog.lower()}{Fore.GREEN}<< successfully!"
            )
        except Exception as e:
            await ctx.send("`MATRIX FAILED`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to reload >>{Fore.CYAN}{ctx.message.content[8:]}{Fore.YELLOW}<< . Check if spelled correctly"
            )

    @bot.command()
    async def reloadcmd(ctx, cmd: str):
        try:
            await bot.reload_extension(f"cogs.{cmd.lower()}")
            await ctx.send("`LOCK N LOAD`")
            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.GREEN} USER >>{ctx.author}<< reloaded >>{cmd.lower()}<< successfully!"
            )
        except Exception as e:
            await ctx.send("`RELOAD JAMMED`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to reload '{ctx.message.content}'. Check if spelled correctly"
            )

    bot.run(DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
