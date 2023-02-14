from discord.ext import commands
import discord
import io
import csv

from models.report import Report
import datetime


@commands.group()
async def getcsv(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"Please specify a user.")


@getcsv.command()
async def user(ctx, user: discord.Member):
    time = datetime.datetime.utcnow()
    ftime = time.strftime("%Y-%B-%d %H:%M")
    filename = f"{user.name}-{ftime}.csv"
    with io.StringIO() as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "GUILDBANNER",
                "EFFORT",
                "IMPACT",
                "DESCRIPTION",
                "ARTEFACT",
                "TIMESTAMP",
            ]
        )
        for report in Report.select().where(
            Report.server == ctx.guild.id, Report.user_discord_id == user.id
        ):

            writer.writerow(
                [
                    report.guildbanner,
                    report.effort,
                    report.impact,
                    report.description,
                    report.artefact,
                    report.date,
                ]
            )
        file.seek(0)
        await ctx.channel.send(
            content=(f"**{user.name}**'s report log as of `{ftime} UTC` is attached below.\n"),
            file=discord.File(fp=file, filename=filename),
        )


async def setup(bot):
    bot.add_command(getcsv)
