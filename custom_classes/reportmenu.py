from discord.ext import commands
import discord

from settings import D_REPORT_CHAN_ID
import settings
import pathlib
import random

import datetime
from colorama import Fore, Back, Style

logger = settings.logging.getLogger("bot")


def get_random_header():
    embed_headers = pathlib.Path(settings.BASE_DIR / "img" / "reportembed").glob("**/*")
    return random.choice(list(embed_headers))


class ReportModal(discord.ui.Modal, title="Sup, what you've been up to?"):
    description = discord.ui.TextInput(
        style=discord.TextStyle.long,
        max_length=690,
        label="Description",
        required=True,
        placeholder="Describe what you did here...",
    )
    artefact = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Artefact",
        required=True,
        placeholder="Paste a URL relevant to your contribution here...",
    )

    async def on_submit(self, interaction: discord.Interaction):

        description_output = self.description
        artefact_output = self.artefact
        guild = PersistentView.guild

        try:
            await interaction.response.defer()
            await PersistentView.modalcallback(
                self, interaction, description_output, artefact_output, guild
            )

            print(
                f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.CYAN}{Fore.BLACK}user submitted a modal successfully"
            )
            print(
                f"{Style.BRIGHT}{Back.MAGENTA}{Fore.BLACK}DATA PASSED:{Style.RESET_ALL}\
        {Style.BRIGHT}{Back.BLACK}{Fore.MAGENTA}{description_output}, {artefact_output} | {Style.RESET_ALL} {Fore.CYAN}by {interaction.user}"
            )

            self.stop()

        except Exception as e:
            print(e)
            logger.exception("An exception occurred")

    async def on_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(
            "Something went wrong. Modal NOT submitted."
        )
        print(
            f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}ERROR:{Style.RESET_ALL}\
            {Style.BRIGHT}{Back.BLACK}{Fore.RED}failed to submit modal."
        )


