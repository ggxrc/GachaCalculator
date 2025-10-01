import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import json
import asyncio
from datetime import datetime

load_dotenv()

# Configurações do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Sistema de carrinho - armazenamento temporário
carrinhos_usuarios = {}

# Dados de precificação
PRECOS_BASE_REGIOES = {
    'mondstadt': 35.00,
    'liyue': 40.00,
    'inazuma': 50.00,
    'sumeru': 100.00,
    'fontaine': 55.00,
    'natlan': 60.00
}

PRECOS_AREAS_ESPECIFICAS = {
    'dragonspine': 30.00,
    'despenhadeiro': 50.00,
    'vale_chenyu': 50.00,
    'enkanomiya': 40.00,
    'mar_antigo': 45.00,
    'vulcao': 40.00
}

PRECOS_ARVORES = {
    'sabugueiro': 1.50,
    'arvore_chenyu': 1.75,
    'pedra_lumem': 1.75,
    'sakura': 1.75,
    'arvore_sonhos': 2.25,
    'lago_pari': 2.50,
    'fonte_lucine': 2.00,
    'placa_tona': 2.00
}

DESCONTO_BUSSOLA = {
    'mondstadt': 0.05,
    'liyue': 0.11,
    'inazuma': 0.17,
    'sumeru': 0.25,
    'fontaine': 0.12,
    'natlan': 0.15
}

PRECO_BASE_PERSONAGEM = 30.00
MULTIPLICADOR_DIFICULDADE = {
    1: -0.15,
    2: -0.05,
    3: 0.00,
    4: 0.05,
    5: 0.15
}

PERSONAGENS_DIFICULDADE = {
    1: ['ifa', 'kazuha', 'emillie', 'kaveh', 'kachina', 'noelle', 'furina', 'fischl', 'bennett'],
    2: ['scaramouche', 'chasca', 'jean', 'lynette', 'sucrose', 'yumemizuki', 'kinich', 'kirara', 'tighnari', 'chiori', 'xilonen', 'dahlia', 'layla', 'dori', 'iansan', 'lisa', 'yae', 'chevreuse', 'mavuika'],
    3: ['faruzan', 'lan_yan', 'sayu', 'retentora', 'collei', 'nahida', 'yaoyao', 'ningguang', 'yunjin', 'candace', 'mualani', 'neuvillette', 'nilou', 'xingqiu', 'yelan', 'citlali', 'diona', 'escoffier', 'kaeya', 'rosaria', 'skirk', 'kujou_sara', 'kuki_shinobu', 'ororon', 'varesa', 'amber', 'gaming', 'lyney', 'xiangling', 'yoimiya'],
    4: ['venti', 'xiao', 'alhaitham', 'albedo', 'gorou', 'navia', 'zhongli', 'barbara', 'mona', 'kokomi', 'sigewinne', 'childe', 'charlotte', 'eula', 'freminet', 'ganyu', 'ayaka', 'mica', 'shenhe', 'wriothesley', 'beidou', 'clorinde', 'razor', 'raiden', 'arlecchino', 'dehya', 'diluc', 'hutao', 'klee', 'thoma', 'yanfei'],
    5: ['heizou', 'baizhu', 'itto', 'ayato', 'aloy', 'chongyun', 'qiqi', 'cyno', 'keqing', 'sethos', 'xinyan']
}

# Classes para o sistema de carrinho
class ItemCarrinho:
    def __init__(self, tipo, nome, preco, detalhes=None):
        self.tipo = tipo  # "exploracao", "personagem", "arvore", etc.
        self.nome = nome
        self.preco = preco
        self.detalhes = detalhes or {}
        
    def to_dict(self):
        return {
            'tipo': self.tipo,
            'nome': self.nome,
            'preco': self.preco,
            'detalhes': self.detalhes
        }

