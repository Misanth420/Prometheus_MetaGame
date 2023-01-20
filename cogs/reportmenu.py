import settings
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, Select

import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)

class ReportModal(discord.ui.Modal, title="Sup, what you've been up to?"):
    description = discord.ui.TextInput(
        style=discord.TextStyle.long,
        max_length=420,
        label="Description",
        required=True,
        placeholder="Describe what you did here..."
        )
    artefact = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Artefact",
        required=True,
        placeholder="Paste a URL relevant to your contribution here..."
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
            await self.didathing(ctx, channel)
        
        
    

        

        
            
    async def didathing(self, ctx, channel:discord.TextChannel):
        selectGuild = Select(
            placeholder="Pick a guild from the list", 
            options=[
                discord.SelectOption(
                    label="Art and Design", 
                    emoji="🎨", 
                    description="Guilds focused on artistry and design frameworks"),
                discord.SelectOption(
                    label="Building", 
                    emoji="🛠️", 
                    description="Guild focused on building MetaGame's infrastructure"),
                discord.SelectOption(
                    label="BridgeBuilding", 
                    emoji="🌉", 
                    description="Guild focused on building external relationships"),
                discord.SelectOption(
                    label="Innkeeping", 
                    emoji="🍻", 
                    description="Guild focused on community building"),
                discord.SelectOption(
                    label="Shilling and Rainmaking", 
                    emoji="📣", 
                    description="Guild focused on marketing and funding")            
        ])
        async def submissionG_callback(interaction):        
            selectGuild.callback = submissionG_callback
            await interaction.response.send_message(
                f"You are about to report under the **{selectGuild.values[0]}** banner.", ephemeral=True)

        selectEffort = Select(
            placeholder="How much effort did you put in?", 
            options=[
                discord.SelectOption(
                    label="Low Effort", 
                    emoji="1️⃣", 
                    description="Low effort. Quick and easy"),
                discord.SelectOption(
                    label="Low-Medium Effort", 
                    emoji="2️⃣", 
                    description="Not low, not medium."),
                discord.SelectOption(
                    label="Medium Effort", 
                    emoji="3️⃣", 
                    description="Medium effort. It took some time."),
                discord.SelectOption(
                    label="Medium-High Effort", 
                    emoji="4️⃣", 
                    description="Not medium, not high"),
                discord.SelectOption(
                    label="High Effort", 
                    emoji="5️⃣", 
                    description="High effort. It took a lot of time")        
        ])
        async def submissionE_callback(interaction):
            selectEffort.callback = submissionE_callback
            await interaction.response.send_message(
                f"You are about to claim that you invested **{selectEffort.values[0]}** in your contribution.", ephemeral=True)

        selectImpact = Select(
            placeholder="What is your perceived impact?", 
            options=[
                discord.SelectOption(
                    label="Low Impact", 
                    emoji="1️⃣", 
                    description="Low impact. Simple contribution."),
                discord.SelectOption(
                    label="Medium Impact", 
                    emoji="2️⃣", 
                    description="Medium impact. Valuable IMO."),
                discord.SelectOption(
                    label="High Impact", 
                    emoji="3️⃣", 
                    description="High impact. Highly valuable IMHO."),
                discord.SelectOption(
                    label="Extreme Impact", 
                    emoji="☣️", 
                    description="Extreme Impact. Will ruffle some feathers.")        
        ])
        async def submissionI_callback(interaction):
            selectImpact.callback = submissionI_callback
            await interaction.response.send_message(
                f"You are projecting that your contribution will have **{selectImpact.values[0]}**.", ephemeral=True)
        
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
        
                
        selectGuild.callback = submissionG_callback    
        selectEffort.callback = submissionE_callback
        selectImpact.callback = submissionI_callback
        report_button.callback = report
                
              
        channel = channel
        print(f"{Fore.GREEN}CHECK: Channel '{channel}' was confirmed") 
      
        view = View()
        view.add_item(selectGuild)
        view.add_item(selectEffort)
        view.add_item(selectImpact)
        view.add_item(report_button)
        await channel.send("Test", view=view)
        print(f"{Fore.GREEN}CHECK: 'report_menu' was sent successfully!")


async def setup(bot):
    await bot.add_cog(ReportCog(bot))