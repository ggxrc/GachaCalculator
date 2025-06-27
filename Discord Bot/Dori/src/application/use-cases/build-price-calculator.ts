// Application - Build Price Calculator
import { BuildService, PriceCalculationResult, CharacterMaterials } from '../../domain/entities';
import { IBuildPriceCalculator } from './interfaces';
import { IPriceRepository } from '../../domain/repositories/price-repository.interface';
import {
  DIFFICULTY_MULTIPLIERS,
  MATERIAL_DISCOUNT_RATES,
  MAX_MATERIAL_DISCOUNT
} from '../../domain/constants';

export class BuildPriceCalculator implements IBuildPriceCalculator {
  constructor(private priceRepository: IPriceRepository) {}

  calculatePrice(service: BuildService): PriceCalculationResult {
    const basePrice = this.priceRepository.getCharacterBasePrice();
    const breakdown: string[] = [];
    const discounts: { type: string; amount: number; percentage: number }[] = [];

    // Aplicar multiplicador de dificuldade
    let finalPrice = this.applyDifficultyMultiplier(basePrice, service.difficulty);
    breakdown.push(`Preço base: R$ ${basePrice.toFixed(2)}`);
    breakdown.push(`Dificuldade ${service.difficulty}: ${this.getDifficultyMultiplierText(service.difficulty)}`);

    // Calcular desconto por materiais coletados
    const materialDiscount = this.calculateMaterialDiscount(service.materialsCollected, service.difficulty);
    
    if (materialDiscount > 0) {
      const discountAmount = finalPrice * (materialDiscount / 100);
      discounts.push({
        type: 'Materiais coletados',
        amount: discountAmount,
        percentage: materialDiscount
      });
      finalPrice -= discountAmount;
    }

    return {
      basePrice,
      discounts,
      finalPrice,
      breakdown
    };
  }

  private applyDifficultyMultiplier(basePrice: number, difficulty: number): number {
    const multiplier = DIFFICULTY_MULTIPLIERS[difficulty as keyof typeof DIFFICULTY_MULTIPLIERS] || 1;
    return basePrice * multiplier;
  }

  private getDifficultyMultiplierText(difficulty: number): string {
    const texts: { [key: number]: string } = {
      1: '-15%',
      2: '-5%',
      3: '0%',
      4: '+5%',
      5: '+15%'
    };

    return texts[difficulty] || '0%';
  }

  private calculateMaterialDiscount(materials: CharacterMaterials, difficulty: number): number {
    let totalDiscount = 0;

    // Desconto por itens de drop
    totalDiscount += Math.floor(materials.dropItems.gray / 10) * 0; // Cinza não dá desconto
    totalDiscount += Math.floor(materials.dropItems.green / 10) * MATERIAL_DISCOUNT_RATES.dropGreen;
    totalDiscount += Math.floor(materials.dropItems.rare / 6) * MATERIAL_DISCOUNT_RATES.dropRare;

    // Desconto por itens de boss
    totalDiscount += Math.floor(materials.bossItems / 2) * MATERIAL_DISCOUNT_RATES.boss;

    // Desconto por pedras elementais
    totalDiscount += Math.floor(materials.elementalStones.blue / 3) * MATERIAL_DISCOUNT_RATES.elementalBlue;
    totalDiscount += materials.elementalStones.purple * MATERIAL_DISCOUNT_RATES.elementalPurple;
    totalDiscount += materials.elementalStones.golden * MATERIAL_DISCOUNT_RATES.elementalGolden;

    // Desconto por itens de coleta
    totalDiscount += Math.floor(materials.collectItems / 8) * MATERIAL_DISCOUNT_RATES.collect;

    // Aplicar modificador de dificuldade
    const difficultyModifier = this.getDifficultyDiscountModifier(difficulty);
    totalDiscount *= difficultyModifier;

    // Aplicar limite máximo de desconto
    const maxDiscount = this.getMaxDiscount(difficulty);
    return Math.min(totalDiscount, maxDiscount);
  }

  private getDifficultyDiscountModifier(difficulty: number): number {
    const modifiers: { [key: number]: number } = {
      1: 0.75,  // -25%
      2: 0.95,  // -5%
      3: 1.00,  // 0%
      4: 1.05,  // +5%
      5: 1.15   // +15%
    };

    return modifiers[difficulty] || 1;
  }

  private getMaxDiscount(difficulty: number): number {
    const difficultyModifier = this.getDifficultyDiscountModifier(difficulty);
    return MAX_MATERIAL_DISCOUNT * difficultyModifier;
  }
}
