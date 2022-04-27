import { Client, Intents } from 'discord.js'

const intents = [Intents.FLAGS.GUILDS, Intents.FLAGS.DIRECT_MESSAGES]

class Bot {
  public static client: Client

  constructor(private token: string) {
    Bot.client = new Client({ intents })
    Bot.client.on('ready', () => {
      if (Bot.client.user) {
        console.log(`The bot is working as ${Bot.client.user.tag}`)
      }
    })
  }
  start() {
    Bot.client.login(this.token)
  }
}

export default Bot
