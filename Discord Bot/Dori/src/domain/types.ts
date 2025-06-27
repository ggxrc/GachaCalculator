// Domain - Types
import { 
  REGION_PRICES, 
  SPECIFIC_AREA_PRICES, 
  TREE_PRICES, 
  REPUTATION_PRICES,
  CHARACTER_DIFFICULTIES 
} from './constants';

export type RegionName = keyof typeof REGION_PRICES;
export type SpecificAreaName = keyof typeof SPECIFIC_AREA_PRICES;
export type TreeName = keyof typeof TREE_PRICES;
export type ReputationRegion = keyof typeof REPUTATION_PRICES;
export type CharacterName = keyof typeof CHARACTER_DIFFICULTIES;
export type Difficulty = 1 | 2 | 3 | 4 | 5;

export interface DiscountInfo {
  type: string;
  amount: number;
  percentage: number;
}

export interface ServiceBreakdown {
  item: string;
  price: number;
  quantity?: number;
}

// Error types for better error handling
export class InvalidRegionError extends Error {
  constructor(region: string) {
    super(`Invalid region: ${region}`);
    this.name = 'InvalidRegionError';
  }
}

export class InvalidCharacterError extends Error {
  constructor(character: string) {
    super(`Invalid character: ${character}`);
    this.name = 'InvalidCharacterError';
  }
}

export class InvalidDifficultyError extends Error {
  constructor(difficulty: number) {
    super(`Invalid difficulty: ${difficulty}. Must be between 1 and 5.`);
    this.name = 'InvalidDifficultyError';
  }
}
