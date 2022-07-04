from random import choice

import discord
from discord.ext import tasks


def __init__(bot):
  """Initialize events"""
  join(bot)
  # ready(bot)


def join(bot):
  @bot.event
  async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='Geral')
    await channel.send(f'Bem vindo ao inferno {member.mention}! Digite `!help` para mais detalhes')

# def ready(bot):
#   @bot.event
#   async def on_ready():
#     change_status.start()
#     print(f"{bot.user.name} running!")

#   @tasks.loop(seconds=20000)
#   async def change_status():
#     status = ['o Netuno no esgoto', 'Dormindo', 'leaguezinho']
#     await bot.change_presence(activity=discord.Game(choice(status)))

  


