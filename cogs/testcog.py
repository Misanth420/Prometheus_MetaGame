import settings
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, Select

import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

logger = settings.logging.getLogger("bot")

class ImpactSelect(discord.ui.Select):
    def __init__(self):
        options=[
                discord.SelectOption(
                    label="Low Impact", 
                    emoji="1️⃣", 
                    description="Low impact. Simple contribution. EZ"),
                discord.SelectOption(
                    label="Medium Impact", 
                    emoji="2️⃣", 
                    description="Medium impact. Decent contribution. "),
                discord.SelectOption(
                    label="High Impact", 
                    emoji="3️⃣", 
                    description="High impact. Will ruffle some feathers."),
                discord.SelectOption(
                    label="Extreme Impact", 
                    emoji="☣️", 
                    description="Extreme Impact. The world as we know it is gone.")        
        ]
        super().__init__(
            options=options, 
            placeholder="How big of an impact do you think this will have", 
            max_values=1, 
            row=2
        )
    async def callback(self, interaction: discord.Interaction):
        await self.view.select_impact(interaction, self.values)


class EffortSelect(discord.ui.Select):
    def __init__(self):        
        options=[
            discord.SelectOption(
                value="Low Effort",
                label="Low Effort", 
                emoji="⚪", 
                description="Low effort. Quick and easy"),
            discord.SelectOption(
                value="Low-Medium Effort",
                label="Low-Medium Effort", 
                emoji="🟢", 
                description="Not low, not medium."),
            discord.SelectOption(
                value="Medium Effort",
                label="Medium Effort", 
                emoji="🟡", 
                description="Medium effort. It took some time."),
            discord.SelectOption(
                value="Medium-High Effort",
                label="Medium-High Effort", 
                emoji="🟠", 
                description="Not medium, not high"),
            discord.SelectOption(
                value="High Effort",
                label="High Effort", 
                emoji="🐙", 
                description="High effort. It took a lot of time")        
        ]
        super().__init__(
            options=options, 
            placeholder="How much effort did you put in?", 
            max_values=1, 
            row=1)

    async def callback(self, interaction: discord.Interaction):
        await self.view.select_effort(interaction, self.values)
        

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
        description = self.description.value
        await interaction.response.defer()
        print(description)
        print(
            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
                {Style.BRIGHT}{Back.CYAN}{Fore.BLACK}user submitted a modal successfully")

    async def on_error(self, interaction: discord.Interaction, error):
        ...


class SubmitButton(discord.ui.View):
    add_description = None
    submit = None
   

    @discord.ui.button(
            label="add description",
            style=discord.ButtonStyle.gray,
            emoji="➕",
            row=0) 
    async def button2callback(self, interaction: discord.Interaction, button: discord.ui.Button):
                
        report_modal = ReportModal()
        await interaction.response.send_modal(report_modal)        
        print(
            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
                {Style.BRIGHT}{Back.BLACK}{Fore.GREEN}modal sent successfully")
        await interaction.followup.send("Button1 changed!. Salute!", ephemeral=True)
    
        


    @discord.ui.button(
            label="add description",
            style=discord.ButtonStyle.gray,
            emoji="📜",
            row=0)
    async def button1callback(self, interaction: discord.Interaction, button : discord.ui.Button):
        button.style=discord.ButtonStyle.green
        button.emoji="✅"
        button.label="description added!"
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Button1 changed!. Salute!", ephemeral=True)


class MyMenu(discord.ui.View):
    # def __init__(self, *, timeout=None):
    #     super().__init__(timeout=timeout)

    answer1 = None
    answer2 = None
    answer3 = None

    @discord.ui.select(
        #placeholder="Pick a guild",
        options=[
                discord.SelectOption(
                    value="Art and Design",
                    label="Art and Design", 
                    emoji="🎨", 
                    description="Guilds focused on artistry and design frameworks"),
                discord.SelectOption(
                    value="Building",
                    label="Building", 
                    emoji="🛠️", 
                    description="Guild focused on building MetaGame's infrastructure"),
                discord.SelectOption(
                    value="BridgeBuilding",
                    label="BridgeBuilding", 
                    emoji="🌉", 
                    description="Guild focused on building external relationships"),
                discord.SelectOption(
                    value="Innkeeping",
                    label="Innkeeping", 
                    emoji="🍻", 
                    description="Guild focused on community building"),
                discord.SelectOption(
                    value="Shilling and Rainmaking",
                    label="Shilling and Rainmaking", 
                    emoji="📣", 
                    description="Guild focused on marketing and funding")            
        ],
        row=0
    )
    async def select_guild(self, interaction: discord.Interaction, select_item : discord.ui.Select):
        self.answer1 = select_item.values
        #self.children[0].disabled = True
        effort_select = EffortSelect()
        self.add_item(effort_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        print(
            f"{Style.BRIGHT}{Back.GREEN}USER:{Style.RESET_ALL}\
                {Style.BRIGHT}{Fore.GREEN}'GUILD' callback was called successfully! Data passed: {Fore.MAGENTA}{self.answer1}")  

    async def select_effort(self, interaction : discord.Interaction, choices):
        self.answer2 = choices
        #self.children[1].disabled = True 
        impact_select = ImpactSelect()
        self.add_item(impact_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer() 
        print(
            f"{Style.BRIGHT}{Back.GREEN}USER:{Style.RESET_ALL}\
                {Style.BRIGHT}{Fore.GREEN}'EFFORT' callback was called successfully! Data passed: {Fore.MAGENTA}{self.answer2}")  

    async def select_impact(self, interaction : discord.Interaction, choices):
        self.answer3 = choices
        #self.children[2].disabled = True
        await interaction.message.edit(view=self) 
        await interaction.response.defer()
        self.stop()  
        print(
            f"{Style.BRIGHT}{Back.GREEN}USER:{Style.RESET_ALL}\
                {Style.BRIGHT}{Fore.GREEN}'IMPACT' callback was called successfully! Data passed: {Fore.MAGENTA}{self.answer3[:1:]}")     


class TestMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def testcommand(self, ctx):
        print(
            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
                {Style.BRIGHT}{Back.CYAN}{Fore.BLACK}user {ctx.author} successfully called testcommand")
        view = MyMenu(timeout=None)        
        await ctx.send(view=view)

        await view.wait()


        report = {
            "GUILD BANNER": view.answer1,
            "EFFORT": view.answer2,
            "IMPACT": view.answer3
        }

        await ctx.send(f"You are about to pick the following:\
            \n**GUILD BANNER: **{view.answer1}\
            \n**INVESTED EFFORT: **{view.answer2}\
            \n**PROJECTED IMPACT: **{view.answer3}", ephemeral=True)        
        print(
    f"{Style.BRIGHT}{Back.MAGENTA}{Fore.BLACK}DATA PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.MAGENTA}{report}{Style.RESET_ALL} {Fore.CYAN}by {ctx.author}")

       

        

        view3 = SubmitButton(timeout=None)
        try:
            await ctx.send(view=view3)
            print(
            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
                {Style.BRIGHT}{Back.BLACK}{Fore.GREEN}second view was sent successfully.")
        except Exception as e:
            await ctx.send("error")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
                    {Style.BRIGHT}{Back.BLACK}{Fore.RED}failed to send second view.")
  
      

async def setup(bot):
    await bot.add_cog(TestMenuCog(bot))