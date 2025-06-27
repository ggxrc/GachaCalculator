// Interfaces - Discord Embeds - Adventure Embed
import { EmbedBuilder } from 'discord.js';
import { AdventureService, PriceCalculationResult } from '../../../domain/entities';

export function createAdventurePriceEmbed(
  service: AdventureService, 
  result: PriceCalculationResult
): EmbedBuilder {
  const embed = new EmbedBuilder()
    .setColor('#00AAFF')
    .setTitle('💰 Cálculo de Preço - Serviço de Aventura')
    .setDescription('Abaixo está o cálculo detalhado do preço para o serviço solicitado.')
    .addFields({ name: '💵 Preço Final', value: `R$ ${result.finalPrice.toFixed(2)}`, inline: false });

  // Adicionar detalhes das regiões se houver
  if (service.regions.length > 0) {
    embed.addFields({
      name: '🗺️ Regiões',
      value: service.regions.join(', '),
      inline: true
    });
  }

  // Adicionar detalhes de áreas específicas se houver
  if (service.specificAreas.length > 0) {
    embed.addFields({
      name: '📍 Áreas Específicas',
      value: service.specificAreas.join(', '),
      inline: true
    });
  }

  // Adicionar detalhes de árvores se houver
  if (service.trees.length > 0) {
    const treesText = service.trees
      .map(tree => `${tree.name} (${tree.levels} níveis)`)
      .join(', ');
    
    embed.addFields({
      name: '🌳 Árvores',
      value: treesText,
      inline: true
    });
  }

  // Adicionar detalhes de reputações se houver
  if (service.reputations.length > 0) {
    embed.addFields({
      name: '⭐ Reputações',
      value: service.reputations.join(', '),
      inline: true
    });
  }

  // Adicionar detalhes da bússola se aplicável
  if (service.hasCompass) {
    embed.addFields({
      name: '🧭 Bússola',
      value: service.compassRegion || 'Sim',
      inline: true
    });
  }

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
