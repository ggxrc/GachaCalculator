// Application - Adventure Price Calculator
import { AdventureService, PriceCalculationResult } from '../../domain/entities';
import { IAdventurePriceCalculator } from './interfaces';
import { IPriceRepository } from '../../domain/repositories/price-repository.interface';
import { EXPLORATION_DISCOUNT_RATE, MAX_EXPLORATION_DISCOUNT } from '../../domain/constants';

export class AdventurePriceCalculator implements IAdventurePriceCalculator {
  constructor(private priceRepository: IPriceRepository) {}

  calculatePrice(service: AdventureService): PriceCalculationResult {
    let totalBasePrice = 0;
    const discounts: { type: string; amount: number; percentage: number }[] = [];
    const breakdown: string[] = [];

    // Calcular preço base das regiões
    for (const region of service.regions) {
      const regionPrice = this.priceRepository.getRegionPrice(region);
      totalBasePrice += regionPrice;
      breakdown.push(`Região ${region}: R$ ${regionPrice.toFixed(2)}`);
    }

    // Calcular preço das áreas específicas
    for (const area of service.specificAreas) {
      const areaPrice = this.priceRepository.getSpecificAreaPrice(area);
      totalBasePrice += areaPrice;
      breakdown.push(`Área ${area}: R$ ${areaPrice.toFixed(2)}`);
    }

    // Calcular preço das árvores
    for (const tree of service.trees) {
      const treePrice = this.priceRepository.getTreePrice(tree.name);
      const treeTotalPrice = treePrice * tree.levels;
      totalBasePrice += treeTotalPrice;
      breakdown.push(`Árvore ${tree.name} (${tree.levels} níveis): R$ ${treeTotalPrice.toFixed(2)}`);
    }

    // Calcular preço das reputações
    for (const reputation of service.reputations) {
      const repPrice = this.priceRepository.getReputationPrice(reputation.region);
      const repTotalPrice = repPrice * reputation.levels;
      totalBasePrice += repTotalPrice;
      breakdown.push(`Reputação ${reputation.region} (${reputation.levels} níveis): R$ ${repTotalPrice.toFixed(2)}`);
    }

    let finalPrice = totalBasePrice;

    // Aplicar desconto da bússola
    if (service.hasCompass && service.compassRegion) {
      const compassDiscount = this.priceRepository.getCompassDiscount(service.compassRegion);
      const discountAmount = finalPrice * (compassDiscount / 100);
      discounts.push({
        type: `Bússola ${service.compassRegion}`,
        amount: discountAmount,
        percentage: compassDiscount
      });
      finalPrice -= discountAmount;
    }

    // Aplicar desconto de exploração
    if (service.explorationPercentage > 0) {
      const explorationDiscount = Math.min(service.explorationPercentage * EXPLORATION_DISCOUNT_RATE, MAX_EXPLORATION_DISCOUNT);
      const discountAmount = finalPrice * (explorationDiscount / 100);
      discounts.push({
        type: 'Exploração',
        amount: discountAmount,
        percentage: explorationDiscount
      });
      finalPrice -= discountAmount;
    }

    return {
      basePrice: totalBasePrice,
      discounts,
      finalPrice,
      breakdown
    };
  }
}
