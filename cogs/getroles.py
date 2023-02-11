from discord.ext import commands
import discord
from settings import D_TESTGUILD_ID

import database
import peewee
from models.msgpersist import PersMessage, Guild
import asyncio


class RoleSelectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        role1 = discord.utils.get(payload.member.guild.roles, name="mgplayer")
        role2 = discord.utils.get(payload.member.guild.roles, name="mgmoderator")
        pmessage = PersMessage.get(PersMessage.purpose == "getroles")
        message = int(pmessage.message_id)
        payload_message = int(payload.message_id)

        if message == payload_message:
            if payload.member.id == self.bot.user.id:
                return
            elif payload.emoji.name == "🕹️":
                await payload.member.add_roles(role1)
            elif payload.emoji.name == "👮":
                await payload.member.add_roles(role2)
            else:
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        member = await (await self.bot.fetch_guild(payload.guild_id)).fetch_member(
            payload.user_id
        )
        role1 = discord.utils.get(member.guild.roles, name="mgplayer")
        role2 = discord.utils.get(member.guild.roles, name="mgmoderator")
        pmessage = PersMessage.get(PersMessage.purpose == "getroles")
        message = int(pmessage.message_id)
        payload_message = int(payload.message_id)

        if message == payload_message:
            if member.id == self.bot.user.id:
                return
            elif payload.emoji.name == "🕹️":
                await member.remove_roles(role1)
            elif payload.emoji.name == "👮":
                await member.remove_roles(role2)
            else:
                return

    @commands.command()
    async def rolemenu(
        self, ctx: commands.Context, channel: discord.TextChannel = None
    ):
        testguild = D_TESTGUILD_ID
        if ctx.guild.id == testguild:
            print(f"guild check passed = {testguild}")
        else:
            print(f"wrong guild attempted - {ctx.guild.name}")
            return
        if channel is None:
            await ctx.send(
                f"No channel specified. Please tell me where to send the menu\
                \nFormat: `rolemenu #channelname`"
            )
            return
        await ctx.send(f"menu sent to {channel.mention}")
        # channel = channel
        message = await channel.send(
            f"React with the appropriate emoji to get the roles\
 required for using various commands:\
\n```🕹️ - Player Role (You need to be a player to call a timeout poll)\
\n👮 - Mod role (You need to be a mod to assemble the report menu.\
 Anyone can use the menu after it was sent)```"
        )
        self.message = message

        await self.store_message(ctx, self.message, channel)

    async def store_message(self, ctx, message, channel):
        if not database.mgdb.table_exists(table_name="persmessage"):
            database.mgdb.create_tables([PersMessage])
        try:
            pmessage = PersMessage.get(PersMessage.purpose == "getroles")
            pmessage.message_id = int(message.id)
            pmessage.channel_id = int(channel.id)
            pmessage.save()
            print("message id updated")
        except peewee.DoesNotExist:
            pmessage = PersMessage.create(
                discord_server=ctx.guild.id,
                purpose="getroles",
                channel_id=channel.id,
                message_id=message.id,
            )
            print("message id added to db")

        await self.message.add_reaction("🕹️")
        await self.message.add_reaction("👮")
        await asyncio.sleep(1)


async def setup(bot):
    await bot.add_cog(RoleSelectCog(bot))
