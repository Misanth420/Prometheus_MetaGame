from discord.ext import commands
import discord
from settings import (
    D_GUILD_ID,
    D_REPORT_CHAN_ID,
    DISCORD_API_SECRET,
    TESTCOGS_DIR,
    COGS_DIR,
    CMDS_DIR,
    CUSTOM_CLASSES_DIR,
)
import settings
import asyncio
import database
import peewee
from models.guild import Guild


import time
from colorama import Fore, Back, Style

from custom_classes.reportmenu import PersistentView


logger = settings.logging.getLogger("bot")
# colorama prefix for time prefix printing)
tprfx = (
    Back.BLACK
    + Style.BRIGHT
    + Fore.GREEN
    + time.strftime("%H:%M:%S UTC", time.gmtime())
    + Back.RESET
    + Fore.WHITE
)


def fetch_prefix(bot, message):
    if message:
        try:
            guild = Guild.get(Guild.server_id == message.guild.id)
            # guild_id = guild.server_id
            prefix = guild.server_prefix
            # print(f"guild {guild_id} found with prefix {prefix}")
            return [str(prefix)]
        except peewee.DoesNotExist:
            guild = Guild.create(server_id=message.guild.id, server_prefix="!")
            # guild_id = guild.server_id
            prefix = guild.server_prefix
            # print(f"guild {guild_id} added with prefix {prefix}")
            return [str(prefix)]
    return "!"


