// Interfaces - Discord Embeds - Build Embed
import { EmbedBuilder } from 'discord.js';
import { BuildService, PriceCalculationResult } from '../../../domain/entities';

export function createBuildPriceEmbed(
  service: BuildService, 
  result: PriceCalculationResult
): EmbedBuilder {
  const embed = new EmbedBuilder()
    .setColor('#FF6B6B')
    .setTitle('💰 Cálculo de Preço - Construção de Personagem')
    .setDescription(`Cálculo de preço para construção do personagem **${service.character}**`)
    .addFields({ name: '💵 Preço Final', value: `R$ ${result.finalPrice.toFixed(2)}`, inline: false });

  // Adicionar detalhes do personagem
  embed.addFields({
    name: '👤 Personagem',
    value: service.character,
    inline: true
  });

  // Adicionar detalhes de dificuldade
  embed.addFields({
    name: '⚔️ Dificuldade',
    value: `${service.difficulty}/5`,
    inline: true
  });

  // Adicionar detalhes dos materiais incluídos
  const materialsIncluded: string[] = [];
  if (service.materials.talents) materialsIncluded.push('Talentos');
  if (service.materials.weapon) materialsIncluded.push('Arma');
  if (service.materials.artifacts) materialsIncluded.push('Artefatos');

  embed.addFields({
    name: '📦 Materiais Incluídos',
    value: materialsIncluded.length > 0 ? materialsIncluded.join(', ') : 'Nenhum material adicional',
    inline: false
  });

  // Adicionar detalhes do cálculo
  const breakdownText = result.breakdown.join('\n');
  embed.addFields({
    name: '📊 Detalhes do Cálculo',
    value: breakdownText || 'Nenhum detalhe disponível',
    inline: false
  });

  // Adicionar descontos aplicados se houver
  if (result.discounts && result.discounts.length > 0) {
    const discountsText = result.discounts
      .map(d => `${d.type}: -${d.percentage}% (R$ ${d.amount.toFixed(2)})`)
      .join('\n');
    
    embed.addFields({
      name: '💹 Descontos Aplicados',
      value: discountsText,
      inline: false
    });
  }
  
  embed.setFooter({ text: 'Calculado por Dori • Preços sujeitos a alterações' });
  embed.setTimestamp();

  return embed;
}
