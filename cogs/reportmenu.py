import settings
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal

import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)

class ReportModal(discord.ui.Modal, title="Let us know what you've been up to!"):
    description = discord.ui.TextInput(
        style=discord.TextStyle.long,
        max_length=420,
        label="Description",
        required=True,
        placeholder="Describe what you did here"
    )

    async def on_submit(self, interaction: discord.Interaction):
        ...
    async def on_error(self, interaction: discord.Interaction, error):
        ...

class ReportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def reportmenu(self, ctx, channel: discord.TextChannel=None):
        role = discord.utils.get(ctx.guild.roles, name=settings.D_REP_MENU_BUILD_ROLE)
        report_channel = (settings.D_REPORT_CHAN_ID)        
        if channel is None:
            channel = ctx.guild.get_channel(report_channel)
            print(f"{Fore.RED}CHECK: NO CHANNEL PASSED, APPLYING DEFAULT... SENDING TO '{channel}'")

        if role not in ctx.author.roles:
            await ctx.send(f"☢️`This command is for sending the report menu, not using it.`☢️\
                \n`Sorry, only {role} can use this command.`\
                \n\n`📜 If you wanted to report, please interact with the menu in` <#{report_channel}>") 
            print(f"{Fore.RED}CHECK: Role check failed. Unauthorized user named: {ctx.author}")            
        else:
            print(f"{Fore.GREEN}CHECK: Role check passed. Access granted to: {ctx.author}") 
            print(f"{Fore.GREEN}CHECK: Channel '{channel}' was passed")
            await ctx.send(f"Menu sent to {channel.mention}!")                                 
            await self.buildmenu(ctx, channel)
        
        
    async def buildmenu(self, ctx, channel: discord.TextChannel):        
        channel = channel
        print(f"{Fore.GREEN}CHECK: Channel '{channel}' was confirmed") 
            
        report_button = Button(
            label="Report Contribution",
            style=discord.ButtonStyle.blurple,
            emoji="📜"
        )

        async def report_button_callback(interaction):
            await interaction.response.send_message("You clicked!")
            print(f"{Back.GREEN}USER CHECK: 'report_button' callback was called successfully! User calling: {interaction.user}")

        async def report(interaction):
            report_modal = ReportModal()
            await interaction.response.send_modal(report_modal)

        report_button.callback = report
        
        
        view = View()
        view.add_item(report_button)
        await channel.send("Test", view=view)
        print(f"{Fore.GREEN}CHECK: 'report_menu' was sent successfully!")


async def setup(bot):
    await bot.add_cog(ReportCog(bot))