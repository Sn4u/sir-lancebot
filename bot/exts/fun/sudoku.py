import datetime
from typing import Optional

import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

from bot.bot import Bot
from bot.constants import Colours

# import random

BACKGROUND = (242, 243, 244)
BLACK = 0
grid = Image.open("bot/resources/fun/sudoku_template.png")
NUM_FONT = ImageFont.truetype("bot/resources/fun/Roboto-Medium.ttf", 99)
draw = ImageDraw.Draw(grid)


class Sudoku(commands.Cog):
    """Cog for the Sudoku game."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.numbers: list[list]
        self.solution = None
        self.draw = draw
        self.running: bool = False
        self.invoker: Optional[discord.Member] = None
        self.started_at: Optional[datetime.datetime] = None
        self.difficulty: str = "Normal"  # enum class?

    @staticmethod
    def draw_num(digit: int, position: tuple[int, int]) -> None:
        """..."""
        digit = str(digit)
        if digit in "123456789" and len(digit) == 1:
            draw.text(position, str(digit), fill=BLACK, font=NUM_FONT)

    @staticmethod
    def index_to_coord(position: tuple[int, int]) -> tuple[int, int]:
        """..."""
        return position[0] * 100 + 20, position[1] * 100 - 5

    @commands.group(aliases=["s"])
    async def sudoku(self, ctx: commands.Context) -> None:
        """
        Play Sudoku with the bot!

        Sudoku is a grid game where you start with a 9x9 grid, and you are given certain numbers on the
        grid. In this version of the game, however, the grid will be a 6x6 one instead of the traditional
        9x9. All numbers on the grid, traditionally, are 1-9, and no number can repeat itself in any row,
        column, or any of the smaller 3x3 grids. In this version of the game, it would be 2x3 smaller grids
        instead of 3x3 and numbers 1-6 will be used on the grid.
        """
        if not self.running:
            await self.start(ctx)

    @sudoku.command()
    async def start(self, ctx: commands.Context) -> None:
        """Start a Sudoku game."""
        if self.running:
            await ctx.send("A Sudoku game is already running!")
            return
        self.running = True
        self.invoker = ctx.author
        self.started_at = datetime.datetime.now()
        # generate a sudoku board
        await ctx.send("Started a Sudoku game.")

    @sudoku.command(aliases=["end", "stop"])
    async def finish(self, ctx: commands.Context) -> None:
        """End a Sudoku game."""
        if self.running:
            if ctx.author == self.invoker:
                self.running = False
                await ctx.send("Ended the current game.")
            else:
                await ctx.send("Only the owner of the game can end it!")
        else:
            await ctx.send("There are no Sudoku games currently running!")

    @sudoku.command(aliases=["who", "information", "score"])
    async def info(self, ctx: commands.Context) -> None:
        """Send info about a currently running Sudoku game."""
        if not self.running:
            await ctx.send("There are no currently running games!")
            return
        now = datetime.datetime.now()
        info_embed = discord.Embed(title="Sudoku Game Information", color=Colours.grass_green)
        info_embed.add_field(name="Player", value=self.invoker.name)
        info_embed.add_field(name="Current Time", value=(now - self.started_at))
        info_embed.add_field(name="Progress", value="N/A")  # add in this variable
        info_embed.add_field(name="Difficulty", value=self.difficulty)
        info_embed.set_author(name=self.invoker.name, icon_url=self.invoker.display_avatar.url)
        await ctx.send(embed=info_embed)


def setup(bot: Bot) -> None:
    """Load the Sudoku cog."""
    bot.add_cog(Sudoku(bot))
