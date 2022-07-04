from random import choice


def __init__(bot):
  leitao(bot)
  delete_message(bot)


def leitao(bot):
  @bot.command()
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

def delete_message(bot):
  @bot.command()
  async def delete(ctx, number_of_messages: int):
    await ctx.channel.purge(limit=number_of_messages+1)
