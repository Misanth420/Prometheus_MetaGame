import discord
from discord.ext import commands
import peewee
import database
from models.report import Report
import datetime


class FetchDataCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["stats"])
    async def reportstats(self, ctx, user: discord.Member = None):
        if user is None:
            server = ctx.guild.id
            report = Report.get(Report.server == server)
            # general number of reports; move all these into a separate funct
            now = datetime.datetime.utcnow()
            day_ago = now - datetime.timedelta(days=1)
            week_ago = now - datetime.timedelta(days=7)
            month_ago = now - datetime.timedelta(days=30)
            day_report = Report.select().where(Report.date >= day_ago)
            week_report = Report.select().where(Report.date >= week_ago)
            month_report = Report.select().where(Report.date >= month_ago)
            total_report = Report.select().where(Report.server == ctx.guild.id)

            art_report = Report.select().where(Report.guildbanner == "Art and Design")
            buidl_report = Report.select().where(Report.guildbanner == "Building")
            bridgebuidl_report = Report.select().where(Report.guildbanner == "BridgeBuilding")
            innkeep_report = Report.select().where(Report.guildbanner == "Innkeeping")
            shill_report = Report.select().where(Report.guildbanner == "Shilling and Rainmaking")

            num_day = day_report.count()
            num_week = week_report.count()
            num_month = month_report.count()
            num_total = total_report.count()
            num_total_art = art_report.count()
            num_total_buidl = buidl_report.count()
            num_total_bridgebuidl = bridgebuidl_report.count()
            num_total_innkeep = innkeep_report.count()
            num_total_shill = shill_report.count()

            embed = discord.Embed(
                colour=discord.Colour.dark_purple(),
                description=(
                    f"There are a total of ` {num_total} report(s) ` found for ` {ctx.guild.name} `.\
            \nThat includes:\n`{num_total_art} ART reports`,\n`{num_total_buidl} BUIDL reports`,\
            \n`{num_total_bridgebuidl} BRIDGEBUIDL reports`,\
            \n`{num_total_innkeep} INNKEEP reports` and \n`{num_total_shill} SHILL reports.`"
                ),
                title="General report stats",
                timestamp=datetime.datetime.now(),
            )
            embed.set_author(name=ctx.guild.name)
            embed.add_field(
                name="PAST DAY",
                value=f"There are a total of ` {num_day} report(s) ` posted today.",
                inline=False,
            )
            embed.add_field(
                name="PAST 7 DAYS",
                value=f"There are a total of ` {num_week} report(s) ` in the past 7 days",
                inline=False,
            )
            embed.add_field(
                name="PAST 30 DAYS",
                value=f"There are a total of ` {num_month} report(s) ` in the past 30 days",
                inline=False,
            )
            embed.add_field

            await ctx.send(embed=embed)
        else:
            server = ctx.guild.id
            report = Report.get(Report.server == server)

            now = datetime.datetime.utcnow()
            week_ago = now - datetime.timedelta(days=7)
            month_ago = now - datetime.timedelta(days=30)
            week_report = Report.select().where(
                Report.date >= week_ago, Report.user_discord_id == user.id
            )
            month_report = Report.select().where(
                Report.date >= month_ago, Report.user_discord_id == user.id
            )
            total_report = Report.select().where(Report.user_discord_id == user.id)

            art_report = Report.select().where(
                Report.guildbanner == "Art and Design", Report.user_discord_id == user.id
            )
            buidl_report = Report.select().where(
                Report.guildbanner == "Building", Report.user_discord_id == user.id
            )
            bridgebuidl_report = Report.select().where(
                Report.guildbanner == "BridgeBuilding", Report.user_discord_id == user.id
            )
            innkeep_report = Report.select().where(
                Report.guildbanner == "Innkeeping", Report.user_discord_id == user.id
            )
            shill_report = Report.select().where(
                Report.guildbanner == "Shilling and Rainmaking", Report.user_discord_id == user.id
            )

            num_week = week_report.count()
            num_month = month_report.count()
            num_total = total_report.count()
            num_total_art = art_report.count()
            num_total_buidl = buidl_report.count()
            num_total_bridgebuidl = bridgebuidl_report.count()
            num_total_innkeep = innkeep_report.count()
            num_total_shill = shill_report.count()

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(0, 255, 255),
                description=(
                    f"There are a total of ` {num_total} report(s) ` found for ` {user.name} `.\n.\
            \nThat includes:\n`{num_total_art} ART reports`,\n`{num_total_buidl} BUIDL reports`,\
            \n`{num_total_bridgebuidl} BRIDGEBUIDL reports`,\
            \n`{num_total_innkeep} INNKEEP reports` and \n`{num_total_shill} SHILL reports.`"
                ),
                title="General report stats",
                timestamp=datetime.datetime.now(),
            )

            embed.set_author(name=ctx.guild.name)
            embed.add_field(
                name="PAST 7 DAYS",
                value=f"There are a total of ` {num_week} report(s) ` in the past 7 days",
                inline=False,
            )
            embed.add_field(
                name="PAST 30 DAYS",
                value=f"There are a total of ` {num_month} report(s) ` in the past 30 days",
                inline=False,
            )

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(FetchDataCog(bot))
