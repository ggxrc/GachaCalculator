// Interfaces - Discord Commands - Adventure Command
import { SlashCommandBuilder, ChatInputCommandInteraction } from 'discord.js';
import { AdventurePriceCalculator } from '../../../application/use-cases/adventure-price-calculator';
import { PriceRepository } from '../../repositories/price-repository';
import { AdventureService } from '../../../domain/entities';
import { ValidationService } from '../../../domain/validation';
import { createAdventurePriceEmbed } from '../embeds';

export class AdventureCommand {
  private calculator: AdventurePriceCalculator;
  private validationService: ValidationService;

  constructor() {
    const priceRepository = new PriceRepository();
    this.calculator = new AdventurePriceCalculator(priceRepository);
    this.validationService = new ValidationService();
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
          .setDescription('Regiões com reputação separadas por vírgula')
          .setRequired(false))
      .addBooleanOption(option =>
        option.setName('bussola')
          .setDescription('Possui bússola? (true/false)')
          .setRequired(false));
  }

  async execute(interaction: ChatInputCommandInteraction) {
    const regions = this.validationService.parseCommaSeparatedString(
      interaction.options.getString('regioes') || ''
    );
    const areas = this.validationService.parseCommaSeparatedString(
      interaction.options.getString('areas') || ''
    );
    const treeInput = this.validationService.parseCommaSeparatedString(
      interaction.options.getString('arvores') || ''
    );
    const reputations = this.validationService.parseCommaSeparatedString(
      interaction.options.getString('reputacoes') || ''
    );
    const hasCompass = interaction.options.getBoolean('bussola') || false;

    // Parse tree input (format: "tree:levels")
    const trees: { name: string; levels: number }[] = [];
    treeInput.forEach(treeInfo => {
      const [name, levelsStr] = treeInfo.split(':');
      if (name && levelsStr) {
        const levels = parseInt(levelsStr);
        if (!isNaN(levels) && levels > 0) {
          trees.push({ name, levels });
        }
      }
    });

    const service: AdventureService = {
      regions,
      specificAreas: areas,
      trees,
      reputations: reputations.map(region => ({ region, levels: 1 })),
      explorationPercentage: 100,
      hasCompass
    };

    try {
      const result = this.calculator.calculatePrice(service);
      const embed = createAdventurePriceEmbed(service, result);
      await interaction.reply({ embeds: [embed] });
    } catch (error: any) {
      await interaction.reply({ 
        content: `Erro ao calcular preço: ${error.message}`, 
        ephemeral: true 
      });
    }
  }
}
