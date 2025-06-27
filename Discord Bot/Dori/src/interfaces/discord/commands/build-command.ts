// Interfaces - Discord Commands - Build Command
import { SlashCommandBuilder, ChatInputCommandInteraction } from 'discord.js';
import { BuildPriceCalculator } from '../../../application/use-cases/build-price-calculator';
import { PriceRepository } from '../../repositories/price-repository';
import { BuildService, CharacterMaterials } from '../../../domain/entities';
import { ValidationService } from '../../../domain/validation';
import { createBuildPriceEmbed } from '../embeds';

export class BuildCommand {
  private calculator: BuildPriceCalculator;
  private validationService: ValidationService;

  constructor() {
    const priceRepository = new PriceRepository();
    this.calculator = new BuildPriceCalculator(priceRepository);
    this.validationService = new ValidationService();
  }

  getSlashCommand() {
    return new SlashCommandBuilder()
      .setName('build')
      .setDescription('Calcula o preço de construção de personagem')
      .addStringOption(option =>
        option.setName('personagem')
          .setDescription('Nome do personagem')
          .setRequired(true))
      .addIntegerOption(option =>
        option.setName('dificuldade')
          .setDescription('Dificuldade (1-5)')
          .setRequired(false))
      .addBooleanOption(option =>
        option.setName('talentos')
          .setDescription('Inclui materiais de talentos?')
          .setRequired(false))
      .addBooleanOption(option =>
        option.setName('arma')
          .setDescription('Inclui materiais de arma?')
          .setRequired(false))
      .addBooleanOption(option =>
        option.setName('artefatos')
          .setDescription('Inclui artefatos?')
          .setRequired(false));
  }

  private validateDifficulty(value: number): 1 | 2 | 3 | 4 | 5 {
    if (value < 1) return 1;
    if (value > 5) return 5;
    return value as 1 | 2 | 3 | 4 | 5;
  }

  async execute(interaction: ChatInputCommandInteraction) {
    try {
      const character = interaction.options.getString('personagem') || '';
      const difficultyValue = interaction.options.getInteger('dificuldade') || 3;
      const difficulty = this.validateDifficulty(difficultyValue);
      const includeTalents = interaction.options.getBoolean('talentos') || false;
      const includeWeapon = interaction.options.getBoolean('arma') || false;
      const includeArtifacts = interaction.options.getBoolean('artefatos') || false;

      const materials: CharacterMaterials = {
        talents: includeTalents,
        weapon: includeWeapon,
        artifacts: includeArtifacts
      };

      const service: BuildService = {
        character,
        materials,
        difficulty
      };

      const result = this.calculator.calculatePrice(service);
      const embed = createBuildPriceEmbed(service, result);
      await interaction.reply({ embeds: [embed] });
    } catch (error: any) {
      await interaction.reply({ 
        content: `Erro ao calcular preço: ${error.message}`, 
        ephemeral: true 
      });
    }
  }
}
