import discord
from discord.ext import commands
from discord import Guild
import datetime
import asyncio
import settings
import re
import peewee
from models.schannel import SChannel


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
            duration = (time - aware_now).total_seconds()
            duration = int(duration)
            print()
            print(f"{member} got timed out until {time} in {before.guild.name}")
            print(time)
            guild = before.guild
            async for entry in guild.audit_logs(limit=1):
                print(
                    f"{entry.user} timed out {entry.target} | {entry.action} |  | {entry.reason}"
                )
                reason = entry.reason
                mod = entry.user

            await self.reversion(before, after, reason, mod, duration)

    @commands.command(hidden=True)
    async def reversion(self, before: discord.Member, after, reason, mod, duration):
        chnl = SChannel.get(
            SChannel.discord_server == before.guild.id, SChannel.purpose == "voting"
        )

        channel = self.bot.get_channel(int(chnl.channel_id))
        guild = discord.Guild
        atime = datetime.timedelta(seconds=int(1))
        # await channel.send(
        #     f"{before.mention} was timed out for {after.timed_out_until}. Unban in 5"
        # )
        # await asyncio.sleep(5)
        # await before.edit(timed_out_until=discord.utils.utcnow() + atime)
        # await channel.send(f"{before.mention} timeout removed")
        offender = before.id
        # POLL SETUP
        embed = discord.Embed(
            title="Poll",
            description=f"Player {before.mention} got timed out because:\
            \n{reason}\n\n**Should we unban them**?\
            \nThey are currently timed out **FOR {duration/60} minutes**",
        )
        embed.set_footer(text=f"Timeout originally enacted by {mod}")

        message = await channel.send(embed=embed)

        if duration < 7200:
            emoji_count = 5
        else:
            emoji_count = 8
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await channel.send(
            f"```THE POLL WILL LAST: ⏲️ {duration/10/60} minutes  ⏲️\
                \nREACTIONS REQUIRED: 👍 {emoji_count} 👍\
                \n\nPlease vote by signaling with:\
                \n👍(thumbs up) if you AGREE or\
                \n(thumbs down)👎 if you DISAGREE.```"
        )

        await asyncio.sleep(duration / 10)
        message = await channel.fetch_message(message.id)
        await self.timeout(message, offender, emoji_count, channel)

    async def timeout(
        self, message, offender: discord.Member, emoji_count, channel: discord.TextChannel
    ):
        thumbs_up = message.reactions[0].count - 1  # first is expected to be (thumbs up)
        thumbs_down = message.reactions[1].count - 1  # second is expected to be (thumbs down)
        member = offender

        # 120 mins 48 hours 28 days,
        if thumbs_up >= emoji_count and thumbs_up > thumbs_down:

            adjusted_time = datetime.timedelta(seconds=int(1))
            await member.edit(timed_out_until=discord.utils.utcnow() + adjusted_time)

        else:
            await channel.send(
                "**Vote Failed**: **Voting conditions not met.** _Revolution ain't so easy._ **🏳️🏳️🏳️**"
            )


async def setup(bot):
    await bot.add_cog(GuardianCog(bot))
