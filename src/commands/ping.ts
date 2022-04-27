import Command from '../interfaces/Commands'

export const ping: Command = {
  name: 'ping',
  description: 'Answers with pong',
  run: async interaction => {
    await interaction.reply('PONG')
  }
}
