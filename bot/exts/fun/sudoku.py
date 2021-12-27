from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

from bot.bot import Bot

BACKGROUND = (242, 243, 244)
BLACK = 0
height = 601
width = 601
grid = Image.new(mode='RGB', size=(height, width), color=BACKGROUND)
NUM_FONT = ImageFont.truetype(r"bot/resources/fun/Roboto-Medium.ttf", 99)

draw = ImageDraw.Draw(grid)
y_start = 0
y_end = grid.height

for x in range(0, grid.width, grid.width // 6):
    line = ((x, y_start), (x, y_end))
    draw.line(line, fill=0, width=2)

for y in range(0, grid.height, grid.width // 6):
    line = ((0, y), (grid.width, y))
    draw.line(line, fill=0, width=2)

for x in range(0, grid.width, grid.width // 2):
    draw.line(((x, 0), (x, grid.height)), fill=0, width=4)

for y in range(0, grid.width, grid.width // 3):
    draw.line(((0, y), (grid.width, y)), fill=0, width=4)


class SudokuGrid(commands.Cog):
    """Generate the Sudoku grid."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.numbers: list[list]
        self.solution = None
        self.draw = draw

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

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def sudoku(self, ctx: commands.Context) -> None:
        """
        Play Sudoku with the bot!

        Sudoku is a grid game where you start with a 9x9 grid, and you are given certain numbers on the
        grid. In this version of the game, however, the grid will be a 6x6 one instead of the traditional
        9x9. All numbers on the grid, traditionally, are 1-9, and no number can repeat itself in any row,
        column, or any of the smaller 3x3 grids. In this version of the game, it would be 2x3 smaller grids
        instead of 3x3.
        """
        self.draw_num(5, self.index_to_coord((5, 5)))
        self.draw_num(1, self.index_to_coord((3, 1)))
        grid.show()


# class Sudoku(commands.Cog):
#     """Cog for the Sudoku game."""
#
#     # @commands.group()
#     # def sudoku(self):
#     #     pass
#     #
#     # @sudoku.command()
#     # def start(self):
#     #     """Start a sudoku game."""
#     #     pass
#     #
#     # @sudoku.command(aliases=["end", "finish"])
#     # def finish(self):
#     #     """End a sudoku game."""
#     #     pass
#
#     @commands.command()
#     @commands.max_concurrency(1, per=commands.BucketType.user)
#     async def sudoku(self, ctx: commands.Context) -> None:
#         """
#         Play Sudoku with the bot!
#
#         Sudoku is a grid game where you start with a 9x9 grid and you are given certain numbers on the
#         grid. In this version of the game, however, the grid will be a 6x6 one instead of the traditional 9x9.
#         All numbers on the grid, traditionally, are 1-9, and no number can repeat itself in any row, column, or any
#         of the smaller 3x3 grids. In this version of the game, it would be 2x3 smaller grids instead of 3x3.
#         """
#         pass


def setup(bot: Bot) -> None:
    """Load the Sudoku cog."""
    bot.add_cog(SudokuGrid(bot))
