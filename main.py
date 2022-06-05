import asyncio
import os
from random import choice

import discord
import youtube_dl
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!')

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
  def __init__(self, source, *, data, volume=0.5):
      super().__init__(source, volume)

      self.data = data

      self.title = data.get('title')
      self.url = data.get('url')

  @classmethod
  async def from_url(cls, url, *, loop=None, stream=False):
    loop = loop or asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

    if 'entries' in data:
      # take first item from a playlist
      data = data['entries'][0]

    filename = data['url'] if stream else ytdl.prepare_filename(data)
    return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


status = ['o Netuno no esgoto', 'Dormindo', 'leaguezinho']
queue = []

@bot.event
async def on_ready():
  change_status.start()
  print(f"{bot.user.name} running!")

@tasks.loop(seconds=20000)
async def change_status():
  await bot.change_presence(activity=discord.Game(choice(status)))

@bot.event
async def on_member_join(member):
  channel = discord.utils.get(member.guild.channels, name='Geral')
  await channel.send(f'Bem vindo ao inferno {member.mention}! Digite `!help` para mais detalhes')

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
    'Paulão',
    'Djonguinha'
    'Periclão',
    'Buzzdudo',
    'Smigou'
  ]

  response = choice(quotes)
  await ctx.send(response)

@bot.command(
  name='delete',
  help='Delete the last messages'
)
async def delete_message(ctx, number_of_messages: int):
  await ctx.channel.purge(limit=number_of_messages+1)

@bot.command(
  name='join',
  help='Makes the bot join the voice channel'
)
async def join(ctx):
  if not ctx.message.author.voice:
    await ctx.send('You are not connected to a voice channel')
    return

  else:
    channel = ctx.message.author.voice.channel

  await channel.connect()

@bot.command(
  name='queue',
  help='Add a song to the queue'
)
async def queue(ctx, url: str):
  global queue

  queue.append(url)
  await ctx.send(f'{url} added to queue')

@bot.command(
  name='remove',
  help='Remove a item from the queue'
)
async def remove(ctx, index):
  global queue

  try:
    del(queue[int(index)])
    await ctx.send(f'Your queue is now {queue}')

  except:
    await ctx.send('Your queue is **empty** or the index is **out of range**')


@bot.command(
  name='play',
  help='Play a music from youtube'
)
async def play(ctx):
  global queue

  server = ctx.message.guild
  voice_channel = ctx.message.author.voice.channel

  async with ctx.typing():
    player = await YTDLSource.from_url(queue[0], loop=bot.loop)
    voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

  await ctx.send('**Now Playing:** {}'.format(player.title))
  del(queue[0])

@bot.command(
  name='leave',
  help='Leave from actual channel'
)
async def leave(ctx):
  voice_client = ctx.message.guild.voice_client
  await voice_client.disconnect()

@bot.command(
  name='pause',
  help='Pause the actual music'
)
async def pause(ctx):
  server = ctx.message.guild
  voice_channel = server.voice_client

  voice_channel.pause()

@bot.command(
  name='resume',
  help='Resume the audio'
)
async def resume(ctx):
  server = ctx.message.guild
  voice_channel = server.voice_client

  voice_channel.resume()

@bot.command(
  name='stop',
  help='Stop the actual audio and makes the bot leave'
)
async def stop(ctx):
  server = ctx.message.guild
  voice_channel = server.voice_client

  voice_channel.stop()

bot.run(TOKEN)
