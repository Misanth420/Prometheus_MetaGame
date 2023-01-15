import settings
import discord
from discord.ext import commands
import random

logger = settings.logging.getLogger("bot")
class Slapper(commands.Converter):

    async def convert( self, ctx, argument):
        someone = random.choice(ctx.guild.members).name
        return f"{ctx.author.display_name} slaps {someone} with {argument}"

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    

    @bot.command()
    async def joined(ctx, who : discord.Member ):
        await ctx.send(who.joined_at)

    @bot.command()
    async def slap(ctx, reason : Slapper ):
        await ctx.send(reason)


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()