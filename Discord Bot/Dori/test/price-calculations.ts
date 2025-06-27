// Test file for price calculations
import { AdventurePriceCalculator } from '../src/application/use-cases/adventure-price-calculator';
import { BuildPriceCalculator } from '../src/application/use-cases/build-price-calculator';
import { PriceRepository } from '../src/interfaces/repositories/price-repository';
import { AdventureService, BuildService } from '../src/domain/entities';

// Test Adventure Service
const priceRepo = new PriceRepository();
const adventureCalc = new AdventurePriceCalculator(priceRepo);
const buildCalc = new BuildPriceCalculator(priceRepo);

// Test Adventure Calculation
const adventureService: AdventureService = {
  regions: ['mondstadt', 'liyue'],
  specificAreas: ['dragonspine'],
  trees: [{ name: 'sakura', levels: 10 }],
  reputations: [{ region: 'mondstadt', levels: 5 }],
  explorationPercentage: 80,
  hasCompass: true,
  compassRegion: 'mondstadt'
};

const adventureResult = adventureCalc.calculatePrice(adventureService);
console.log('Adventure Service Result:', adventureResult);

// Test Build Calculation
const buildService: BuildService = {
  character: 'kazuha',
  difficulty: 1,
  materials: {
    talents: true,
    weapon: true,
    artifacts: true,
    dropItems: { gray: 0, green: 20, rare: 0 },
    bossItems: 10,
    elementalStones: { blue: 9, purple: 0, golden: 0 },
    collectItems: 50
  }
};

const buildResult = buildCalc.calculatePrice(buildService);
console.log('Build Service Result:', buildResult);