class Carrinho:
    def __init__(self, user_id):
        self.user_id = user_id
        self.itens = []
        self.created_at = datetime.now()
    
    def adicionar_item(self, item):
        self.itens.append(item)
    
    def remover_item(self, index):
        if 0 <= index < len(self.itens):
            return self.itens.pop(index)
        return None
    
    def calcular_total(self):
        return sum(item.preco for item in self.itens)
    
    def limpar(self):
        self.itens.clear()
    
    def gerar_resumo(self):
        if not self.itens:
            return "Carrinho vazio"
        
        resumo_por_tipo = {}
        for item in self.itens:
            tipo = item.tipo
            if tipo not in resumo_por_tipo:
                resumo_por_tipo[tipo] = []
            resumo_por_tipo[tipo].append(item.nome)
        
        linhas = []
        for tipo, nomes in resumo_por_tipo.items():
            contador = {}
            for nome in nomes:
                contador[nome] = contador.get(nome, 0) + 1
            
            for nome, qtd in contador.items():
                if tipo == "exploracao":
                    linhas.append(f"{qtd}x Exploração - {nome.title()}")
                elif tipo == "personagem":
                    linhas.append(f"{qtd}x Build de Personagem - {nome.title()}")
                elif tipo == "arvore":
                    linhas.append(f"{qtd}x Árvore - {nome.title()}")
                else:
                    linhas.append(f"{qtd}x {tipo.title()} - {nome.title()}")
        
        return "\n".join(linhas)

# Funções de cálculo de preços
def calcular_desconto_exploracao(porcentagem_exploracao):
    if porcentagem_exploracao > 80:
        porcentagem_exploracao = 80
    return porcentagem_exploracao * 0.0045

def calcular_preco_regiao(regiao, tem_bussola=False, porcentagem_exploracao=0):
    preco_base = PRECOS_BASE_REGIOES.get(regiao.lower())
    if not preco_base:
        return None
    
    preco_final = preco_base
    
    if tem_bussola:
        desconto_bussola = DESCONTO_BUSSOLA.get(regiao.lower(), 0)
        preco_final = preco_final * (1 - desconto_bussola)
    
    if porcentagem_exploracao > 0:
        desconto_exploracao = calcular_desconto_exploracao(porcentagem_exploracao)
        preco_final = preco_final * (1 - desconto_exploracao)
    
    return round(preco_final, 2)

def obter_dificuldade_personagem(nome_personagem):
    nome = nome_personagem.lower().replace(' ', '_')
    for dificuldade, personagens in PERSONAGENS_DIFICULDADE.items():
        if nome in personagens:
            return dificuldade
    return None

def calcular_preco_personagem(nome_personagem):
    dificuldade = obter_dificuldade_personagem(nome_personagem)
    if not dificuldade:
        return None
    
    preco_base = PRECO_BASE_PERSONAGEM
    multiplicador = 1 + MULTIPLICADOR_DIFICULDADE[dificuldade]
    preco_final = preco_base * multiplicador
    
    return round(preco_final, 2)

def calcular_preco_arvore(arvore, niveis, explorar_completo=False):
    preco_por_nivel = PRECOS_ARVORES.get(arvore.lower())
    if not preco_por_nivel:
        return None
    
    preco_total = niveis * preco_por_nivel
    
    if explorar_completo:
        preco_total = preco_total * 0.25
    
    return round(preco_total, 2)

# Funções de carrinho
def obter_carrinho(user_id):
    if user_id not in carrinhos_usuarios:
        carrinhos_usuarios[user_id] = Carrinho(user_id)
    return carrinhos_usuarios[user_id]

def salvar_carrinho(carrinho):
    try:
        with open('carrinhos.json', 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    data[str(carrinho.user_id)] = {
        'itens': [item.to_dict() for item in carrinho.itens],
        'total': carrinho.calcular_total(),
        'created_at': carrinho.created_at.isoformat()
    }
    
    with open('carrinhos.json', 'w') as f:
        json.dump(data, f, indent=2)

# Views para interface interativa
class MenuPrincipalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='🗺️ Serviços de Exploração', style=discord.ButtonStyle.primary)
    async def exploracao_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ExploracaoView()
        embed = discord.Embed(title="🗺️ Serviços de Exploração", color=0x00ff00)
        embed.add_field(name="Escolha o tipo de exploração:", value="• Regiões completas\n• Áreas específicas\n• Árvores especiais", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='⚔️ Builds de Personagens', style=discord.ButtonStyle.success)
    async def personagem_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = PersonagemView()
        embed = discord.Embed(title="⚔️ Builds de Personagens", color=0x00ff00)
        embed.add_field(name="Build completa inclui:", value="• Ascensão até nível 80/90\n• Talentos 8/8/8 ou 9/9/9\n• Artefatos 5* com substatus\n• Arma apropriada", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='🛒 Ver Carrinho', style=discord.ButtonStyle.secondary)
    async def carrinho_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        carrinho = obter_carrinho(interaction.user.id)
        view = CarrinhoView(carrinho)
        
        embed = discord.Embed(title="🛒 Seu Carrinho", color=0x00ff00)
        
        if not carrinho.itens:
            embed.add_field(name="Carrinho vazio", value="Adicione alguns serviços primeiro!", inline=False)
        else:
            embed.add_field(name="Itens:", value=carrinho.gerar_resumo(), inline=False)
            embed.add_field(name="💰 Total:", value=f"R$ {carrinho.calcular_total():.2f}", inline=False)
        
        await interaction.response.edit_message(embed=embed, view=view)

class ExploracaoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='🏞️ Regiões Completas', style=discord.ButtonStyle.primary)
    async def regioes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = RegiaoSelecaoView()
        embed = discord.Embed(title="🏞️ Exploração de Regiões", color=0x00ff00)
        embed.add_field(name="Selecione a região:", value="Exploração 100% da região escolhida", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='🌳 Árvores Especiais', style=discord.ButtonStyle.success)
    async def arvores_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ArvoreSelecaoView()
        embed = discord.Embed(title="🌳 Árvores Especiais", color=0x00ff00)
        embed.add_field(name="Selecione a árvore:", value="Upagem até o nível máximo", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='🔙 Voltar', style=discord.ButtonStyle.secondary)
    async def voltar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MenuPrincipalView()
        embed = discord.Embed(title="🤖 Dori - Calculadora Genshin Impact", description="Selecione uma categoria:", color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=view)

class RegiaoSelecaoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        
        regioes = ['mondstadt', 'liyue', 'inazuma', 'sumeru', 'fontaine', 'natlan']
        for i, regiao in enumerate(regioes):
            if i < 5:  # Discord limit
                button = discord.ui.Button(
                    label=regiao.title(),
                    style=discord.ButtonStyle.primary,
                    custom_id=f"regiao_{regiao}"
                )
                button.callback = self.criar_callback_regiao(regiao)
                self.add_item(button)
    
    def criar_callback_regiao(self, regiao):
        async def callback(interaction):
            modal = RegiaoModal(regiao)
            await interaction.response.send_modal(modal)
        return callback
    
    @discord.ui.button(label='🔙 Voltar', style=discord.ButtonStyle.secondary)
    async def voltar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ExploracaoView()
        embed = discord.Embed(title="🗺️ Serviços de Exploração", color=0x00ff00)
        embed.add_field(name="Escolha o tipo de exploração:", value="• Regiões completas\n• Áreas específicas\n• Árvores especiais", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)

class ArvoreSelecaoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        
        arvores = ['sabugueiro', 'sakura', 'arvore_sonhos', 'lago_pari']
        for arvore in arvores:
            button = discord.ui.Button(
                label=arvore.replace('_', ' ').title(),
                style=discord.ButtonStyle.success,
                custom_id=f"arvore_{arvore}"
            )
            button.callback = self.criar_callback_arvore(arvore)
            self.add_item(button)
    
    def criar_callback_arvore(self, arvore):
        async def callback(interaction):
            modal = ArvoreModal(arvore)
            await interaction.response.send_modal(modal)
        return callback
    
    @discord.ui.button(label='🔙 Voltar', style=discord.ButtonStyle.secondary)
    async def voltar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ExploracaoView()
        embed = discord.Embed(title="🗺️ Serviços de Exploração", color=0x00ff00)
        embed.add_field(name="Escolha o tipo de exploração:", value="• Regiões completas\n• Áreas específicas\n• Árvores especiais", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)

class PersonagemView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='💫 5 Estrelas', style=discord.ButtonStyle.primary)
    async def cinco_estrelas_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = PersonagemModal("5 estrelas")
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label='⭐ 4 Estrelas', style=discord.ButtonStyle.success)
    async def quatro_estrelas_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = PersonagemModal("4 estrelas")
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label='🔙 Voltar', style=discord.ButtonStyle.secondary)
    async def voltar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MenuPrincipalView()
        embed = discord.Embed(title="🤖 Dori - Calculadora Genshin Impact", description="Selecione uma categoria:", color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=view)