def run():
    class PrometheusBot(commands.Bot):
        def __init__(self) -> None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.guilds = True
            super().__init__(command_prefix=fetch_prefix, intents=intents)

        async def setup_hook(self) -> None:
            self.add_view(PersistentView())

        async def on_ready(self):
            print(f"{tprfx}\t\tLogged in as {Fore.CYAN}{bot.user.name}")
            print(f"{tprfx}\t\tBOT ID {Fore.YELLOW}{bot.user.id}")
            print("--------------------------------------------")
            await self.fetch_guilds()

            for cmd_file in CMDS_DIR.glob("*.py"):
                if cmd_file.name != "__init__.py":
                    await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
                    print((f"{tprfx}\t\tCOMMAND LOADED:"), end="")
                    print(f"{f' {cmd_file.name[:-3]}'}")

            for cog_file in COGS_DIR.glob("*.py"):
                if cog_file.name != "__init__.py":
                    await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
                    print(
                        (f"{tprfx}\t\tEXTENSION LOADED:"),
                        end="",
                    )
                    print(f"{f' {cog_file.name[:-3]}'}")
            await bot.tree.sync()  # guild=discord.Object(id=D_GUILD_ID)
            print(f"{tprfx}\t\tCOGS SYNCED")

            for class_file in CUSTOM_CLASSES_DIR.glob("*.py"):
                if class_file.name != "__init__.py":
                    await bot.load_extension(f"custom_classes.{class_file.name[:-3]}")
                    print(
                        (f"{tprfx}\t\tEXTENSION LOADED:"),
                        end="",
                    )
                    print(f"{f' {class_file.name[:-3]}'}")
            # await bot.tree.sync()  # guild=discord.Object(id=D_GUILD_ID)
            print(f"{tprfx}\t\tCUSTOM CLASSES SYNCED")

            for testcog_file in TESTCOGS_DIR.glob("*.py"):
                if testcog_file.name != "__init__.py":
                    await bot.load_extension(f"testcogs.{testcog_file.name[:-3]}")
                    print(
                        (f"{tprfx}\t\tTEST EXTENSION LOADED:"),
                        end="",
                    )
                    print(f"{f' {testcog_file.name[:-3]}'}")

        async def fetch_guilds(self):
            if not database.mgdb.table_exists(table_name="guild"):
                database.mgdb.create_tables([Guild])
                print(f"{tprfx}Database created")
            else:
                guild_list = [
                    (guild.server_id, guild.server_prefix)
                    for guild in Guild.select(Guild.server_id, Guild.server_prefix)
                ]

                print(f"{tprfx}\t\tDatabase found.")
                print(f"{tprfx}\t\t{guild_list}")
                print()

    bot = PrometheusBot()

    @bot.event
    async def on_guild_join(guild):
        print(f"{tprfx}\t\tPrometheus was added to a server: {guild.name}")
        try:
            guild = Guild.get(Guild.server_id == guild.id)
            print(f"{tprfx}\t\tGuild already present. Continuing..")

        except peewee.DoesNotExist:
            guild = Guild.create(server_prefix="!", server_id=guild.id)
            print(f"{tprfx}\t\tDatabase entry created with default prefix '!' ")

    @bot.event
    async def on_guild_remove(guild):
        print(f"{tprfx}\t\tPrometheus was removed from a server: {guild.name}")
        guild = Guild.get(Guild.server_id == guild.id)
        guild.delete_instance()
        print(f"{tprfx}\t\tDatabase entry removed succesful.")

    @bot.command()
    async def set_prefix(ctx: commands.Context, new_prefix: str):
        guild = Guild.get(Guild.server_id == ctx.message.guild.id)
        guild.server_prefix = str(new_prefix)
        guild.save()
        print(f"guild {ctx.message.guild.id} updated with prefix {new_prefix}")
        await ctx.send(f"`PREFIX UPDATED` New prefix set to {new_prefix}")

    @bot.command()
    async def loadcog(ctx, cog: str):
        try:
            await bot.load_extension(f"cogs.{cog.lower()}")
            await ctx.send(f"`{cog} MATRIX HAS BEEN LOADED`")
            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} loaded >>{Fore.CYAN}{cog.lower()}{Fore.GREEN}<< successfully!"
            )

        except Exception as e:
            await ctx.send(f"`{cog} MATRIX HAS FAILED TO LOAD`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to load >>{Fore.CYAN}{ctx.message.content[9:]}{Fore.YELLOW}<< . Check if spelled correctly"
            )

    @bot.command()
    async def unloadcog(ctx, cog: str):
        try:
            await bot.unload_extension(f"cogs.{cog.lower()}")
            await ctx.send(f"`{cog} MATRIX HAS BEEN UNLOADED`")
            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} unloaded >>{Fore.CYAN}{cog.lower()}{Fore.GREEN}<< successfully!"
            )
        except Exception as e:
            await ctx.send(f"`{cog} MATRIX FAILED TO UNLOAD`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to unload >>{Fore.CYAN}{ctx.message.content[8:]}{Fore.YELLOW}<< . Check if spelled correctly"
            )

    @bot.command()
    async def reloadcog(ctx, cog: str):
        try:
            await bot.reload_extension(f"cogs.{cog.lower()}")
            await ctx.send(f"`{cog} MATRIX HAS BEEN RELOADED`")
            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} reloaded >>{Fore.CYAN}{cog.lower()}{Fore.GREEN}<< successfully!"
            )
        except Exception as e:
            await ctx.send(f"`{cog} MATRIX FAILED TO RELOAD`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to reload >>{Fore.CYAN}{ctx.message.content[11:]}{Fore.YELLOW}<< . Check if spelled correctly"
            )

    @bot.command()
    async def testreload(ctx, testcog: str):
        try:
            await bot.reload_extension(f"testcogs.{testcog.lower()}")
            await ctx.send(f"`{testcog} MATRIX HAS BEEN RELOADED`")
            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} reloaded >>{Fore.CYAN}{testcog.lower()}{Fore.GREEN}<< successfully!"
            )
        except Exception as e:
            await ctx.send(f"`{testcog} MATRIX FAILED TO LOAD`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to reload >>{Fore.CYAN}{ctx.message.content[12:]}{Fore.YELLOW}<< . Check if spelled correctly"
            )

    @bot.command()
    async def reloadcmd(ctx, cmd: str):
        try:
            await bot.reload_extension(f"cmds.{cmd.lower()}")
            await ctx.send(f"`LOCK N LOAD, {cmd} RELOADED`")
            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.GREEN} USER >>{ctx.author}<< reloaded >>{cmd.lower()}<< successfully!"
            )
        except Exception as e:
            await ctx.send(f"`RELOAD JAMMED, {cmd} FAILED TO RELOAD`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to reload '{ctx.message.content}'. Check if spelled correctly"
            )

    @bot.command()
    async def reloadclass(ctx, custom_classes: str):
        try:
            await bot.reload_extension(f"custom_classes.{custom_classes.lower()}")
            await ctx.send(f"`{custom_classes} MATRIX HAS BEEN RELOADED`")
            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Fore.GREEN}USER {Back.BLACK}{Fore.CYAN}{ctx.author}{Fore.GREEN} reloaded >>{Fore.CYAN}{custom_classes.lower()}{Fore.GREEN}<< successfully!"
            )

        except Exception as e:
            await ctx.send(f"`{custom_classes} MATRIX HAS FAILED TO LOAD`")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to load >>{Fore.CYAN}{ctx.message.content[13:]}{Fore.YELLOW}<< . Check if spelled correctly"
            )

    bot.run(DISCORD_API_SECRET)


if __name__ == "__main__":
    run()