class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    guild = None
    effort = None
    impact = None
    desc = None
    art = None

    @discord.ui.button(
        label="add description",
        style=discord.ButtonStyle.blurple,
        emoji="➕",
        custom_id="report_view:modal_button",
        row=4,
    )
    async def button2callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        button.style = discord.ButtonStyle.green
        report_modal = ReportModal(timeout=None)
        report_modal.user = interaction.user

        await interaction.response.send_modal(report_modal)
        print(
            f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}PASSED:{Style.RESET_ALL}\
            {Style.BRIGHT}{Back.BLACK}{Fore.GREEN}modal sent successfully"
        )

        await report_modal.wait()
        self.desc = report_modal.description
        self.art = report_modal.artefact
        print(
            f"button2 callback(report modal button): {report_modal.description}, {report_modal.artefact}, {self.guild}, {self.effort}, {self.impact}"
        )

        reportembed = discord.Embed(
            colour=discord.Colour.magenta(),
            description=(
                f"On the battlefield, a strange schorched document is seen\
        pinned on a spear, begging to be torn...It reads:"
            ),
            title="has slain an enemy!",
            timestamp=datetime.datetime.now(),
            # time=datetime.datetime.utcnow().strftime("%Y-%d-%m %H:%M:%S %Z")
        )
        guild = str(self.guild)[1:-1]
        effort = str(self.effort)[1:-1]
        impact = str(self.impact)[1:-1]
        cguild = str(guild)[1:-1]
        ceffort = str(effort)[1:-1]
        cimpact = str(impact)[1:-1]

        random_header_path = get_random_header()
        random_header_image = discord.File(
            random_header_path, filename=random_header_path.name
        )

        reportembed.set_footer(text="Scorched document found")
        reportembed.set_author(name="A PLAYER")

        reportembed.set_image(url=(f"attachment://{random_header_path.name}"))
        reportembed.insert_field_at(0, name="GUILD BANNER", value=cguild, inline=True)
        reportembed.insert_field_at(
            0, name="EFFORT INVESTED", value=ceffort, inline=True
        )
        reportembed.insert_field_at(
            0, name="PROJECTED IMPACT", value=cimpact, inline=True
        )
        reportembed.insert_field_at(
            3,
            name="",
            value=(
                f"[...]\n`..{report_modal.description}`\
            \n**{interaction.user.name}**, Bane of Sugar Plums"
            ),
        )
        reportembed.insert_field_at(
            4, name="Artefact", value=f"{report_modal.artefact}", inline=False
        )
        await interaction.followup.send(
            (
                f"This is a preview of the report you're about to submit.\
        \n**Please click** `🔺SUBMIT REPORT` **if happy**"
            ),
            file=random_header_image,
            embed=reportembed,
            ephemeral=True,
        )

    @discord.ui.button(
        label="Submit Report",
        style=discord.ButtonStyle.gray,
        emoji="🔺",
        custom_id="report_view:submit_button",
        row=4,
    )
    async def button1callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        button.style = (discord.ButtonStyle.green,)
        button.label = "submit report"

        reportembed = discord.Embed(
            colour=discord.Colour.magenta(),
            description=(
                f"On the battlefield, a strange schorched document is seen\
        pinned on a spear, begging to be torn...It reads:"
            ),
            title="has slain an enemy!",
            timestamp=datetime.datetime.now(),
            # time=datetime.datetime.utcnow().strftime("%Y-%d-%m %H:%M:%S %Z")
        )
        guild = str(self.guild)[1:-1]
        effort = str(self.effort)[1:-1]
        impact = str(self.impact)[1:-1]
        cguild = str(guild)[1:-1]
        ceffort = str(effort)[1:-1]
        cimpact = str(impact)[1:-1]

        random_header_path = get_random_header()
        random_header_image = discord.File(
            random_header_path, filename=random_header_path.name
        )
        # reportembed = discord.Embed()
        reportembed.set_footer(text="Scorched document found")
        reportembed.set_author(name="A PLAYER")

        reportembed.set_image(url=(f"attachment://{random_header_path.name}"))
        reportembed.insert_field_at(0, name="GUILD BANNER", value=cguild, inline=True)
        reportembed.insert_field_at(
            0, name="EFFORT INVESTED", value=ceffort, inline=True
        )
        reportembed.insert_field_at(
            0, name="PROJECTED IMPACT", value=cimpact, inline=True
        )
        reportembed.insert_field_at(
            3,
            name="",
            value=(
                f"[...]\n`..{self.desc}`\
            \n**{interaction.user.name}**, Bane of Sugar Plums"
            ),
        )
        reportembed.insert_field_at(
            4, name="Artefact", value=f"{self.art}", inline=False
        )

        channel = interaction.guild.get_channel(D_REPORT_CHAN_ID)
        await channel.send(
            f"{interaction.user.mention} found a scorched document!",
            file=random_header_image,
            embed=reportembed,
        )
        await interaction.response.send_message(
            (f"Check {channel.mention}\nYour report has been submitted. Salute!"),
            ephemeral=True,
        )

    @discord.ui.select(
        options=[
            discord.SelectOption(
                value="Art and Design",
                label="Art and Design",
                emoji="🎨",
                description="Guilds focused on artistry and design frameworks",
            ),
            discord.SelectOption(
                value="Building",
                label="Building",
                emoji="🛠️",
                description="Guild focused on building MetaGame's infrastructure",
            ),
            discord.SelectOption(
                value="BridgeBuilding",
                label="BridgeBuilding",
                emoji="🌉",
                description="Guild focused on building external relationships",
            ),
            discord.SelectOption(
                value="Innkeeping",
                label="Innkeeping",
                emoji="🍻",
                description="Guild focused on community building",
            ),
            discord.SelectOption(
                value="Shilling and Rainmaking",
                label="Shilling and Rainmaking",
                emoji="📣",
                description="Guild focused on marketing and funding",
            ),
        ],
        placeholder="Pick a Guild",
        row=0,
        custom_id="report_view:select_option.guild",
    )
    async def customcallback2(self, interaction, select_item: discord.ui.Select):
        self.guild = select_item.values
        await interaction.response.defer()

    @discord.ui.select(
        options=[
            discord.SelectOption(
                value="Extreme Effort",
                label="Extreme Effort",
                emoji="🐙",
                description="30+ days. Blood, sweat and tears. What is reality?",
            ),
            discord.SelectOption(
                value="High Effort",
                label="High Effort",
                emoji="🟠",
                description="14+ days. Spent a lot of time and effort.",
            ),
            discord.SelectOption(
                value="Medium-High Effort",
                label="Medium-High Effort",
                emoji="🟡",
                description="7+ days. It took some time.",
            ),
            discord.SelectOption(
                value="Medium Effort",
                label="Medium Effort",
                emoji="🟢",
                description="Less than a day. Decent.",
            ),
            discord.SelectOption(
                value="Low Effort",
                label="Low Effort",
                emoji="⚪",
                description="Less than an hour, thinking included.",
            ),
        ],
        placeholder="Effort invested",
        row=1,
        custom_id="report_view:select_option.effort",
    )
    async def customcallback3(
        self, interaction: discord.Interaction, select_item: discord.ui.Select
    ):
        self.effort = select_item.values
        await interaction.response.defer()

    @discord.ui.select(
        options=[
            discord.SelectOption(
                label="Extreme Impact",
                emoji="☣️",
                description="Extreme Impact. The world as we know it is gone.",
            ),
            discord.SelectOption(
                label="High Impact",
                emoji="3️⃣",
                description="High impact. Will ruffle some feathers.",
            ),
            discord.SelectOption(
                label="Medium Impact",
                emoji="2️⃣",
                description="Medium impact. Decent contribution. ",
            ),
            discord.SelectOption(
                label="Low Impact",
                emoji="1️⃣",
                description="Low impact. Simple contribution. EZ",
            ),
        ],
        placeholder="Projected Impact",
        row=2,
        custom_id="report_view:select_option.impact",
    )
    async def customcallback4(
        self, interaction: discord.Interaction, select_item: discord.ui.Select
    ):
        self.impact = select_item.values
        await interaction.response.defer()

    async def modalcallback(
        self,
        interaction: discord.Interaction,
        description_output,
        artefact_output,
        guild,
    ):

        self.descriptionreply = description_output
        self.artefactreply = artefact_output
        self.guild = guild

        logger.info(
            f"User {interaction.user.name} is submitting description: {self.descriptionreply} and artefact: {self.artefactreply}. Extra: {self.guild}"
        )
        # await interaction.response.defer()
        logger.info("Submission process completed.")


class ReportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(ReportCog(bot))
