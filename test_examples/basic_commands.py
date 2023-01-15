import settings
import discord
from discord.ext import commands
import random

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command(
        aliases=['p'],
        help="This is help",
        description="This is a description",
        brief="This is a brief",
        hidden=True
    )
    async def ping(ctx):
        """ Returns pong """
        await ctx.send("pong")

    @bot.command()
    async def say(ctx, *what):        
        await ctx.send(" ".join(what))
    @bot.command()
    async def say2(ctx, what = "WHAT?!?"): 
        await ctx.send(" ".join(what))

    @bot.command()
    async def choices(ctx, *options):        
        await ctx.send(random.choice(options))


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()