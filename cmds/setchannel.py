from discord.ext import commands
import discord
import peewee
import database
from models.schannel import SChannel


@commands.group(aliases=["set"])
async def set_channel(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"{ctx.subcommand_passed} command does not exist.")


@set_channel.command()
async def channel(ctx, channel: discord.TextChannel, purpose: str):
    if not database.mgdb.table_exists(table_name="schannel"):
        database.mgdb.create_tables([SChannel])
    try:
        schannel = SChannel.get(
            SChannel.discord_server == ctx.guild.id, SChannel.purpose == purpose
        )
        schannel.channel_id = int(channel.id)
        schannel.purpose = str(purpose)
        schannel.save()
        print("channel id and purpose updated")
        await ctx.send("Channels updated!")
    except peewee.DoesNotExist:
        schannel = SChannel.create(
            discord_server=int(ctx.guild.id), purpose=str(purpose), channel_id=channel.id
        )

        print("channel id and purpose updated")
        await ctx.send("Channels updated!")


async def setup(bot):
    bot.add_command(set_channel)
