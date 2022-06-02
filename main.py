import os
import random
from unicodedata import name

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
  print(f"{bot.user.name} running!")

@bot.command(
  name="leitao",
  help="Responds with a random leitao of Netuno"
  )
async def leitao(ctx):
  quotes = [
    'Tulhão',
    'Necas',
    'Cojas',
    'Lombras',
    'Hiku',
    'Pk',
    'Adm',
    'Didico',
    'Periclão',
    'Buzzdudo',
    'Smigou'
  ]

  response = random.choice(quotes)
  await ctx.send(response)

@bot.command(
  name='delete',
  help='Delete the last messages'
)
async def delete_message(ctx, number_of_messages: int):
  await ctx.channel.purge(limit=number_of_messages+1)

bot.run(TOKEN)
