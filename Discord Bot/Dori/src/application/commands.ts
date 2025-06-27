// Application - Discord Commands
import { SlashCommandBuilder, ChatInputCommandInteraction, EmbedBuilder } from 'discord.js';
import { AdventurePriceCalculator } from './use-cases/adventure-price-calculator';
import { BuildPriceCalculator } from './use-cases/build-price-calculator';
import { PriceRepository } from '../domain/repositories/price-repository';
import { AdventureService, BuildService, CharacterMaterials } from '../domain/entities';
import { ValidationService } from '../domain/validation';
import { container } from '../config/dependency-container';

export class AdventureCommand {
  private calculator: AdventurePriceCalculator;
  private validationService: ValidationService;

  constructor(
    calculator: AdventurePriceCalculator = container.adventurePriceCalculator,
    validationService: ValidationService = container.validationService
  ) {
    this.calculator = calculator;
    this.validationService = validationService;
  }

  getSlashCommand() {
    return new SlashCommandBuilder()
      .setName('adventure')
      .setDescription('Calcula o preço de serviços de aventura')
      .addStringOption(option =>
        option.setName('regioes')
          .setDescription('Regiões separadas por vírgula (mondstadt, liyue, inazuma, sumeru, fontaine, natlan)')
          .setRequired(false))
      .addStringOption(option =>
        option.setName('areas')
          .setDescription('Áreas específicas separadas por vírgula')
          .setRequired(false))
      .addStringOption(option =>
        option.setName('arvores')
          .setDescription('Árvores no formato "nome:níveis" separadas por vírgula')
          .setRequired(false))
      .addStringOption(option =>
        option.setName('reputacoes')
          .setDescription('Reputações no formato "região:níveis" separadas por vírgula')
          .setRequired(false))
      .addNumberOption(option =>
        option.setName('exploracao')
          .setDescription('Percentual de exploração (0-100)')
          .setRequired(false))
      .addBooleanOption(option =>
        option.setName('bussola')
          .setDescription('Possui bússola?')
          .setRequired(false))
      .addStringOption(option =>
        option.setName('regiao_bussola')
          .setDescription('Região da bússola')
          .setRequired(false));
  }

  async execute(interaction: ChatInputCommandInteraction) {
    try {
      const regions = interaction.options.getString('regioes')?.split(',').map(r => r.trim()) || [];
      const areas = interaction.options.getString('areas')?.split(',').map(a => a.trim()) || [];
      const explorationPercentage = interaction.options.getNumber('exploracao') || 0;
      const hasCompass = interaction.options.getBoolean('bussola') || false;
      const compassRegion = interaction.options.getString('regiao_bussola');

      // Parse trees
      const trees: { name: string; levels: number }[] = [];
      const treesInput = interaction.options.getString('arvores');
      if (treesInput) {
        treesInput.split(',').forEach(tree => {
          const [name, levels] = tree.trim().split(':');
          if (name && levels) {
            trees.push({ name: name.trim(), levels: parseInt(levels) });
          }
        });
      }

      // Parse reputations
      const reputations: { region: string; levels: number }[] = [];
      const repsInput = interaction.options.getString('reputacoes');
      if (repsInput) {
        repsInput.split(',').forEach(rep => {
          const [region, levels] = rep.trim().split(':');
          if (region && levels) {
            reputations.push({ region: region.trim(), levels: parseInt(levels) });
          }
        });
      }

      const service: AdventureService = {
        regions,
        specificAreas: areas,
        trees,
        reputations,
        explorationPercentage,
        hasCompass,
        compassRegion: compassRegion || undefined
      };

      const result = this.calculator.calculatePrice(service);

      const embed = new EmbedBuilder()
        .setTitle('💰 Cálculo de Preço - Serviços de Aventura')
        .setColor('#0099ff') // Substitua por BOT_CONFIG.COLORS.ADVENTURE se necessário
        .addFields(
          { name: 'Preço Base', value: `R$ ${result.basePrice.toFixed(2)}`, inline: true },
          { name: 'Preço Final', value: `R$ ${result.finalPrice.toFixed(2)}`, inline: true },
          { name: 'Economia', value: `R$ ${(result.basePrice - result.finalPrice).toFixed(2)}`, inline: true }
        );

      if (result.breakdown.length > 0) {
        embed.addFields({ name: 'Detalhamento', value: result.breakdown.join('\n'), inline: false });
      }

      if (result.discounts.length > 0) {
        const discountText = result.discounts.map(d => 
          `${d.type}: -${d.percentage.toFixed(1)}% (R$ ${d.amount.toFixed(2)})`
        ).join('\n');
        embed.addFields({ name: 'Descontos Aplicados', value: discountText, inline: false });
      }

      await interaction.reply({ embeds: [embed] });
    } catch (error) {
      console.error('Erro no comando adventure:', error);
      await interaction.reply({ content: 'Erro ao calcular o preço. Verifique os parâmetros.', ephemeral: true });
    }
  }
}

