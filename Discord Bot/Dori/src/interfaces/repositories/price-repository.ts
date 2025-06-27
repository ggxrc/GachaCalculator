// Interfaces - Price Repository Implementation
import { IPriceRepository } from '../../domain/repositories/price-repository.interface';
import {
  REGION_PRICES,
  SPECIFIC_AREA_PRICES,
  TREE_PRICES,
  REPUTATION_PRICES,
  COMPASS_DISCOUNTS,
  CHARACTER_DIFFICULTIES,
  CHARACTER_BASE_PRICE
} from '../../domain/constants';

export class PriceRepository implements IPriceRepository {
  getRegionPrice(region: string): number {
    return REGION_PRICES[region.toLowerCase() as keyof typeof REGION_PRICES] || 0;
  }

  getSpecificAreaPrice(area: string): number {
    return SPECIFIC_AREA_PRICES[area.toLowerCase() as keyof typeof SPECIFIC_AREA_PRICES] || 0;
  }

  getTreePrice(tree: string): number {
    return TREE_PRICES[tree.toLowerCase() as keyof typeof TREE_PRICES] || 0;
  }

  getReputationPrice(region: string): number {
    return REPUTATION_PRICES[region.toLowerCase() as keyof typeof REPUTATION_PRICES] || 0;
  }

  getCompassDiscount(region: string): number {
    return COMPASS_DISCOUNTS[region.toLowerCase() as keyof typeof COMPASS_DISCOUNTS] || 0;
  }

  getCharacterBasePrice(): number {
    return CHARACTER_BASE_PRICE;
  }

  getCharacterDifficulty(character: string): number {
    return CHARACTER_DIFFICULTIES[character.toLowerCase() as keyof typeof CHARACTER_DIFFICULTIES] || 3;
  }
}
