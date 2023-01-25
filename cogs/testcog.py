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

        description_output = self.description 
        artefact_output = self.artefact 

        
        
        try: 
            await interaction.response.defer() 
            await SubmitButtonView.modalcallback(self, interaction, description_output, artefact_output)
            

            print(
        f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.CYAN}{Fore.BLACK}user submitted a modal successfully")          
            print(
        f"{Style.BRIGHT}{Back.MAGENTA}{Fore.BLACK}DATA PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.MAGENTA}{description_output}, {artefact_output} | {Style.RESET_ALL} {Fore.CYAN}by {interaction.user}")


            self.stop()

        
        except Exception as e:
            print(e)
            logger.exception("An exception occurred")
        


    async def on_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Something went wrong. Modal NOT submitted.")
        print(
            f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
                {Style.BRIGHT}{Back.BLACK}{Fore.RED}failed to submit modal.")



class SubmitButtonView(discord.ui.View):
    
    
    artefact = None
    description = None
    descriptionreply = None
    artefactreply = None
    
    foo : bool = None
    

    async def disable_menu(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.message.channel.send("timed out..")
        await self.disable_menu()



    @discord.ui.button(
            label="add description",
            style=discord.ButtonStyle.gray,
            emoji="➕",
            row=0) 
    async def button1callback(self, interaction: discord.Interaction, button: discord.ui.Button): 
                
        report_modal = ReportModal()
        report_modal.user = interaction.user
        
        await interaction.response.send_modal(report_modal)        
        print(
            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
                {Style.BRIGHT}{Back.BLACK}{Fore.GREEN}modal sent successfully")
        #await report_modal.on_submit(interaction)
        await report_modal.wait()
        
        
        

    @discord.ui.button(
            label="Submit Report",
            style=discord.ButtonStyle.gray,
            emoji="📜",
            row=0)
    async def button2callback(self, interaction: discord.Interaction, button : discord.ui.Button):
        button.style=discord.ButtonStyle.green
        button.emoji="✅"
        button.label="description submitted!" 
        await self.disable_menu()       
        await interaction.response.edit_message(view=self)
        
        
        #await interaction.response.defer()
        print(
            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
                {Style.BRIGHT}{Back.BLACK}{Fore.GREEN}report submitted and buttons view locked successfully")
         
        self.foo = True
        self.stop()
        

    async def modalcallback(self, interaction : discord.Interaction, description_output, artefact_output):
        
        self.descriptionreply = description_output
        self.artefactreply = artefact_output
        #print(f"DATA PASSED: {self.description}, {self.artefact}. modal callback reached")
        logger.info(f"User is submitting description: {self.descriptionreply} and artefact: {self.artefactreply}")
        await interaction.followup.send(f"You are about to submit the following:\
            \n`DESCRIPTION`\
            \n**_{self.description}_**\
            \n`ARTEFACT`\
            \n_{self.artefact}_")
        logger.info("Submission process completed.")
        
        self.stop()
    


    

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
    async def tc(self, ctx):
        print(
            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
                {Style.BRIGHT}{Back.CYAN}{Fore.BLACK}user {ctx.author} successfully called testcommand")
        view = MyMenu(timeout=None)        
        await ctx.send(view=view)

        await view.wait()



        view2 = SubmitButtonView(timeout=None)
        print("PROGRAM STILL RUNNING")

        
        try:
            message = await ctx.send(view=view2)
            view2.message = message
            print(
            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
                {Style.BRIGHT}{Back.BLACK}{Fore.GREEN}buttons view sent successfully!")
            
        except Exception as e:
            await ctx.send("error")
            print(
                f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
                    {Style.BRIGHT}{Back.BLACK}{Fore.RED}failed to send buttons view.")

        print("PROGRAM STILL RUNNING 2")

        

        await ctx.send(f"You are about to pick the following:\
            \n`GUILD BANNER: `_{view.answer1}_\
            \n`INVESTED EFFORT: `_{view.answer2}_\
            \n`PROJECTED IMPACT: `_{view.answer3}_")        
        
        
        print(
        f"{Style.BRIGHT}{Back.MAGENTA}{Fore.BLACK}DATA PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.MAGENTA}{view.answer1}, {view.answer2}, {view.answer3}{Style.RESET_ALL} {Fore.CYAN}by {ctx.author}")
        
        
        
        await view2.wait()
        print(f"{view2.artefact}, {view2.artefactreply}, {SubmitButtonView.artefact}, {SubmitButtonView.artefactreply}, {ReportModal.artefact}, {ReportModal.artefact.value}")
        print("PROGRAM STILL RUNNING 3")


     
        if view2.foo is None:
            logger.error("Timeout")
        elif view2.foo is True:
            logger.info("Someone locked the view")
        else:
            logger.error("Canceled")

        await view2.wait()
        print("PROGRAM STILL RUNNING 4")


        


async def setup(bot):
    await bot.add_cog(TestMenuCog(bot))