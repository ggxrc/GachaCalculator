# Usar uma imagem oficial do Node.js como base
FROM node:18

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de dependências
COPY package.json package-lock.json ./

# Instalar as dependências
RUN npm install

# Copiar o restante do código da aplicação
COPY . .

# Construir o projeto
RUN npm run build

# Expor a porta usada pelo bot
EXPOSE 3000

# Comando para iniciar o bot
CMD ["npm", "start"]
