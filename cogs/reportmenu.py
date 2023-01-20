import settings
import discord
from discord.ext import commands


class ReportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reportmenu(self, ctx, channel: discord.TextChannel):

        role = discord.utils.get(ctx.guild.roles, name=settings.D_REP_MENU_BUILD_ROLE)
        report_channel = (settings.D_REPORT_CHAN_ID)
        if role not in ctx.author.roles:
            await ctx.send(f"```Sorry, only {role} can use this command.\
                \nThis command is for sending the report menu, not using it.```\
                \n`📜 If you wanted to report, please interact with the menu in` <#{report_channel}>")
        else:
            print("all good")
            return


async def setup(bot):
    await bot.add_cog(ReportCog(bot))