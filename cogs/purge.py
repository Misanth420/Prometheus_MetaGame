import discord
from discord.ext import commands


class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge", "delete"])
    async def clear(self, ctx, amount: int):
        if not ctx.message.author.guild_permissions.manage_messages:
            await ctx.send("Sorry, ask someone else, preferably a moderator")
            return

        amount = amount + 1
        if amount > 101:
            await ctx.send("Sorry, I'm not able to delete more than a 100 messages.")

        else:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"Purged {amount} messages, including your command")


async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
