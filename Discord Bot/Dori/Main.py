import discord
from discord.ext import commands

# Bot config
TOKEN = 'a1aa1f8490b205a504f7871d3d405859b9466e9fcfec31f1c20aba508fcb49cb'
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Catálogo safado de itens
catalogo = {
    'espada': 50,
    'arco': 40,
    'livro': 30,
    'lanca': 45,
    'catalisador': 35
}

# Carrinho temporário por usuário
carrinhos = {}

# Evento pra quando o bot liga
@bot.event
async def on_ready():
    print(f'Bot {bot.user} tá online, porra!')

# Comando pra ver os itens
@bot.command()
async def loja(ctx):
    msg = "**🛒 Itens disponíveis:**\n"
    for item, preco in catalogo.items():
        msg += f"- {item.title()} ➝ R$ {preco}\n"
    await ctx.send(msg)

# Comando pra adicionar item
@bot.command()
async def add(ctx, item: str, quantidade: int = 1):
    user = str(ctx.author.id)
    item = item.lower()

    if item not in catalogo:
        await ctx.send(f"🛑 Item `{item}` não existe, ZÉ RUELA.")
        return

    if user not in carrinhos:
        carrinhos[user] = {}

    if item in carrinhos[user]:
        carrinhos[user][item] += quantidade
    else:
        carrinhos[user][item] = quantidade

    await ctx.send(f"✅ {quantidade}x `{item}` adicionado ao seu carrinho, patrão!")

# Comando pra ver carrinho
@bot.command()
async def carrinho(ctx):
    user = str(ctx.author.id)
    if user not in carrinhos or not carrinhos[user]:
        await ctx.send("🛒 Seu carrinho tá mais vazio que a conta do Alessandro no final do mês.")
        return

    total = 0
    msg = "**🛍️ Seu carrinho:**\n"
    for item, qtd in carrinhos[user].items():
        preco = catalogo[item] * qtd
        total += preco
        msg += f"- {item.title()} x{qtd} ➝ R$ {preco}\n"

    msg += f"\n💰 **Total: R$ {total}**"
    await ctx.send(msg)

# Comando pra limpar o carrinho
@bot.command()
async def limpar(ctx):
    user = str(ctx.author.id)
    carrinhos[user] = {}
    await ctx.send("🗑️ Seu carrinho foi limpo, chefia.")

# Rodando o bot
bot.run(TOKEN)
