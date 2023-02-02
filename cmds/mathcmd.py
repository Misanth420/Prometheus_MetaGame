from discord.ext import commands


@commands.group()
async def math(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple math")


@math.command()
async def add(ctx, one: int, two: int):
    await ctx.send(one + two)


@math.command()
async def sub(ctx, one: int, two: int):
    await ctx.send(one - two)


@math.command()
async def mul(ctx, one: int, two: int):
    await ctx.send(one * two)


@math.command()
async def mul(ctx, one: int, two: int):
    await ctx.send(one / two)


async def setup(bot):
    bot.add_command(math)
