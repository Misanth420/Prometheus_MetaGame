from discord.ext import commands
import discord

import database
import peewee
from models.guild import Guild

from settings import (
    D_GUILD_ID,
    D_REPORT_CHAN_ID,
    DISCORD_API_SECRET,
    TESTCOGS_DIR,
    COGS_DIR,
    CMDS_DIR,
)
import settings

import time
from colorama import Fore, Back, Style

from custom_classes.reportmenu import PersistentView, ReportModal

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
            guild = Guild.get(Guild.guild_id == D_GUILD_ID)
            prefix = guild.guild_prefix
            print(
                f"{tprfx}\t\tGuild found and prefix set to '{Fore.YELLOW}{prefix}{Style.RESET_ALL}'"
            )
        except peewee.DoesNotExist:
            guild = Guild.create(
                Guild.guild_id == D_GUILD_ID, Guild.guild_prefix == "!"
            )
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

            for cog_file in COGS_DIR.glob("*.py"):
                if cog_file.name != "__init__.py":
                    await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
                    print(
                        (f"{tprfx}\t\tExtension loaded:"),
                        end="",
                    )
                    print(f"{f' cogs.{cog_file.name[:-3]}'}")
            await bot.tree.sync(guild=discord.Object(id=D_GUILD_ID))

            for testcog_file in TESTCOGS_DIR.glob("*.py"):
                if testcog_file.name != "__init__.py":
                    await bot.load_extension(f"testcogs.{testcog_file.name[:-3]}")
                    print(
                        (f"{tprfx}\t\tTEST Extension loaded:"),
                        end="",
                    )
                    print(f"{f' tcogs.{testcog_file.name[:-3]}'}")
            await bot.tree.sync(guild=discord.Object(id=D_GUILD_ID))

            for cmd_file in CMDS_DIR.glob("*.py"):
                if cmd_file.name != "__init__.py":
                    await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
                    print((f"{tprfx}\t\tCommand loaded:"), end="")
                    print(f"{f' cmds.{cmd_file.name[:-3]}'}")
            await bot.tree.sync(guild=discord.Object(id=D_GUILD_ID))

    bot = PrometheusBot()

    @bot.command()
    async def prepare(ctx: commands.Context, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.guild.get_channel(D_REPORT_CHAN_ID)

        await channel.send(
            """To report a contribution, please:\n
    `✅ PICK THE CORRESPONDING ITEMS`
    `📜 add a description`
    `🔺 click submit report`
            """,
            view=PersistentView(),
        )

    bot.run(DISCORD_API_SECRET)


if __name__ == "__main__":
    run()