class CarrinhoView(discord.ui.View):
    def __init__(self, carrinho):
        super().__init__(timeout=300)
        self.carrinho = carrinho
    
    @discord.ui.button(label='💳 Finalizar Pedido', style=discord.ButtonStyle.success)
    async def finalizar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.carrinho.itens:
            await interaction.response.send_message("❌ Carrinho vazio! Adicione alguns serviços primeiro.", ephemeral=True)
            return
        
        # Salva o carrinho
        salvar_carrinho(self.carrinho)
        
        embed = discord.Embed(title="✅ Pedido Finalizado!", color=0x00ff00)
        embed.add_field(name="Resumo do Pedido:", value=self.carrinho.gerar_resumo(), inline=False)
        embed.add_field(name="💰 Total:", value=f"R$ {self.carrinho.calcular_total():.2f}", inline=False)
        embed.add_field(name="📞 Próximo Passo:", value="Entre em contato para confirmar o pedido e pagamento!", inline=False)
        
        # Limpa o carrinho
        self.carrinho.limpar()
        
        view = MenuPrincipalView()
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='🗑️ Limpar Carrinho', style=discord.ButtonStyle.danger)
    async def limpar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.carrinho.limpar()
        
        embed = discord.Embed(title="🛒 Carrinho Limpo", color=0x00ff00)
        embed.add_field(name="Carrinho vazio", value="Adicione alguns serviços!", inline=False)
        
        view = CarrinhoView(self.carrinho)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='➕ Continuar Comprando', style=discord.ButtonStyle.primary)
    async def continuar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MenuPrincipalView()
        embed = discord.Embed(title="🤖 Dori - Calculadora Genshin Impact", description="Selecione uma categoria:", color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=view)

# Modals para entrada de dados
class RegiaoModal(discord.ui.Modal):
    def __init__(self, regiao):
        super().__init__(title=f"Exploração - {regiao.title()}")
        self.regiao = regiao
        
        self.exploracao_atual = discord.ui.TextInput(
            label="Exploração atual (%)",
            placeholder="Ex: 65 (deixe 0 se não explorou)",
            default="0",
            max_length=3
        )
        
        self.tem_bussola = discord.ui.TextInput(
            label="Possui bússola da região? (sim/não)",
            placeholder="sim ou não",
            default="não",
            max_length=3
        )
        
        self.add_item(self.exploracao_atual)
        self.add_item(self.tem_bussola)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            exploracao = int(self.exploracao_atual.value)
            bussola = self.tem_bussola.value.lower() in ['sim', 's', 'yes', 'y']
            
            preco = calcular_preco_regiao(self.regiao, bussola, exploracao)
            
            if preco is None:
                await interaction.response.send_message("❌ Erro ao calcular preço!", ephemeral=True)
                return
            
            carrinho = obter_carrinho(interaction.user.id)
            item = ItemCarrinho(
                "exploracao",
                self.regiao,
                preco,
                {"bussola": bussola, "exploracao_atual": exploracao}
            )
            carrinho.adicionar_item(item)
            
            view = ContinuarComprandoView()
            embed = discord.Embed(title="✅ Item Adicionado!", color=0x00ff00)
            embed.add_field(name="Serviço:", value=f"Exploração completa - {self.regiao.title()}", inline=False)
            embed.add_field(name="Preço:", value=f"R$ {preco:.2f}", inline=False)
            embed.add_field(name="Total no carrinho:", value=f"R$ {carrinho.calcular_total():.2f}", inline=False)
            
            await interaction.response.edit_message(embed=embed, view=view)
            
        except ValueError:
            await interaction.response.send_message("❌ Por favor, insira um número válido para a exploração!", ephemeral=True)

