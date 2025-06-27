// Domain - Validation Service
import { 
  RegionName, 
  SpecificAreaName, 
  TreeName, 
  CharacterName, 
  Difficulty,
  InvalidRegionError,
  InvalidCharacterError,
  InvalidDifficultyError
} from './types';
import { 
  REGION_PRICES, 
  SPECIFIC_AREA_PRICES, 
  TREE_PRICES, 
  CHARACTER_DIFFICULTIES 
} from './constants';

export interface IValidationService {
  validateRegion(region: string): RegionName;
  validateSpecificArea(area: string): SpecificAreaName;
  validateTree(tree: string): TreeName;
  validateCharacter(character: string): CharacterName;
  validateDifficulty(difficulty: number): Difficulty;
  validateExplorationPercentage(percentage: number): number;
  parseCommaSeparatedString(input: string): string[];
}

export class ValidationService implements IValidationService {
  validateRegion(region: string): RegionName {
    const normalizedRegion = region.toLowerCase();
    if (!(normalizedRegion in REGION_PRICES)) {
      throw new InvalidRegionError(region);
    }
    return normalizedRegion as RegionName;
  }

  validateSpecificArea(area: string): SpecificAreaName {
    const normalizedArea = area.toLowerCase();
    if (!(normalizedArea in SPECIFIC_AREA_PRICES)) {
      throw new Error(`Invalid specific area: ${area}`);
    }
    return normalizedArea as SpecificAreaName;
  }

  validateTree(tree: string): TreeName {
    const normalizedTree = tree.toLowerCase();
    if (!(normalizedTree in TREE_PRICES)) {
      throw new Error(`Invalid tree: ${tree}`);
    }
    return normalizedTree as TreeName;
  }

  validateCharacter(character: string): CharacterName {
    const normalizedCharacter = character.toLowerCase();
    if (!(normalizedCharacter in CHARACTER_DIFFICULTIES)) {
      throw new InvalidCharacterError(character);
    }
    return normalizedCharacter as CharacterName;
  }

  validateDifficulty(difficulty: number): Difficulty {
    if (difficulty < 1 || difficulty > 5 || !Number.isInteger(difficulty)) {
      throw new InvalidDifficultyError(difficulty);
    }
    return difficulty as Difficulty;
  }

  validateExplorationPercentage(percentage: number): number {
    if (percentage < 0 || percentage > 100) {
      throw new Error(`Invalid exploration percentage: ${percentage}. Must be between 0 and 100.`);
    }
    return percentage;
  }

  parseCommaSeparatedString(input: string): string[] {
    if (!input || input.trim() === '') {
      return [];
    }
    
    return input
      .split(',')
      .map(item => item.trim())
      .filter(item => item !== '');
  }
}
