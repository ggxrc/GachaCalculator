// Domain - Repository Interfaces
export interface IPriceRepository {
  getRegionPrice(region: string): number;
  getSpecificAreaPrice(area: string): number;
  getTreePrice(tree: string): number;
  getReputationPrice(region: string): number;
  getCompassDiscount(region: string): number;
  getCharacterBasePrice(): number;
  getCharacterDifficulty(character: string): number;
}
