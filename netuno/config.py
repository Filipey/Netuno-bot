import os


def bot_token():
  return os.getenv('BOT_TOKEN')

def client_id():
  return os.getenv('CLIENT_ID')

def bot_prefix():
  return "$"
