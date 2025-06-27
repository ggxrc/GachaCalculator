// Domain - Value Objects and Constants
export const REGION_PRICES = {
  mondstadt: 35.00,
  liyue: 40.00,
  inazuma: 50.00,
  sumeru: 100.00,
  fontaine: 55.00,
  natlan: 60.00
} as const;

export const SPECIFIC_AREA_PRICES = {
  dragonspine: 30.00,
  despenhadeiro: 50.00,
  vale_chenyu: 50.00,
  enkanomiya: 40.00,
  mar_antigo: 45.00,
  vulcao: 40.00
} as const;

export const TREE_PRICES = {
  sabugueiro: 1.50,
  arvore_chenyu: 1.75,
  pedra_lumem: 1.75,
  sakura: 1.75,
  arvore_sonhos: 2.25,
  lago_pari: 2.50,
  fonte_lucine: 2.00,
  placa_tona: 2.00
} as const;

export const REPUTATION_PRICES = {
  mondstadt: 1.00,
  liyue: 1.25,
  inazuma: 2.00,
  sumeru: 1.50,
  fontaine: 2.00,
  natlan: 1.75
} as const;

export const COMPASS_DISCOUNTS = {
  mondstadt: 5,
  liyue: 11,
  inazuma: 17,
  sumeru: 25,
  fontaine: 12,
  natlan: 15
} as const;

export const CHARACTER_DIFFICULTIES = {
  // Dificuldade 1
  ifa: 1, kazuha: 1, emillie: 1, kaveh: 1, kachina: 1,
  noelle: 1, furina: 1, fischl: 1, bennett: 1,
  
  // Dificuldade 2
  scaramouche: 2, chasca: 2, jean: 2, lynette: 2, sucrose: 2,
  yumemizuki_mizuki: 2, kinich: 2, kirara: 2, tighnari: 2,
  chiori: 2, xilonen: 2, dahlia: 2, layla: 2, dori: 2,
  iansan: 2, lisa: 2, yae_miko: 2, chevreuse: 2, mavuika: 2,
  
  // Dificuldade 3
  faruzan: 3, lan_yan: 3, sayu: 3, retentora: 3, collei: 3,
  nahida: 3, yaoyao: 3, ningguang: 3, yunjin: 3, candace: 3,
  mualani: 3, neuvillette: 3, nilou: 3, xingqiu: 3, yelan: 3,
  citlali: 3, diona: 3, escoffier: 3, kaeya: 3, rosaria: 3,
  skirk: 3, kujou_sara: 3, kuki_shinobu: 3, ororon: 3,
  varesa: 3, amber: 3, gaming: 3, lyney: 3, xiangling: 3, yoimiya: 3,
  
  // Dificuldade 4
  venti: 4, xiao: 4, alhaitham: 4, albedo: 4, gorou: 4,
  navia: 4, zhongli: 4, barbara: 4, mona: 4, kokomi: 4,
  sigewinne: 4, childe: 4, charlotte: 4, eula: 4, freminet: 4,
  ganyu: 4, ayaka: 4, mica: 4, shenhe: 4, wriothesley: 4,
  beidou: 4, clorinde: 4, razor: 4, raiden_shogun: 4,
  arlecchino: 4, dehya: 4, diluc: 4, hu_tao: 4, klee: 4,
  thoma: 4, yanfei: 4,
  
  // Dificuldade 5
  heizou: 5, baizhu: 5, itto: 5, ayato: 5, aloy: 5,
  chongyun: 5, qiqi: 5, cyno: 5, keqing: 5, sethos: 5, xinyan: 5
} as const;

export const DIFFICULTY_MULTIPLIERS = {
  1: 0.85, // -15%
  2: 0.95, // -5%
  3: 1.00, // 0%
  4: 1.05, // +5%
  5: 1.15  // +15%
} as const;

export const MATERIAL_DISCOUNT_RATES = {
  dropGreen: 1.0,      // -1% per 10 items
  dropRare: 1.5,       // -1.5% per 6 items
  boss: 0.5,           // -0.5% per 2 items
  elementalBlue: 0.2,  // -0.2% per 3 items
  elementalPurple: 0.4, // -0.4% per item
  elementalGolden: 0.8, // -0.8% per item
  collect: 0.78        // -0.78% per 8 items
} as const;

export const EXPLORATION_DISCOUNT_RATE = 0.45; // 0.45% per 1% exploration
export const MAX_EXPLORATION_DISCOUNT = 36; // Maximum 36% discount at 80% exploration

export const CHARACTER_BASE_PRICE = 30.00;
export const MAX_MATERIAL_DISCOUNT = 30.00;
