// Utility Commands
import { SlashCommandBuilder, ChatInputCommandInteraction, EmbedBuilder } from 'discord.js';
import { PriceRepository } from '../interfaces/repositories/price-repository';
import { BOT_CONFIG } from '../config';

export class HelpCommand {
  getSlashCommand() {
    return new SlashCommandBuilder()
      .setName('help')
      .setDescription('Mostra informações sobre como usar o bot');
  }

  async execute(interaction: ChatInputCommandInteraction) {
    const embed = new EmbedBuilder()
      .setTitle('🤖 Dori - Calculadora Genshin Impact')
      .setDescription('Bot para cálculo de preços de serviços no Genshin Impact')
      .setColor(0x5865F2)
      .addFields(
        {
          name: '⚔️ /adventure',
          value: 'Calcula preços de serviços de aventura\n' +
                 '• **regioes**: mondstadt, liyue, inazuma, sumeru, fontaine, natlan\n' +
                 '• **areas**: dragonspine, despenhadeiro, vale_chenyu, etc.\n' +
                 '• **arvores**: formato "nome:níveis" (ex: sakura:10)\n' +
                 '• **reputacoes**: formato "região:níveis" (ex: mondstadt:5)\n' +
                 '• **exploracao**: percentual de 0-100\n' +
                 '• **bussola**: true/false',
          inline: false
        },
        {
          name: '🏗️ /build',
          value: 'Calcula preços de build de personagem\n' +
                 '• **personagem**: nome do personagem\n' +
                 '• **dificuldade**: 1-5\n' +
                 '• **talentos**: true/false\n' +
                 '• **arma**: true/false\n' +
                 '• **artefatos**: true/false',
          inline: false
        },
        {
          name: '📋 /precos',
          value: 'Mostra tabela de preços base',
          inline: false
        },
        {
          name: '👥 /personagens',
          value: 'Lista personagens por dificuldade',
          inline: false
        }
      )
      .setFooter({ text: 'Desenvolvido por Dori' });

    await interaction.reply({ embeds: [embed] });
  }
}

export class PricesCommand {
  private repository: PriceRepository;

  constructor() {
    this.repository = new PriceRepository();
  }

  getSlashCommand() {
    return new SlashCommandBuilder()
      .setName('precos')
      .setDescription('Mostra tabela de preços base');
  }

  async execute(interaction: ChatInputCommandInteraction) {
    const embed = new EmbedBuilder()
      .setTitle('💰 Tabela de Preços Base')
      .setColor(0xFFD700)
      .addFields(
        {
          name: '🗺️ Regiões',
          value: this.formatPricesList([
            { name: 'Mondstadt', price: 10.00 },
            { name: 'Liyue', price: 10.00 },
            { name: 'Inazuma', price: 15.00 },
            { name: 'Sumeru', price: 15.00 },
            { name: 'Fontaine', price: 20.00 },
            { name: 'Natlan', price: 25.00 }
          ]),
          inline: true
        },
        {
          name: '📍 Áreas Específicas',
          value: this.formatPricesList([
            { name: 'Dragonspine', price: 5.00 },
            { name: 'Despenhadeiro', price: 5.00 },
            { name: 'Vale Chenyu', price: 5.00 },
            { name: 'Ilha Musk', price: 3.00 },
            { name: 'Ilha Tsurumi', price: 5.00 },
            { name: 'Enkanomiya', price: 5.00 },
            { name: 'Deserto', price: 7.00 }
          ]),
          inline: true
        },
        {
          name: '🌳 Árvores',
          value: this.formatPricesList([
            { name: 'Frostbearing', price: 2.00 },
            { name: 'Sakura', price: 2.00 },
            { name: 'Lumberpunk', price: 2.00 },
            { name: 'Rainforest', price: 2.00 },
            { name: 'Desert', price: 2.00 }
          ]),
          inline: false
        },
        {
          name: '👤 Personagem Base',
          value: 'R$ 30,00',
          inline: false
        },
        {
          name: '⚔️ Dificuldade de Personagens',
          value: 'Multiplicador: x1.0 (fácil) até x2.0 (muito difícil)',
          inline: false
        }
      )
      .setFooter({ text: 'Preços sujeitos a alterações' });

    await interaction.reply({ embeds: [embed] });
  }

  private formatPricesList(items: { name: string; price: number }[]): string {
    return items.map(item => `• ${item.name}: R$ ${item.price.toFixed(2)}`).join('\n');
  }
}

export class CharactersCommand {
  private repository: PriceRepository;

  constructor() {
    this.repository = new PriceRepository();
  }

  getSlashCommand() {
    return new SlashCommandBuilder()
      .setName('personagens')
      .setDescription('Lista personagens por dificuldade');
  }

  async execute(interaction: ChatInputCommandInteraction) {
    const characters = {
      easy: [
        'Amber', 'Barbara', 'Bennett', 'Diona', 'Fischl', 'Kaeya', 'Lisa',
        'Noelle', 'Rosaria', 'Sucrose', 'Xiangling'
      ],
      medium: [
        'Albedo', 'Aloy', 'Beidou', 'Chongyun', 'Collei', 'Diluc', 'Eula',
        'Ganyu', 'Gorou', 'Jean', 'Klee', 'Kokomi', 'Layla', 'Mona',
        'Ningguang', 'Qiqi', 'Razor', 'Shenhe', 'Thoma', 'Tighnari',
        'Traveler', 'Venti', 'Xingqiu', 'Xinyan', 'Yanfei', 'Yelan',
        'Yoimiya', 'Yun Jin', 'Zhongli'
      ],
      hard: [
        'Ayaka', 'Ayato', 'Cyno', 'Heizou', 'Hu Tao', 'Itto', 'Kazuha',
        'Keqing', 'Nahida', 'Nilou', 'Raiden', 'Sara', 'Sayu', 'Shinobu',
        'Tartaglia', 'Wanderer', 'Xiao', 'Yae Miko'
      ]
    };

    const embed = new EmbedBuilder()
      .setTitle('👥 Personagens por Dificuldade')
      .setColor(0x9B59B6)
      .addFields(
        {
          name: '😌 Fácil (x1.0)',
          value: characters.easy.join(', '),
          inline: false
        },
        {
          name: '😐 Médio (x1.5)',
          value: characters.medium.join(', '),
          inline: false
        },
        {
          name: '😫 Difícil (x2.0)',
          value: characters.hard.join(', '),
          inline: false
        }
      )
      .setFooter({ text: 'Classificação baseada na complexidade de rotação/build' });

    await interaction.reply({ embeds: [embed] });
  }
}
