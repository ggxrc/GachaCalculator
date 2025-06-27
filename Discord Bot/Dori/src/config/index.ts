// Configuration
export const BOT_CONFIG = {
  // Bot Information
  NAME: 'Dori',
  DESCRIPTION: 'Calculadora Genshin Impact Bot',
  VERSION: '1.0.0',
  
  // Discord Configuration
  INTENTS: ['Guilds', 'GuildMessages'],
  
  // Command Configuration
  MAX_EMBED_FIELDS: 25,
  MAX_FIELD_LENGTH: 1024,
  
  // Price Configuration
  CURRENCY_SYMBOL: 'R$',
  DECIMAL_PLACES: 2,
  
  // Validation Limits
  MAX_REGIONS: 6,
  MAX_AREAS: 10,
  MAX_TREES: 8,
  MAX_REPUTATIONS: 6,
  
  // Colors for embeds
  COLORS: {
    SUCCESS: 0x00AE86,
    ERROR: 0xFF0000,
    WARNING: 0xFFA500,
    INFO: 0x5865F2,
    ADVENTURE: 0x00AE86,
    BUILD: 0x9D4EDD
  }
} as const;
