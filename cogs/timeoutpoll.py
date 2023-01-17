import discord
from discord.ext import commands
import datetime
import asyncio
import re
import settings

class AdminPollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command()
    async def timeoutpoll(self, ctx, poll_duration: int, offender: discord.Member, emoji_count: int, timeout_time, *, description: str):

        # Argument checks
        role = discord.utils.get(ctx.guild.roles, name=settings.DISCORD_ADMINCOG_REQ_ROLE) # temporarily defined here until expanded; string should match the role req. for invokation.
        if role not in ctx.author.roles:
            await ctx.send(f"Sorry, level up to {role} in order to cast Ice Nova ")
            return        
        if not isinstance(poll_duration, int) or poll_duration < 0:
            await ctx.send("Error: Poll Duration must be a positive integer.")
            return        
        if not isinstance(emoji_count, int) or emoji_count < 0:
            await ctx.send("Error: Emoji Count must be a positive integer.")
            return
        
        timeout_regex = r'^\d+[dhmn]$'
        if not re.match(timeout_regex, timeout_time):
            await ctx.send("Error: timeout time must be in the format of number followed by letters 'd', 'h', or 'm'. \n_For example: **5m, 1h, 7d** where **m** stands for **minutes**, **h** stands for **hours** and **d** stands for **days** respectively_")
            return
        
        timeout_unit = timeout_time[-1].lower()
        timeout_value = int(timeout_time[:-1])
        limit = {"d": 28, "h": 672, "m": 40320}
        if timeout_value > limit.get(timeout_unit, 0):
            await ctx.send(f"Error: Timeout duration cannot be longer than {limit[timeout_unit]} {timeout_unit}")
            return
        
        # POLL SETUP
        embed = discord.Embed(title='Poll', description=f"{description}\n\nMember to timeout: {offender.mention}")
        embed.set_footer(text=f'Timeout proposed by {ctx.author}')
        
        message = await ctx.send(embed=embed)        
        await message.add_reaction('👍')
        await message.add_reaction('👎')        
        await asyncio.sleep(poll_duration * 60) #lazy conversion to minutes, temporary until conditioned.

        message = await ctx.channel.fetch_message(message.id)
        await self.timeout(ctx, message, offender, emoji_count, timeout_time)


    async def timeout(self, ctx, message, offender, emoji_count, timeout_time):
                        
        if len(message.reactions) < 2:
            await ctx.send("**Vote Failed**: No votes have been recorded. Let's try again and **encourage more participation. 🏳️🏳️🏳️**")
            return
        
        thumbs_up = message.reactions[0].count - 1 # first is expected to be (thumbs up)
        thumbs_down = message.reactions[1].count - 1 # second is expected to be (thumbs down)
        member = offender

        # 'gettime' vars are defined after each check to avoid defining 3 separate 'gettime' values
        if thumbs_up >= emoji_count and thumbs_up > thumbs_down: 
            if "m" in timeout_time:
                gettime = timeout_time.strip("m")
                if int(gettime) > 40320:
                    await ctx.send("Timeout duration cannot be longer than 28 days")
                else:
                    adjusted_time = datetime.timedelta(minutes=int(gettime))
                    await member.edit(timed_out_until=discord.utils.utcnow() + adjusted_time)
                    await ctx.send(f"**{message.author.name}** _casts_ 🥶**Frostbolt**🥶! \n\n**Frostbolt** _hits_ _{member.name}_ _for **9000!**_ \n\n{member.mention} _has been_ **_chilled_** _out for:_ **_{gettime} minutes._ 🧊**")
            elif "h" in timeout_time:
                gettime = timeout_time.strip("h")
                if int(gettime) > 672:
                    await ctx.send("Timeout duration cannot be longer than 28 days")
                else:
                    adjusted_time = datetime.timedelta(hours=int(gettime))
                    await member.edit(timed_out_until=discord.utils.utcnow() + adjusted_time)
                    await ctx.send(f"**{message.author.name}** _casts_ 🧊🌟**Frost Nova**🌟🧊! \n\n**Frost Nova** _hits_ _{member.name}_ _for **9000!**_ \n\n{member.mention} _has been_ **_chilled_** _out for:_ **_{gettime} hours._ 🧊🧊**")

            elif "d" in timeout_time:
                gettime = timeout_time.strip("d")
                if int(gettime) > 28:
                    await ctx.send("Timeout duration cannot be longer than 28 days")
                else:
                    adjusted_time = datetime.timedelta(days=int(gettime))
                    await member.edit(timed_out_until=discord.utils.utcnow() + adjusted_time)
                    await ctx.send(f"**{message.author.name}** _casts_ 🧊🔥**Frostfire Bolt**🔥🧊! \n\n**Frostfire Bolt** _hits_ _{member.name}_ _for **9000!**_ \n\n{member.mention} _has been_ **_chilled_** _out for:_ **_{gettime} days._ 🧊🥶🧊**")

            else:
                await ctx.send("Invalid format for timeout_time.")
        else:
            await ctx.send("**Vote Failed**: **Voting conditions not met.** _Revolution ain't so easy._ **🏳️🏳️🏳️**")

async def setup(bot):
    await bot.add_cog(AdminPollCog(bot))