import { IPriceRepository } from './price-repository.interface';

export class PriceRepository implements IPriceRepository {
  getRegionPrice(region: string): number {
    // Implementação fictícia para exemplo
    const regionPrices: Record<string, number> = {
      Mondstadt: 35,
      Liyue: 40,
      Inazuma: 50,
      Sumeru: 100,
      Fontaine: 55,
      Natlan: 60,
    };
    return regionPrices[region] || 0;
  }

  getSpecificAreaPrice(area: string): number {
    // Implementação fictícia para exemplo
    const areaPrices: Record<string, number> = {
      Dragonspine: 30,
      Despenhadeiro: 50,
      ValeChenyu: 50,
      Enkanomiya: 40,
      MarAntigo: 45,
      Vulcao: 40,
    };
    return areaPrices[area] || 0;
  }

  getTreePrice(tree: string): number {
    // Implementação fictícia para exemplo
    const treePrices: Record<string, number> = {
      Sabugueiro: 1.5,
      PedraLumen: 1.75,
      Sakura: 1.75,
      ArvoreDosSonhos: 2.25,
      LagoDasPari: 2.5,
      FonteDeLucine: 2,
      PlacaDeTona: 2,
    };
    return treePrices[tree] || 0;
  }

  getReputationPrice(region: string): number {
    // Implementação fictícia para exemplo
    const reputationPrices: Record<string, number> = {
      Mondstadt: 1,
      Liyue: 1.25,
      Inazuma: 2,
      Sumeru: 1.5,
      Fontaine: 2,
      Natlan: 1.75,
    };
    return reputationPrices[region] || 0;
  }

  getCompassDiscount(region: string): number {
    // Implementação fictícia para exemplo
    const compassDiscounts: Record<string, number> = {
      Mondstadt: 5,
      Liyue: 11,
      Inazuma: 17,
      Sumeru: 25,
      Fontaine: 12,
      Natlan: 15,
    };
    return compassDiscounts[region] || 0;
  }

  getCharacterBasePrice(): number {
    return 30; // Preço base fictício
  }

  getCharacterDifficulty(character: string): number {
    // Implementação fictícia para exemplo
    const difficultyMultipliers: Record<string, number> = {
      dificuldade1: -0.15,
      dificuldade2: -0.05,
      dificuldade3: 0,
      dificuldade4: 0.05,
      dificuldade5: 0.15,
    };
    return difficultyMultipliers[character] || 0;
  }
}
