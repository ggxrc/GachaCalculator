#!/usr/bin/env node

// Script para registrar comandos do bot
const { REST, Routes } = require('discord.js');
const dotenv = require('dotenv');

dotenv.config();

const commands = [
  {
    name: 'adventure',
    description: 'Calcula o preço de serviços de aventura',
    options: [
      {
        name: 'regioes',
        description: 'Regiões separadas por vírgula',
        type: 3,
        required: false
      },
      {
        name: 'areas',
        description: 'Áreas específicas separadas por vírgula',
        type: 3,
        required: false
      },
      {
        name: 'arvores',
        description: 'Árvores no formato "nome:níveis"',
        type: 3,
        required: false
      },
      {
        name: 'reputacoes',
        description: 'Reputações no formato "região:níveis"',
        type: 3,
        required: false
      },
      {
        name: 'exploracao',
        description: 'Percentual de exploração (0-100)',
        type: 10,
        required: false
      },
      {
        name: 'bussola',
        description: 'Possui bússola?',
        type: 5,
        required: false
      },
      {
        name: 'regiao_bussola',
        description: 'Região da bússola',
        type: 3,
        required: false
      }
    ]
  },
  {
    name: 'build',
    description: 'Calcula o preço de build de personagem',
    options: [
      {
        name: 'personagem',
        description: 'Nome do personagem',
        type: 3,
        required: true
      },
      {
        name: 'cinza',
        description: 'Itens de drop cinza coletados',
        type: 4,
        required: false
      },
      {
        name: 'verde',
        description: 'Itens de drop verde coletados',
        type: 4,
        required: false
      },
      {
        name: 'raro',
        description: 'Itens de drop raro coletados',
        type: 4,
        required: false
      },
      {
        name: 'boss',
        description: 'Itens de boss coletados',
        type: 4,
        required: false
      },
      {
        name: 'azul',
        description: 'Pedras elementais azuis coletadas',
        type: 4,
        required: false
      },
      {
        name: 'roxa',
        description: 'Pedras elementais roxas coletadas',
        type: 4,
        required: false
      },
      {
        name: 'dourada',
        description: 'Pedras elementais douradas coletadas',
        type: 4,
        required: false
      },
      {
        name: 'coleta',
        description: 'Itens de coleta coletados',
        type: 4,
        required: false
      }
    ]
  },
  {
    name: 'help',
    description: 'Mostra informações sobre como usar o bot'
  },
  {
    name: 'precos',
    description: 'Mostra tabela de preços base'
  },
  {
    name: 'personagens',
    description: 'Lista personagens por dificuldade',
    options: [
      {
        name: 'dificuldade',
        description: 'Filtrar por dificuldade (1-5)',
        type: 4,
        required: false,
        min_value: 1,
        max_value: 5
      }
    ]
  }
];

async function deployCommands() {
  const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);

  try {
    console.log('🔄 Registrando comandos slash...');

    // Registrar globalmente
    await rest.put(
      Routes.applicationCommands(process.env.CLIENT_ID),
      { body: commands }
    );

    console.log('✅ Comandos registrados com sucesso!');
  } catch (error) {
    console.error('❌ Erro ao registrar comandos:', error);
  }
}

deployCommands();
