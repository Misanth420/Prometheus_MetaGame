import discord
from discord.ext import commands
import datetime
import asyncio
import re
import settings
from models.schannel import SChannel


class ModPollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def banpoll(self, ctx, user: discord.Member, *, description: str):

        role = discord.utils.get(ctx.guild.roles, name=settings.D_TIMEOUT_USE_ROLE)
        if role not in ctx.author.roles:
            await ctx.send(f"Sorry, level up to {role} in order to cast Ice Nova ")
            return

        chnl = SChannel.get(SChannel.discord_server == ctx.guild.id, SChannel.purpose == "voting")
        channel = self.bot.get_channel(int(chnl.channel_id))
        guild = ctx.guild
        duration = 10  # 86400  # day
        emoji_count = 1

        # POLL SETUP
        embed = discord.Embed(
            title="Poll",
            description=f"{description}\n\nIt is proposed to ban {user.mention}\
            \n",
        )
        embed.set_footer(text=f"Ban proposed by {ctx.author}")

        message = await ctx.send(embed=embed)

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

        await self.unbanpollcount(message, user, guild, emoji_count, channel)

    async def unbanpollcount(
        self, message, user: discord.Member, guild, emoji_count, channel: discord.TextChannel
    ):
        thumbs_up = message.reactions[0].count - 1
        thumbs_down = message.reactions[1].count - 1

        if thumbs_up >= emoji_count and thumbs_up > thumbs_down:
            await guild.ban(user)

        else:
            await channel.send(
                f"` VOTE FAILED `: **Voting conditions not met.\
            \nExpected more than ` {emoji_count} 👍 ` but got ` {thumbs_up} 👍 `\
            \n** _Revolution ain't so easy._ **🏳️🏳️🏳️**"
            )


async def setup(bot):
    await bot.add_cog(ModPollCog(bot))
