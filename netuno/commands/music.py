import datetime
import random

import discord
import wavelink
from discord.ext import commands as cmd


def __init__(bot):
  play(bot)
  pause(bot)
  resume(bot)
  stop(bot)
  disconnect(bot)
  queue(bot)
  loop(bot)
  volume(bot)
  now_playing(bot)
  # shuffle(bot) # NOT USABLE
  skip(bot)
  remove(bot)
  clear(bot)


def play(bot):
  @bot.command()
  async def play(ctx: cmd.Context, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
      vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"Hey, {ctx.message.author.mention}You are not connected to a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and not vc.is_playing():
      await vc.play(search)
      await ctx.send(f"Now playing {search.title}!")
    else:
      await vc.queue.put_wait(search)
      await ctx.send(f"Added {search.title} to the queue")
    vc.ctx = ctx
    setattr(vc, "loop", False)    

def pause(bot):
  @bot.command()
  async def pause(ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.pause()
    await ctx.send(f"Music paused by {ctx.message.author.mention}")

def resume(bot):
  @bot.command()
  async def resume(ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.resume()
    await ctx.send(f"Music is back! by {ctx.message.author.mention}")

def stop(bot):
  @bot.command()
  async def stop(ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    await ctx.send(f"{ctx.message.author.mention} stopped the music.")

def disconnect(bot):
  @bot.command()
  async def disconnect(ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.disconnect()
    await ctx.send(f"{ctx.message.author.mention} send me out :(")

def loop(bot):
  @bot.command()
  async def loop(ctx: cmd.Context):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    try:
      vc.loop ^= True
    except Exception:
      setattr(vc, "loop", False)

    if vc.loop:
      return await ctx.send("Loop is now Enabled!")
    else:
      return await ctx.send("Loop is now Disabled!")

def queue(bot):
  @bot.command()
  async def queue(ctx: cmd.Context):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, im not connected to a voice channel")   
    elif not ctx.author.voice:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty:
      return await ctx.send("Queue is empty!")

    em = discord.Embed(color=0x1A2382, title="Queue")
    copy = vc.queue.copy()
    count = 0
    for song in copy:
      count += 1
      em.add_field(name=f"Position {count}", value=f"`{song.title}`")

    return await ctx.send(embed=em)

def volume(bot):
  @bot.command()
  async def volume(ctx: cmd.Context, volume: int):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    if volume > 100:
      return await ctx.send("Thats to high...")
    elif volume < 0:
      return await ctx.send("Thats to low...")

    await ctx.send(f"Set the volume to {volume}%")
    return await vc.set_volume(volume=volume)

def now_playing(bot):
  @bot.command()
  async def playing(ctx: cmd.Context):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client
    
    if not vc.is_playing():
      return await ctx.send("Nothing is playing")

    em = discord.Embed(title=f"Now playing {vc.track}", description=f"Artist: {vc.track.author}")
    em.add_field(name="Duration", value=f"`{datetime.timedelta(seconds=vc.track.length)}`")
    em.add_field(name="Extra info", value=f"Song URL: [Click Me]({str(vc.track.uri)})")
    return await ctx.send(embed=em)

def shuffle(bot):
  @bot.command()
  async def shuffle(ctx: cmd.Context):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    copy = vc.queue.copy()
    random.shuffle(copy)
    vc.queue = copy
    await ctx.send(f"{ctx.message.author.mention} shuffled the queue.")

def skip(bot):
  @bot.command()
  async def skip(ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    return await ctx.send(f"{ctx.message.author.mention} skipped the actual music.")

def remove(bot):
  @bot.command()
  async def remove(ctx: cmd.Context, index: int):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    if index > len(vc.queue) or index < 1:
      return await ctx.send(f"Index must be between 1 and {len(vc.queue)}")

    removed = vc.queue.pop(index - 1)

    await ctx.send(f"{ctx.message.author.mention} removed `{removed.title}` from the queue")

def clear(bot):
  async def qclear(ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.queue.clear()
    return await ctx.send(f"{ctx.message.author.mention} cleared the queue.")
