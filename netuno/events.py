import discord


def __init__(bot):
  """Initialize events"""
  join(bot) 


def join(bot):
  @bot.event
  async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='Geral')
    await channel.send(f'Bem vindo ao inferno {member.mention}! Digite `$help` para mais detalhes')