export class BuildCommand {
  private calculator: BuildPriceCalculator;
  private priceRepository: PriceRepository;
  private validationService: ValidationService;

  constructor(
    calculator: BuildPriceCalculator = container.buildPriceCalculator,
    priceRepository: PriceRepository = container.priceRepository as PriceRepository,
    validationService: ValidationService = container.validationService
  ) {
    this.calculator = calculator;
    this.priceRepository = priceRepository;
    this.validationService = validationService;
  }

  getSlashCommand() {
    return new SlashCommandBuilder()
      .setName('build')
      .setDescription('Calcula o preço de build de personagem')
      .addStringOption(option =>
        option.setName('personagem')
          .setDescription('Nome do personagem')
          .setRequired(true))
      .addIntegerOption(option =>
        option.setName('cinza')
          .setDescription('Quantidade de itens de drop cinza coletados')
          .setRequired(false))
      .addIntegerOption(option =>
        option.setName('verde')
          .setDescription('Quantidade de itens de drop verde coletados')
          .setRequired(false))
      .addIntegerOption(option =>
        option.setName('raro')
          .setDescription('Quantidade de itens de drop raro coletados')
          .setRequired(false))
      .addIntegerOption(option =>
        option.setName('boss')
          .setDescription('Quantidade de itens de boss coletados')
          .setRequired(false))
      .addIntegerOption(option =>
        option.setName('azul')
          .setDescription('Quantidade de pedras elementais azuis coletadas')
          .setRequired(false))
      .addIntegerOption(option =>
        option.setName('roxa')
          .setDescription('Quantidade de pedras elementais roxas coletadas')
          .setRequired(false))
      .addIntegerOption(option =>
        option.setName('dourada')
          .setDescription('Quantidade de pedras elementais douradas coletadas')
          .setRequired(false))
      .addIntegerOption(option =>
        option.setName('coleta')
          .setDescription('Quantidade de itens de coleta coletados')
          .setRequired(false));
  }

  async execute(interaction: ChatInputCommandInteraction) {
    try {
      const character = interaction.options.getString('personagem', true);
      const rawDifficulty = this.priceRepository.getCharacterDifficulty(character);
      const difficulty = this.validationService.validateDifficulty(rawDifficulty);

      const materials: CharacterMaterials = {
        dropItems: {
          gray: interaction.options.getInteger('cinza') || 0,
          green: interaction.options.getInteger('verde') || 0,
          rare: interaction.options.getInteger('raro') || 0
        },
        bossItems: interaction.options.getInteger('boss') || 0,
        elementalStones: {
          blue: interaction.options.getInteger('azul') || 0,
          purple: interaction.options.getInteger('roxa') || 0,
          golden: interaction.options.getInteger('dourada') || 0
        },
        collectItems: interaction.options.getInteger('coleta') || 0
      };

      const service: BuildService = {
        character,
        difficulty,
        materials: materials
      };

      const result = this.calculator.calculatePrice(service);

      const embed = new EmbedBuilder()
        .setTitle(`⚔️ Cálculo de Preço - Build ${character}`)
        .setColor('#ff9900') // Substitua por BOT_CONFIG.COLORS.BUILD se necessário
        .addFields(
          { name: 'Personagem', value: character, inline: true },
          { name: 'Dificuldade', value: difficulty.toString(), inline: true },
          { name: 'Preço Final', value: `R$ ${result.finalPrice.toFixed(2)}`, inline: true }
        );

      if (result.breakdown.length > 0) {
        embed.addFields({ name: 'Detalhamento', value: result.breakdown.join('\n'), inline: false });
      }

      if (result.discounts.length > 0) {
        const discountText = result.discounts.map(d => 
          `${d.type}: -${d.percentage.toFixed(1)}% (R$ ${d.amount.toFixed(2)})`
        ).join('\n');
        embed.addFields({ name: 'Descontos Aplicados', value: discountText, inline: false });
      }

      await interaction.reply({ embeds: [embed] });
    } catch (error) {
      console.error('Erro no comando build:', error);
      await interaction.reply({ content: 'Erro ao calcular o preço. Verifique os parâmetros.', ephemeral: true });
    }
  }
}
