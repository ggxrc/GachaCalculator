// Main Discord Bot
import { Client, GatewayIntentBits, Events, REST, Routes } from 'discord.js';
import { AdventureCommand, BuildCommand } from './interfaces/discord';
import { HelpCommand, PricesCommand, CharactersCommand } from './application/utility-commands';
import * as dotenv from 'dotenv';

dotenv.config();

class DoriBot {
  private client: Client;
  private adventureCommand: AdventureCommand;
  private buildCommand: BuildCommand;
  private helpCommand: HelpCommand;
  private pricesCommand: PricesCommand;
  private charactersCommand: CharactersCommand;

  constructor() {
    this.client = new Client({ 
      intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] 
    });
    this.adventureCommand = new AdventureCommand();
    this.buildCommand = new BuildCommand();
    this.helpCommand = new HelpCommand();
    this.pricesCommand = new PricesCommand();
    this.charactersCommand = new CharactersCommand();
  }

  async start() {
    // Register event handlers
    this.client.once(Events.ClientReady, (readyClient) => {
      console.log(`✅ Bot conectado como ${readyClient.user.tag}!`);
    });

    this.client.on(Events.InteractionCreate, async (interaction) => {
      if (!interaction.isChatInputCommand()) return;

      try {
        if (interaction.commandName === 'adventure') {
          await this.adventureCommand.execute(interaction);
        } else if (interaction.commandName === 'build') {
          await this.buildCommand.execute(interaction);
        } else if (interaction.commandName === 'help') {
          await this.helpCommand.execute(interaction);
        } else if (interaction.commandName === 'precos') {
          await this.pricesCommand.execute(interaction);
        } else if (interaction.commandName === 'personagens') {
          await this.charactersCommand.execute(interaction);
        }
      } catch (error) {
        console.error('Erro ao executar comando:', error);
        
        const reply = { 
          content: 'Houve um erro ao executar este comando!', 
          ephemeral: true 
        };
        
        if (interaction.isChatInputCommand()) {
          if (interaction.replied || interaction.deferred) {
            await interaction.followUp(reply);
          } else {
            await interaction.reply(reply);
          }
        }
      }
    });

    // Login to Discord
    await this.client.login(process.env.DISCORD_TOKEN);
  }

  async registerCommands(guildId?: string) {
    const commands = [
      this.adventureCommand.getSlashCommand().toJSON(),
      this.buildCommand.getSlashCommand().toJSON(),
      this.helpCommand.getSlashCommand().toJSON(),
      this.pricesCommand.getSlashCommand().toJSON(),
      this.charactersCommand.getSlashCommand().toJSON()
    ];

    const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN!);

    try {
      console.log('🔄 Registrando comandos slash...');

      if (guildId) {
        // Register for specific guild (faster for development)
        await rest.put(
          Routes.applicationGuildCommands(process.env.CLIENT_ID!, guildId),
          { body: commands }
        );
        console.log(`✅ Comandos registrados para o servidor ${guildId}`);
      } else {
        // Register globally (takes up to 1 hour)
        await rest.put(
          Routes.applicationCommands(process.env.CLIENT_ID!),
          { body: commands }
        );
        console.log('✅ Comandos registrados globalmente');
      }
    } catch (error) {
      console.error('❌ Erro ao registrar comandos:', error);
    }
  }

  async stop() {
    await this.client.destroy();
    console.log('🔴 Bot desconectado');
  }
}

// Start the bot
const bot = new DoriBot();

async function main() {
  try {
    await bot.start();
    
    // Register commands for a specific guild during development
    // Replace with your guild ID or remove for global registration
    // await bot.registerCommands('YOUR_GUILD_ID_HERE');
    
  } catch (error) {
    console.error('❌ Erro ao iniciar o bot:', error);
    process.exit(1);
  }
}

main().catch(console.error);

// Handle graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n🛑 Recebido SIGINT, desligando bot...');
  await bot.stop();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('\n🛑 Recebido SIGTERM, desligando bot...');
  await bot.stop();
  process.exit(0);
});

// Exportar o bot para possível importação em outros módulos
export default bot;
