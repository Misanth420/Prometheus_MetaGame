from discord.ext import commands
import discord
from settings import (
    D_GUILD_ID,
    D_REPORT_CHAN_ID,
    DISCORD_API_SECRET,
    TESTCOGS_DIR,
    COGS_DIR,
    CMDS_DIR,
)
import settings
import database
import peewee
from models.guild import Guild

import time
import asyncio
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


def run():

    if not database.mgdb.table_exists(table_name="guild"):
        database.mgdb.create_tables([Guild])
        print(f"{tprfx}Database created")
    else:
        try:
            guild = Guild.get(Guild.server_id == D_GUILD_ID)
            prefix = guild.server_prefix
            print(
                f"{tprfx}\t\tGuild found and prefix set to '{Fore.YELLOW}{prefix}{Style.RESET_ALL}'"
            )
        except peewee.DoesNotExist:
            guild = Guild.create(server_prefix="!", server_id=D_GUILD_ID)
            prefix = guild.server_prefix
            print(
                f"{tprfx}\t\tGuild table created and prefix set to default: '{Fore.YELLOW}!{Style.RESET_ALL}'"
            )

    class PrometheusBot(commands.Bot):
        def __init__(self) -> None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            super().__init__(
                command_prefix=commands.when_mentioned_or(prefix), intents=intents
            )

        async def setup_hook(self) -> None:
            self.add_view(PersistentView())

        async def on_ready(self):
            print(f"{tprfx}\t\tLogged in as {Fore.CYAN}{bot.user.name}")
            print(f"{tprfx}\t\tBOT ID {Fore.YELLOW}{bot.user.id}")
            print("--------------------------------------------")

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

            for testcog_file in TESTCOGS_DIR.glob("*.py"):
                if testcog_file.name != "__init__.py":
                    await bot.load_extension(f"testcogs.{testcog_file.name[:-3]}")
                    print(
                        (f"{tprfx}\t\tTEST EXTENSION LOADED:"),
                        end="",
                    )
                    print(f"{f' {testcog_file.name[:-3]}'}")

            await bot.tree.sync(guild=discord.Object(id=D_GUILD_ID))

    bot = PrometheusBot()

    @bot.command()
    async def prepare(ctx: commands.Context, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.guild.get_channel(D_REPORT_CHAN_ID)

        await channel.send(
            """To report a contribution, please:\n
✅ `PICK THE CORRESPONDING GUILD, EFFORT AND PROJECTED IMPACT`
📜 `ADD A DESCRIPTION`
🔺 `CLICK SUBMIT WHEN READY`
            """,
            view=PersistentView(),
        )

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
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to load >>{Fore.CYAN}{ctx.message.content[6:]}{Fore.YELLOW}<< . Check if spelled correctly"
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
        {Style.BRIGHT}{Back.BLACK}{Fore.YELLOW}USER {Fore.CYAN}{ctx.author}{Fore.YELLOW} failed to reload >>{Fore.CYAN}{ctx.message.content[8:]}{Fore.YELLOW}<< . Check if spelled correctly"
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

    bot.run(DISCORD_API_SECRET)


if __name__ == "__main__":
    run()
