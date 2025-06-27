# Dori - Calculadora Genshin Impact Bot

Bot Discord desenvolvido em TypeScript usando arquitetura limpa para calcular preços de serviços do Genshin Impact.

## 🚀 Características

- **Arquitetura Limpa**: Separação clara entre domínio, aplicação e infraestrutura
- **TypeScript**: Código tipado e robusto
- **Discord.js v14**: Suporte completo a Slash Commands
- **Cálculos Precisos**: Implementação fiel às regras de precificação

## 📋 Comandos

### `/adventure` - Cálculo de Serviços de Aventura
Calcula preços para exploração de regiões, áreas específicas, árvores e reputação.

**Parâmetros:**
- `regioes`: Regiões separadas por vírgula (mondstadt, liyue, inazuma, sumeru, fontaine, natlan)
- `areas`: Áreas específicas (dragonspine, despenhadeiro, vale_chenyu, etc.)
- `arvores`: Formato "nome:níveis" separado por vírgula (ex: sakura:10,sabugueiro:5)
- `reputacoes`: Formato "região:níveis" separado por vírgula (ex: mondstadt:5,liyue:3)
- `exploracao`: Percentual de exploração (0-100)
- `bussola`: Possui bússola? (true/false)
- `regiao_bussola`: Região da bússola

**Exemplo:**
```
/adventure regioes:mondstadt,liyue arvores:sakura:10 reputacoes:mondstadt:5 exploracao:80 bussola:true regiao_bussola:mondstadt
```

### `/build` - Cálculo de Build de Personagem
Calcula preços para builds de personagem considerando dificuldade e materiais coletados.

**Parâmetros:**
- `personagem`: Nome do personagem (obrigatório)
- `cinza`: Quantidade de itens de drop cinza coletados
- `verde`: Quantidade de itens de drop verde coletados
- `raro`: Quantidade de itens de drop raro coletados
- `boss`: Quantidade de itens de boss coletados
- `azul`: Quantidade de pedras elementais azuis coletadas
- `roxa`: Quantidade de pedras elementais roxas coletadas
- `dourada`: Quantidade de pedras elementais douradas coletadas
- `coleta`: Quantidade de itens de coleta coletados

**Exemplo:**
```
/build personagem:kazuha verde:20 boss:10 azul:9 coleta:50
```

### `/help` - Ajuda
Mostra informações sobre como usar o bot.

### `/precos` - Tabela de Preços
Exibe a tabela completa de preços base.

### `/personagens` - Lista de Personagens
Lista personagens organizados por dificuldade.

**Parâmetros:**
- `dificuldade`: Filtrar por dificuldade específica (1-5)

## 🛠️ Instalação

### Pré-requisitos
- Node.js 18+ 
- npm ou yarn
- Bot Discord criado no Discord Developer Portal

### Passos

1. **Clone e entre no diretório:**
```bash
cd "C:\Users\ggxrc\Documents\GitHub\GachaCalculator\Discord Bot\Dori"
```

2. **Instale as dependências:**
```bash
npm install
```

3. **Configure as variáveis de ambiente:**
Edite o arquivo `.env`:
```env
DISCORD_TOKEN=seu_token_do_bot
CLIENT_ID=seu_client_id
```

4. **Compile o projeto:**
```bash
npm run build
```

5. **Execute o bot:**
```bash
npm start
```

Para desenvolvimento com hot reload:
```bash
npm run dev
```

## 📁 Estrutura do Projeto

```
src/
├── domain/
│   ├── entities/           # Entidades do domínio
│   └── use-cases/          # Casos de uso e interfaces
│       ├── interfaces.ts
│       ├── adventure-price-calculator.ts
│       └── build-price-calculator.ts
├── infrastructure/
│   └── price-repository.ts # Repositório de dados
├── application/
│   ├── commands.ts         # Comandos principais
│   └── utility-commands.ts # Comandos utilitários
└── index.ts               # Ponto de entrada
```

## 🎯 Sistema de Preços

### Serviços de Aventura

**Preços Base:**
- Mondstadt: R$ 35,00
- Liyue: R$ 40,00  
- Inazuma: R$ 50,00
- Sumeru: R$ 100,00
- Fontaine: R$ 55,00
- Natlan: R$ 60,00

**Descontos:**
- **Bússola**: 5% a 25% dependendo da região
- **Exploração**: 0,45% por 1% de exploração (máximo 36%)

### Builds de Personagem

**Preço Base:** R$ 30,00

**Multiplicadores por Dificuldade:**
- Dificuldade 1: -15%
- Dificuldade 2: -5%  
- Dificuldade 3: 0%
- Dificuldade 4: +5%
- Dificuldade 5: +15%

**Descontos por Materiais:**
- Itens de drop verde: -1% a cada 10
- Itens de drop raro: -1.5% a cada 6
- Itens de boss: -0.5% a cada 2
- Pedras elementais: varia por tipo
- Itens de coleta: -0.78% a cada 8

## 🔧 Scripts Disponíveis

- `npm run build` - Compila TypeScript para JavaScript
- `npm start` - Executa o bot compilado
- `npm run dev` - Executa em modo desenvolvimento
- `npm run watch` - Compila em modo watch

## 📝 Licença

MIT License

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## ⚡ Performance

- Arquitetura limpa garante manutenibilidade
- Cálculos otimizados para resposta rápida
- Tratamento robusto de erros
- Interface intuitiva via Discord
