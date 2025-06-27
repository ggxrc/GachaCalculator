import { AdventurePriceCalculator } from '../application/use-cases/adventure-price-calculator';
import { BuildPriceCalculator } from '../application/use-cases/build-price-calculator';
import { IPriceRepository } from '../domain/repositories/price-repository.interface';
import { ValidationService } from '../domain/validation';
import { PriceRepository } from '../domain/repositories/price-repository';

class DependencyContainer {
  private static instance: DependencyContainer;

  public priceRepository: IPriceRepository;
  public adventurePriceCalculator: AdventurePriceCalculator;
  public buildPriceCalculator: BuildPriceCalculator;
  public validationService: ValidationService;

  private constructor() {
    this.priceRepository = new PriceRepository();
    this.adventurePriceCalculator = new AdventurePriceCalculator(this.priceRepository);
    this.buildPriceCalculator = new BuildPriceCalculator(this.priceRepository);
    this.validationService = new ValidationService();
  }

  public static getInstance(): DependencyContainer {
    if (!DependencyContainer.instance) {
      DependencyContainer.instance = new DependencyContainer();
    }
    return DependencyContainer.instance;
  }
}

export const container = DependencyContainer.getInstance();
