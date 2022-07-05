import os


def bot_token():
  return os.getenv('BOT_TOKEN')

def client_id():
  return os.getenv('CLIENT_ID')

def bot_prefix():
  return os.getenv('BOT_PREFIX')

def is_admin(ctx):
  for role in ctx.guild.roles:
    if role.name == 'ADM':
      return True
  return False
