import os

import discord
import wavelink


def __init__(bot):
  """Initialize events"""
  join(bot)
  node_ready(bot)
  track_end(bot)

def join(bot):
  @bot.event
  async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='geral')
    prefix = os.getenv('BOT_PREFIX')
    await channel.send(f'Bem vindo ao inferno {member.mention}! Digite `{prefix}help` para mais detalhes')

async def change_status(bot):
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="conversa fiada"))

async def node_connect(bot):
  await bot.wait_until_ready()
  await wavelink.NodePool.create_node(bot=bot, host='lavalinkinc.ml', port=443, password='incognito', https=True)

def track_end(bot):
  @bot.event
  async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
      return await vc.play(track)

    try:
      next_song = vc.queue.get()
      await vc.play(next_song)
      await ctx.send(f"Now playing: {next_song.title}")
    except wavelink.errors.QueueEmpty:
      await vc.disconnect()
      await ctx.send("There is no more music to play! Im out fellas xD")

def node_ready(bot):
  @bot.event
  async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")
