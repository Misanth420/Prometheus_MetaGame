import discord
from discord.ext import commands
from discord.ui import Select, View


@commands.command()
async def didathing(ctx):
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
        
    selectGuild.callback = submissionG_callback    
    selectEffort.callback = submissionE_callback
    selectImpact.callback = submissionI_callback

    view = View(timeout=None)
    view.add_item(selectGuild)
    view.add_item(selectEffort)
    view.add_item(selectImpact)

    await ctx.send("Use the fields below to create a report on your contribution.\n", view=view)

async def setup(bot):
    bot.add_command(didathing)