class ArvoreModal(discord.ui.Modal):
    def __init__(self, arvore):
        super().__init__(title=f"Árvore - {arvore.replace('_', ' ').title()}")
        self.arvore = arvore
        
        self.nivel_atual = discord.ui.TextInput(
            label="Nível atual da árvore",
            placeholder="Ex: 25 (deixe 0 se não upou)",
            default="0",
            max_length=3
        )
        
        self.exploracao_completa = discord.ui.TextInput(
            label="Exploração completa da região? (sim/não)",
            placeholder="sim para 75% de desconto",
            default="sim",
            max_length=3
        )
        
        self.add_item(self.nivel_atual)
        self.add_item(self.exploracao_completa)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            nivel_atual = int(self.nivel_atual.value)
            explorar_completo = self.exploracao_completa.value.lower() in ['sim', 's', 'yes', 'y']
            
            niveis_restantes = 50 - nivel_atual  # Assumindo máximo 50
            if niveis_restantes <= 0:
                await interaction.response.send_message("❌ Esta árvore já está no nível máximo!", ephemeral=True)
                return
            
            preco = calcular_preco_arvore(self.arvore, niveis_restantes, explorar_completo)
            
            if preco is None:
                await interaction.response.send_message("❌ Erro ao calcular preço!", ephemeral=True)
                return
            
            carrinho = obter_carrinho(interaction.user.id)
            item = ItemCarrinho(
                "arvore",
                self.arvore.replace('_', ' ').title(),
                preco,
                {"nivel_atual": nivel_atual, "niveis_restantes": niveis_restantes, "explorar_completo": explorar_completo}
            )
            carrinho.adicionar_item(item)
            
            view = ContinuarComprandoView()
            embed = discord.Embed(title="✅ Item Adicionado!", color=0x00ff00)
            embed.add_field(name="Serviço:", value=f"Árvore - {self.arvore.replace('_', ' ').title()}", inline=False)
            embed.add_field(name="Níveis:", value=f"{niveis_restantes} níveis", inline=False)
            embed.add_field(name="Preço:", value=f"R$ {preco:.2f}", inline=False)
            embed.add_field(name="Total no carrinho:", value=f"R$ {carrinho.calcular_total():.2f}", inline=False)
            
            await interaction.response.edit_message(embed=embed, view=view)
            
        except ValueError:
            await interaction.response.send_message("❌ Por favor, insira um número válido para o nível!", ephemeral=True)

class PersonagemModal(discord.ui.Modal):
    def __init__(self, raridade):
        super().__init__(title=f"Build de Personagem ({raridade})")
        self.raridade = raridade
        
        self.nome_personagem = discord.ui.TextInput(
            label="Nome do personagem",
            placeholder="Ex: Kazuha, Bennett, Furina...",
            max_length=50
        )
        
        self.add_item(self.nome_personagem)
    
    async def on_submit(self, interaction: discord.Interaction):
        nome = self.nome_personagem.value.strip()
        preco = calcular_preco_personagem(nome)
        
        if preco is None:
            await interaction.response.send_message(f"❌ Personagem '{nome}' não encontrado! Verifique a ortografia.", ephemeral=True)
            return
        
        carrinho = obter_carrinho(interaction.user.id)
        item = ItemCarrinho(
            "personagem",
            nome.title(),
            preco,
            {"raridade": self.raridade}
        )
        carrinho.adicionar_item(item)
        
        view = ContinuarComprandoView()
        embed = discord.Embed(title="✅ Item Adicionado!", color=0x00ff00)
        embed.add_field(name="Serviço:", value=f"Build de Personagem - {nome.title()}", inline=False)
        embed.add_field(name="Preço:", value=f"R$ {preco:.2f}", inline=False)
        embed.add_field(name="Total no carrinho:", value=f"R$ {carrinho.calcular_total():.2f}", inline=False)
        
        await interaction.response.edit_message(embed=embed, view=view)

class ContinuarComprandoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='🛒 Ver Carrinho', style=discord.ButtonStyle.primary)
    async def ver_carrinho_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        carrinho = obter_carrinho(interaction.user.id)
        view = CarrinhoView(carrinho)
        
        embed = discord.Embed(title="🛒 Seu Carrinho", color=0x00ff00)
        embed.add_field(name="Itens:", value=carrinho.gerar_resumo(), inline=False)
        embed.add_field(name="💰 Total:", value=f"R$ {carrinho.calcular_total():.2f}", inline=False)
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='➕ Continuar Comprando', style=discord.ButtonStyle.success)
    async def continuar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MenuPrincipalView()
        embed = discord.Embed(title="🤖 Dori - Calculadora Genshin Impact", description="Selecione uma categoria:", color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=view)

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos slash")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

@bot.tree.command(name="dori", description="🤖 Calculadora de preços Genshin Impact - Sistema de carrinho")
async def dori_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Dori - Calculadora Genshin Impact",
        description="Bem-vindo ao sistema de carrinho! Selecione uma categoria para começar:",
        color=0x00ff00
    )
    embed.add_field(
        name="📋 Como funciona:",
        value="1. Escolha um serviço\n2. Configure os detalhes\n3. Adicione ao carrinho\n4. Finalize o pedido",
        inline=False
    )
    
    view = MenuPrincipalView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Roda o bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ Token do Discord não encontrado no arquivo .env!")
