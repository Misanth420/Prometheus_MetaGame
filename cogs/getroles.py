from discord.ext import commands
import discord
from settings import D_TESTGUILD_ID


class RoleSelectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    message = None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        role1 = discord.utils.get(payload.member.guild.roles, name="mgplayer")
        role2 = discord.utils.get(payload.member.guild.roles, name="mgmoderator")

        if self.message.id == payload.message_id:
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

        if self.message.id == payload.message_id:
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
            print("wrong guild")
            return
        if channel is None:
            await ctx.send(
                f"No channel specified. Please tell me where to send the menu\
                \nFormat: `rolemenu #channelname`"
            )
        await ctx.send(f"menu sent to {channel.mention}")
        self.channel = channel
        self.message = await channel.send(
            f"React with the appropriate emoji to get the roles\
required for using various commands:\
\n```🕹️ - Player Role (You need to be a player to call a timeout poll)\
\n👮 - Mod role (You need to be a mod to assemble the report menu.\
Anyone can use the menu after it was sent)```"
        )
        await self.message.add_reaction("🕹️")
        await self.message.add_reaction("👮")


async def setup(bot):
    await bot.add_cog(RoleSelectCog(bot))
