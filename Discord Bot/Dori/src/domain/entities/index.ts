// Domain - Entities
import { RegionName, SpecificAreaName, TreeName, CharacterName, Difficulty, DiscountInfo } from '../types';

export interface Region {
  name: RegionName;
  basePrice: number;
  areas: Area[];
  compass?: Compass;
}

export interface Area {
  name: string;
  price: number;
  explorationPercentage?: number;
}

export interface Compass {
  region: RegionName;
  discountPercentage: number;
}

export interface Tree {
  name: TreeName;
  pricePerLevel: number;
  region: RegionName;
}

export interface Reputation {
  region: RegionName;
  pricePerLevel: number;
}

export interface AdventureService {
  regions: string[];
  specificAreas: string[];
  trees: { name: string; levels: number }[];
  reputations: { region: string; levels: number }[];
  explorationPercentage: number;
  hasCompass: boolean;
  compassRegion?: string;
}

export interface Character {
  name: CharacterName;
  difficulty: Difficulty;
  materials: CharacterMaterials;
}

export interface CharacterMaterials {
  talents?: boolean;
  weapon?: boolean;
  artifacts?: boolean;
  dropItems?: {
    gray: number;
    green: number;
    rare: number;
  };
  bossItems?: number;
  elementalStones?: {
    blue: number;
    purple: number;
    golden: number;
  };
  collectItems?: number;
}

export interface BuildService {
  character: string;
  difficulty: Difficulty;
  materials: CharacterMaterials;
}

export interface PriceCalculationResult {
  basePrice: number;
  discounts: DiscountInfo[];
  finalPrice: number;
  breakdown: string[];
}
