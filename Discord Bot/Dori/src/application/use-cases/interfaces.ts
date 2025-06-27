// Application - Use Case Interfaces
import { AdventureService, BuildService, PriceCalculationResult } from '../../domain/entities';

export interface IAdventurePriceCalculator {
  calculatePrice(service: AdventureService): PriceCalculationResult;
}

export interface IBuildPriceCalculator {
  calculatePrice(service: BuildService): PriceCalculationResult;
}
