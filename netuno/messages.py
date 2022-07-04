import discord


def in_progress():
  """This functionality is in development!"""
  return discord.Embed(title="⏲ This feature is in development!",
                        description="You can find the last updates [here]("
                                     "https://github.com/Filipey/Netuno-bot)!", color=0x1A2382)

def permission_denied():
  """User dont have permission"""
  return discord.Embed(title="Permission denied.", description="You dont have permission to do this!",
                        color=0xFF0000)

def not_found(s):
  discord.Embed(title=f"Oops! {s.capitalize()} not found!",
                description=f"Unable to find the specified {s.lower()}!",
                color=0xFF0000)
