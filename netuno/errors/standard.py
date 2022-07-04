from discord.ext import commands as cmd
from netuno.messages import permission_denied


async def handle(ctx, error):
  if isinstance(error, cmd.BadArgument):
    await ctx.send("Specify a **valid** user!")
  elif isinstance(error, cmd.MissingPermissions):
    await ctx.send(embed=permission_denied())
