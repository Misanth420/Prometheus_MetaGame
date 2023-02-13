import discord
from discord.ext import commands
from discord import Guild
import datetime
import asyncio


class GuardianCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        check_time = datetime.timedelta(seconds=int(5))
        naive_now = datetime.datetime.utcnow() + check_time
        aware_now = naive_now.replace(tzinfo=datetime.timezone.utc)
        if after.timed_out_until is not None and after.timed_out_until > aware_now:
            member = before.name

            time = after.timed_out_until
            print(f"{member} got timed out until {time} in {before.guild.name}")
            print(time)
            guild = before.guild
            async for entry in guild.audit_logs(limit=1):
                print(f"{entry.user} timed out {entry.target} | {entry.action}")
            await self.reversion(before, time)

    @commands.command(hidden=True)
    async def reversion(self, before: discord.Member, time):
        channel = self.bot.get_channel(1072404346299490426)
        guild = discord.Guild
        atime = datetime.timedelta(seconds=int(1))
        await channel.send(f"{before.mention} was timed out for {time}. Unban in 5")
        await asyncio.sleep(5)
        await before.edit(timed_out_until=discord.utils.utcnow() + atime)
        await channel.send(f"{before.mention} timeout removed")


async def setup(bot):
    await bot.add_cog(GuardianCog(bot))
