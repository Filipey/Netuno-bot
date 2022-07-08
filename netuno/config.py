import os

import discord


def bot_token():
  return os.getenv('BOT_TOKEN')

def client_id():
  return os.getenv('CLIENT_ID')

def bot_prefix():
  return os.getenv('BOT_PREFIX')

def is_admin(ctx, member: discord.Member):
  for role in member.roles:
    if role == 'ADM':
      return True
  return False
  
