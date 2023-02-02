from discord.ext import commands


@commands.group()
async def math(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple math")


@math.command()
async def add(ctx, x: int, y: int):
    await ctx.send(x + y)


@math.command()
async def sub(ctx, x: int, y: int):
    await ctx.send(x - y)


@math.command()
async def mul(ctx, x: int, y: int):
    await ctx.send(x * y)


@math.command()
async def div(ctx, x: int, y: int):
    await ctx.send(x / y)


@math.command()
async def pct(ctx, x: int, y: int):
    await ctx.send(f"`{x} is {x/y*100}% of {y}`")


async def setup(bot):
    bot.add_command(math)
