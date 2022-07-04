import discord
from discord.ext import commands as c
from dotenv import load_dotenv

import netuno

load_dotenv()
intents = discord.Intents.all()
intents.members = True
intents.typing = False

bot = c.Bot(intents = intents, command_prefix=netuno.config.bot_prefix(), help_command=None)

@bot.event
async def on_ready():
  print(f"{bot.user.name} running!")
  # loading commands
  netuno.events.__init__(bot)
  netuno.commands.chat.__init__(bot)

bot.run(netuno.config.bot_token())
