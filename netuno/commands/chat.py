from random import choice

import discord
import netuno
from discord.ext import commands as cmd
from netuno.errors.standard import handle


def __init__(bot):
  leitao(bot)
  clear(bot)
  ban(bot)
  kick(bot)
  helpc(bot)


def leitao(bot):
  @bot.command()
  async def leitao(ctx):
    quotes = ctx.guild.members

    response = choice(quotes)
    await ctx.send(f"{response.mention} é um leitãozinho")

def clear(bot):
  @bot.command()
  @cmd.has_permissions(manage_messages=True)
  async def clear(ctx, number_of_messages: int):
    await ctx.channel.purge(limit=number_of_messages+1)

  @clear.error
  async def clear_error(ctx, error):
    await handle(ctx, error)


def ban(bot):
  @bot.command()
  @cmd.has_permissions(ban_members=True)
  async def ban(ctx, member: discord.Member=None, *, reason=None):

    if member is None:
      await ctx.send("Mention someone to kick")
    
    if reason is None:
      await ctx.send("Reason was not specified")

    try:
      await ctx.send(f'{member.mention} foi banido!')
      await member.ban(reason=reason)
    except discord.Forbidden as e:
      await ctx.send(f'Failed to ban {member.mention}')

  @ban.error
  async def ban_error(ctx, error):
    await handle(ctx, error)

def kick(bot):
  @bot.command()
  @cmd.has_guild_permissions(kick_members=True)
  async def kick(ctx, member: discord.Member=None, *, reason=None):

    if member is None:
      await ctx.send("Mention someone to kick")
    
    if reason is None:
      await ctx.send("Reason was not specified")

    try:
      await ctx.send(f'{member.mention} foi expulso!')
      await member.kick(reason=reason)
    except discord.Forbidden as e:
      await ctx.send(f'Failed to kick {member.mention}' + str(e))

  @kick.error
  async def kick_error(ctx, error):
    await handle(ctx, error)

def helpc(bot):
  bot.remove_command('help')
  @bot.command()
  async def help(ctx):
    await ctx.send(embed=netuno.tools.embed.new_embed())
