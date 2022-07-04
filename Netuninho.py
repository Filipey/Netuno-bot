import discord
from discord.ext import commands as c

import netuno

intents = discord.Intents.all()
intents.members = True
intents.typing = False

bot = c.Bot(intents = intents, command_prefix="-", help_command=None)

@bot.event
async def on_ready():
  print(f"{bot.user.name} running!")
  # loading commands
  netuno.events.__init__(bot)
  netuno.commands.chat.__init__(bot)
