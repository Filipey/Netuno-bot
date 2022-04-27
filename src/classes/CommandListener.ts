import Command from '../interfaces/Commands'
import Bot from './Bot'

class CommandListener {
  constructor(private command: Command[]) {
    if (!Bot.client) return
    Bot.client.on('interactionCreate', async interaction => {
      if (!interaction.isCommand()) return

      this.command.forEach(command => {
        if (interaction.commandName === command.name) {
          command.run(interaction)
        }
      })
    })
  }
}

export default CommandListener
