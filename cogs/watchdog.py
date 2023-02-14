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
    async def on_member_ban(self, guild, user):
        chnl = SChannel.get(SChannel.discord_server == user.guild.id, SChannel.purpose == "voting")
        channel = self.bot.get_channel(int(chnl.channel_id))
        duration = 86400  # day
        emoji_count = 8

        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1):

            print(f"{entry.user} banned {entry.target} | {entry.action} |  | {entry.reason}")
            reason = entry.reason
            mod = entry.user

        embed = discord.Embed(
            title="Poll",
            description=f"Player {user.mention} got permabanned because:\
            \n{reason}\n\n**Should we unban them**?",
        )
        embed.set_footer(text=f"Banhammer originally wielded by {mod}")
        message = await channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await channel.send(
            f"```THE POLL WILL LAST: ⏲️ {duration/60/60} hours  ⏲️\
                \nREACTIONS REQUIRED: 👍 {emoji_count} 👍\
                \n\nPlease vote by signaling with:\
                \n👍(thumbs up) if you AGREE or\
                \n(thumbs down)👎 if you DISAGREE.```"
        )
        await asyncio.sleep(duration)
        message = await channel.fetch_message(message.id)
        await self.timeout(message, user, guild, emoji_count, channel)

    async def timeout(
        self, message, user: discord.Member, guild, emoji_count, channel: discord.TextChannel
    ):
        thumbs_up = message.reactions[0].count - 1
        thumbs_down = message.reactions[1].count - 1

        if thumbs_up >= emoji_count and thumbs_up > thumbs_down:
            await guild.unban(user)

        else:
            await channel.send(
                f"` VOTE FAILED `: **Voting conditions not met.\
            \nExpected more than ` {emoji_count} 👍 ` but got ` {thumbs_up} 👍 `\
            \n** _Revolution ain't so easy._ **🏳️🏳️🏳️**"
            )

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

        async def timer(bot, duration):
            duration = datetime.timedelta(seconds=int(duration))
            time_remaining = datetime.datetime.utcnow() + duration

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
        thumbs_up = message.reactions[0].count - 1
        thumbs_down = message.reactions[1].count - 1
        member = offender

        if thumbs_up >= emoji_count and thumbs_up > thumbs_down:

            adjusted_time = datetime.timedelta(seconds=int(1))
            await member.edit(timed_out_until=discord.utils.utcnow() + adjusted_time)

        else:
            await channel.send(
                "**Vote Failed**: **Voting conditions not met.** _Revolution ain't so easy._ **🏳️🏳️🏳️**"
            )

    @commands.command()
    async def unban(self, ctx, user: discord.User):
        guild = ctx.guild
        useravatar = user.display_avatar
        await guild.unban(user=user)
        embed = discord.Embed(
            title="Mod Action",
            description=(f"Successfully unbanned ` {user.name} `"),
            colour=discord.Colour.red(),
        )
        embed.set_thumbnail(url=useravatar)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GuardianCog(bot))
