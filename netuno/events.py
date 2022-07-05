import os

import discord


def __init__(bot):
  """Initialize events"""
  join(bot)


def join(bot):
  @bot.event
  async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='geral')
    prefix = os.getenv('BOT_PREFIX')
    await channel.send(f'Bem vindo ao inferno {member.mention}! Digite `{prefix}help` para mais detalhes')

async def change_status(bot):
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="conversa fiada"))
