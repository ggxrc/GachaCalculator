import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import math

load_dotenv()

# Configurações do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Sistema de carrinho
CARRINHO_FILE = os.path.join(os.path.dirname(__file__), 'carrinhos.json')

def carregar_carrinhos():
    """Carrega os carrinhos existentes do arquivo JSON"""
    try:
        with open(CARRINHO_FILE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            if conteudo.strip():
                return json.loads(conteudo)
            return {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_carrinhos(carrinhos):
    """Salva os carrinhos no arquivo JSON"""
    with open(CARRINHO_FILE, 'w', encoding='utf-8') as f:
        json.dump(carrinhos, f, ensure_ascii=False, indent=4)

def adicionar_ao_carrinho(user_id, item):
    """Adiciona um item ao carrinho do usuário"""
    carrinhos = carregar_carrinhos()
    user_id_str = str(user_id)
    
    if user_id_str not in carrinhos:
        carrinhos[user_id_str] = {"itens": [], "total": 0.0, "timestamp": datetime.now().isoformat()}
    
    carrinhos[user_id_str]["itens"].append(item)
    carrinhos[user_id_str]["total"] += item["preco"]
    carrinhos[user_id_str]["timestamp"] = datetime.now().isoformat()
    
    salvar_carrinhos(carrinhos)
    return carrinhos[user_id_str]

def obter_carrinho(user_id):
    """Obtém o carrinho atual do usuário"""
    carrinhos = carregar_carrinhos()
    return carrinhos.get(str(user_id), {"itens": [], "total": 0.0})

def limpar_carrinho(user_id):
    """Limpa o carrinho do usuário"""
    carrinhos = carregar_carrinhos()
    if str(user_id) in carrinhos:
        del carrinhos[str(user_id)]
        salvar_carrinhos(carrinhos)

# Dados de precificação
PRECOS_BASE_REGIOES = {
    'mondstadt': 35.00,
    'liyue': 40.00,
    'inazuma': 50.00,
    'sumeru': 100.00,
    'fontaine': 55.00,
    'natlan': 60.00
}

# Descrições amigáveis para regiões
DESCRICAO_REGIOES = {
    'mondstadt': 'Cidade da Liberdade',
    'liyue': 'Porto de Pedra',
    'inazuma': 'Nação da Eternidade',
    'sumeru': 'Nação da Sabedoria',
    'fontaine': 'Nação da Justiça',
    'natlan': 'Nação da Guerra'
}

# Descrições amigáveis para árvores
DESCRICAO_ARVORES = {
    'sabugueiro': 'Árvore Carmesim de Dragonspine',
    'arvore_chenyu': 'Árvore do Vale Chenyu',
    'pedra_lumem': 'Pedra Lúmem do Despenhadeiro',
    'sakura': 'Sakura Sagrada de Inazuma',
    'arvore_sonhos': 'Árvore dos Sonhos de Sumeru',
    'lago_pari': 'Lago das Pari do Mar Antigo',
    'fonte_lucine': 'Fonte de Lucine de Fontaine',
    'placa_tona': 'Placa de Tona de Natlan'
}

PRECOS_AREAS_ESPECIFICAS = {
    'dragonspine': 30.00,
    'despenhadeiro': 50.00,
    'vale_chenyu': 50.00,
    'enkanomiya': 40.00,
    'mar_antigo': 45.00,
    'vulcao': 40.00
}

PRECOS_REPUTACAO = {
    'mondstadt': 1.00,
    'liyue': 1.25,
    'inazuma': 2.00,
    'sumeru': 1.50,
    'fontaine': 2.00,
    'natlan': 1.75
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

REGIOES_NACAO = {
    'mondstadt': {
        'colina_silvante': 12.00,
        'vale_estrelas': 13.00,
        'terras_altas': 14.00,
        'montanhas_coroas': 14.00
    },
    'liyue': {
        'minlin': 11.00,
        'mar_nuvens': 12.00,
        'estuario_qiongji': 12.00,
        'lisha': 13.00,
        'planicies_bishui': 14.00
    },
    'inazuma': {
        'ilha_yashiori': 12.00,
        'kannazuka': 12.00,
        'ilha_watatsumi': 13.00,
        'ilha_narukami': 14.00,
        'ilha_seirai': 14.00,
        'ilha_tsurumi': 15.00
    },
    'sumeru': {
        'campo_vissudha': 11.00,
        'alto_setekh': 11.00,
        'floresta_avidya': 12.00,
        'vanarana': 13.00,
        'sementeira_perdida': 13.00,
        'baixo_setekh': 14.00,
        'reino_ashavan': 14.00,
        'floresta_lokapala': 15.00,
        'vale_ardravi': 16.00,
        'hipostilo_desertico': 17.00,
        'gavireh_lajavard': 17.00,
        'reino_farakhkert': 18.00,
        'deserto_hadramaveth': 19.00
    },
    'fontaine': {
        'regiao_nostoi': 10.00,
        'regiao_mortaine': 10.00,
        'floresta_erinnyes': 11.00,
        'distrito_corte': 11.00,
        'instituto_energia': 12.00,
        'distrito_beryl': 12.00,
        'distrito_belleau': 13.00,
        'regiao_liffey': 14.00
    },
    'natlan': {
        'cordilheira_tezcatepetonco': 11.00,
        'precipicio_quahuacan': 11.00,
        'montanha_coatepec': 12.00,
        'bacia_chamas': 12.00,
        'ochkanatlan': 13.00,
        'atocpan': 13.00,
        'pantanal_toyac': 14.00,
        'vale_tequemecan': 15.00
    }
}

# Dados de personagens
PRECO_BASE_PERSONAGEM = 30.00
MULTIPLICADOR_DIFICULDADE = {
    1: -0.15,
    2: -0.05,
    3: 0.00,
    4: 0.05,
    5: 0.15
}

DESCONTO_ITENS = {
    'cinza': {'quantidade': 10, 'desconto': 0.00},
    'verde': {'quantidade': 10, 'desconto': -0.01},
    'raro': {'quantidade': 6, 'desconto': -0.015},
    'boss': {'quantidade': 2, 'desconto': -0.005},
    'azul': {'quantidade': 3, 'desconto': -0.002},
    'roxa': {'quantidade': 1, 'desconto': -0.004},
    'dourado': {'quantidade': 1, 'desconto': -0.008},
    'coleta': {'quantidade': 8, 'desconto': -0.0078}
}

MODIFICADOR_DIFICULDADE_DESCONTO = {
    1: -0.25,
    2: -0.05,
    3: 0.00,
    4: 0.05,
    5: 0.15
}

DESCONTO_MAXIMO_BASE = -0.30

PERSONAGENS_DIFICULDADE = {
    1: ['ifa', 'kazuha', 'emillie', 'kaveh', 'kachina', 'noelle', 'furina', 'fischl', 'bennett'],
    2: ['scaramouche', 'chasca', 'jean', 'lynette', 'sucrose', 'yumemizuki', 'kinich', 'kirara', 'tighnari', 'chiori', 'xilonen', 'dahlia', 'layla', 'dori', 'iansan', 'lisa', 'yae', 'chevreuse', 'mavuika'],
    3: ['faruzan', 'lan_yan', 'sayu', 'retentora', 'collei', 'nahida', 'yaoyao', 'ningguang', 'yunjin', 'candace', 'mualani', 'neuvillette', 'nilou', 'xingqiu', 'yelan', 'citlali', 'diona', 'escoffier', 'kaeya', 'rosaria', 'skirk', 'kujou_sara', 'kuki_shinobu', 'ororon', 'varesa', 'amber', 'gaming', 'lyney', 'xiangling', 'yoimiya'],
    4: ['venti', 'xiao', 'alhaitham', 'albedo', 'gorou', 'navia', 'zhongli', 'barbara', 'mona', 'kokomi', 'sigewinne', 'childe', 'charlotte', 'eula', 'freminet', 'ganyu', 'ayaka', 'mica', 'shenhe', 'wriothesley', 'beidou', 'clorinde', 'razor', 'raiden', 'arlecchino', 'dehya', 'diluc', 'hutao', 'klee', 'thoma', 'yanfei'],
    5: ['heizou', 'baizhu', 'itto', 'ayato', 'aloy', 'chongyun', 'qiqi', 'cyno', 'keqing', 'sethos', 'xinyan']
}

def calcular_desconto_exploracao(porcentagem_exploracao):
    """Calcula desconto baseado na porcentagem de exploração"""
    if porcentagem_exploracao > 80:
        porcentagem_exploracao = 80
    return porcentagem_exploracao * 0.0045

def calcular_preco_regiao(regiao, tem_bussola=False, porcentagem_exploracao=0):
    """Calcula preço de uma região com descontos"""
    preco_base = PRECOS_BASE_REGIOES.get(regiao.lower())
    if not preco_base:
        return None
    
    preco_final = preco_base
    
    # Aplica desconto da bússola primeiro
    if tem_bussola:
        desconto_bussola = DESCONTO_BUSSOLA.get(regiao.lower(), 0)
        preco_final = preco_final * (1 - desconto_bussola)
    
    # Aplica desconto de exploração
    if porcentagem_exploracao > 0:
        desconto_exploracao = calcular_desconto_exploracao(porcentagem_exploracao)
        preco_final = preco_final * (1 - desconto_exploracao)
    
    return preco_final

def calcular_preco_arvore(arvore, niveis, explorar_completo=False):
    """Calcula preço para upar árvore"""
    preco_por_nivel = PRECOS_ARVORES.get(arvore.lower())
    if not preco_por_nivel:
        return None
    
    preco_total = niveis * preco_por_nivel
    
    # Desconto de 75% se explorar região completa
    if explorar_completo:
        preco_total = preco_total * 0.25
    
    return preco_total

def obter_dificuldade_personagem(nome_personagem):
    """Obtém a dificuldade de um personagem"""
    nome = nome_personagem.lower().replace(' ', '_')
    for dificuldade, personagens in PERSONAGENS_DIFICULDADE.items():
        if nome in personagens:
            return dificuldade
    return None

def calcular_preco_personagem(nome_personagem, itens_coletados=None):
    """Calcula preço de build de personagem"""
    dificuldade = obter_dificuldade_personagem(nome_personagem)
    if not dificuldade:
        return None, None
    
    # Preço base com multiplicador de dificuldade
    preco_base = PRECO_BASE_PERSONAGEM
    multiplicador = 1 + MULTIPLICADOR_DIFICULDADE[dificuldade]
    preco_final = preco_base * multiplicador
    
    # Calcula descontos por itens coletados
    if itens_coletados:
        desconto_total = 0
        modificador = 1 + MODIFICADOR_DIFICULDADE_DESCONTO[dificuldade]
        
        for tipo_item, quantidade in itens_coletados.items():
            if tipo_item in DESCONTO_ITENS:
                info = DESCONTO_ITENS[tipo_item]
                desconto_aplicado = (quantidade / info['quantidade']) * info['desconto']
                desconto_total += desconto_aplicado
        
        # Aplica limite máximo de desconto
        desconto_maximo = DESCONTO_MAXIMO_BASE * modificador
        if desconto_total < desconto_maximo:
            desconto_total = desconto_maximo
        
        preco_final = preco_final * (1 + desconto_total)
    
    return preco_final, f"Dificuldade {dificuldade}"

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

# Classes de Views para menus interativos
class MenuPrincipalView(discord.ui.View):
    """Menu principal da calculadora com categorias de serviços"""
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='🗺️ Exploração', style=discord.ButtonStyle.primary)
    async def exploracao_button(self, interaction, button):
        view = ExploracaoView()
        embed = discord.Embed(
            title="🗺️ Serviços de Exploração",
            description="Selecione o tipo de serviço de exploração que deseja:",
            color=0x3498db
        )
        embed.add_field(name="⚙️ Opções Disponíveis", value=
            "• **Regiões**: Exploração de nações principais\n"
            "• **Áreas Específicas**: Exploração de áreas especiais\n"
            "• **Reputação**: Subir níveis de reputação\n"
            "• **Árvores**: Árvores sagradas e monumentos"
        )
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='⚔️ Personagens', style=discord.ButtonStyle.success)
    async def personagens_button(self, interaction, button):
        view = PersonagensView()
        embed = discord.Embed(
            title="⚔️ Serviços de Personagens",
            description="Selecione o tipo de serviço para personagens:",
            color=0x2ecc71
        )
        embed.add_field(name="⚙️ Opções Disponíveis", value=
            "• **Construção de Personagem**: Subir nível e construir personagem\n"
            "• **Itens de Ascensão**: Calcular com itens já coletados\n"
            "• **Talentos**: Subir talentos de personagens"
        )
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label='🛒 Ver Carrinho', style=discord.ButtonStyle.secondary)
    async def carrinho_button(self, interaction, button):
        carrinho = obter_carrinho(interaction.user.id)
        
        if not carrinho["itens"]:
            embed = discord.Embed(
                title="🛒 Seu carrinho está vazio",
                description="Adicione itens ao seu carrinho primeiro.",
                color=0xe74c3c
            )
            await interaction.response.edit_message(embed=embed, view=self)
            return
            
        view = CarrinhoView()
        embed = gerar_embed_carrinho(carrinho)
        await interaction.response.edit_message(embed=embed, view=view)

class ExploracaoView(discord.ui.View):
    """Menu de serviços de exploração"""
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='🌍 Regiões', style=discord.ButtonStyle.primary)
    async def regioes_button(self, interaction, button):
        view = RegioesView()
        embed = discord.Embed(
            title="🌍 Exploração de Regiões",
            description="Selecione a região que deseja explorar:",
            color=0x3498db
        )
        embed.add_field(name="🗺️ Regiões Disponíveis", value=
            "• **Mondstadt**: A Cidade da Liberdade\n"
            "• **Liyue**: O Porto de Pedra\n"
            "• **Inazuma**: A Nação da Eternidade\n"
            "• **Sumeru**: A Nação da Sabedoria\n"
            "• **Fontaine**: A Nação da Justiça\n"
            "• **Natlan**: A Nação da Guerra"
        )
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='🏔️ Áreas Especiais', style=discord.ButtonStyle.primary)
    async def areas_button(self, interaction, button):
        view = AreasEspeciaisView()
        embed = discord.Embed(
            title="🏔️ Exploração de Áreas Especiais",
            description="Selecione a área especial que deseja explorar:",
            color=0x3498db
        )
        embed.add_field(name="❄️ Áreas Disponíveis", value=
            "• **Dragonspine**: Montanha congelada\n"
            "• **Despenhadeiro**: Abismo entre Liyue e Sumeru\n"
            "• **Vale Chenyu**: Vale de mineração em Liyue\n"
            "• **Enkanomiya**: Reino submerso\n"
            "• **Mar Antigo**: Resquícios submarinos\n"
            "• **Vulcão**: Região vulcânica"
        )
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='🌳 Árvores', style=discord.ButtonStyle.primary)
    async def arvores_button(self, interaction, button):
        view = ArvoresView()
        embed = discord.Embed(
            title="🌳 Árvores e Monumentos",
            description="Selecione a árvore ou monumento para upar:",
            color=0x3498db
        )
        embed.add_field(name="🌱 Opções Disponíveis", value=
            "• **Sabugueiro**: Árvore de Dragonspine\n"
            "• **Sakura**: Árvore Sagrada de Inazuma\n"
            "• **Árvore dos Sonhos**: Árvore de Sumeru\n"
            "• **Fonte de Lucine**: Fonte de Fontaine\n"
            "• **Outros Monumentos**: Demais monumentos"
        )
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label='🏆 Reputação', style=discord.ButtonStyle.primary)
    async def reputacao_button(self, interaction, button):
        view = ReputacaoView()
        embed = discord.Embed(
            title="🏆 Níveis de Reputação",
            description="Selecione a região para subir reputação:",
            color=0x3498db
        )
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='↩️ Voltar', style=discord.ButtonStyle.danger)
    async def voltar_button(self, interaction, button):
        view = MenuPrincipalView()
        embed = discord.Embed(
            title="🤖 Dori - Calculadora Genshin Impact", 
            description="Selecione uma categoria abaixo:",
            color=0x00ff00
        )
        embed.add_field(name="📊 Funcionalidades", value="• Serviços de exploração\n• Serviços de personagens\n• Ver seu carrinho de compras", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)

class RegioesView(discord.ui.View):
    """Menu de seleção de regiões para exploração"""
    def __init__(self):
        super().__init__(timeout=300)
        self.add_region_buttons()
    
    def add_region_buttons(self):
        regions = [
            ("Mondstadt", discord.ButtonStyle.primary),
            ("Liyue", discord.ButtonStyle.primary),
            ("Inazuma", discord.ButtonStyle.primary),
            ("Sumeru", discord.ButtonStyle.primary),
            ("Fontaine", discord.ButtonStyle.primary),
            ("Natlan", discord.ButtonStyle.primary),
            ("↩️ Voltar", discord.ButtonStyle.danger)
        ]
        
        for i, (label, style) in enumerate(regions):
            button = discord.ui.Button(label=label, style=style, custom_id=f"region_{label.lower()}" if label != "↩️ Voltar" else "voltar")
            button.callback = self.button_callback
            self.add_item(button)
    
    async def button_callback(self, interaction):
        button_id = interaction.data["custom_id"]
        
        if button_id == "voltar":
            view = ExploracaoView()
            embed = discord.Embed(
                title="🗺️ Serviços de Exploração",
                description="Selecione o tipo de serviço de exploração que deseja:",
                color=0x3498db
            )
            embed.add_field(name="⚙️ Opções Disponíveis", value=
                "• **Regiões**: Exploração de nações principais\n"
                "• **Áreas Específicas**: Exploração de áreas especiais\n"
                "• **Reputação**: Subir níveis de reputação\n"
                "• **Árvores**: Árvores sagradas e monumentos"
            )
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            regiao = button_id.split("_")[1]
            
            # Modal para coletar informações extras
            modal = RegionOptionsModal(regiao)
            await interaction.response.send_modal(modal)

class AreasEspeciaisView(discord.ui.View):
    """Menu de seleção de áreas especiais para exploração"""
    def __init__(self):
        super().__init__(timeout=300)
        self.add_area_buttons()
    
    def add_area_buttons(self):
        areas = [
            ("Dragonspine", discord.ButtonStyle.primary),
            ("Despenhadeiro", discord.ButtonStyle.primary),
            ("Vale Chenyu", discord.ButtonStyle.primary),
            ("Enkanomiya", discord.ButtonStyle.primary),
            ("Mar Antigo", discord.ButtonStyle.primary),
            ("Vulcão", discord.ButtonStyle.primary),
            ("↩️ Voltar", discord.ButtonStyle.danger)
        ]
        
        for i, (label, style) in enumerate(areas):
            button_id = label.lower().replace(' ', '_')
            button = discord.ui.Button(label=label, style=style, custom_id=f"area_{button_id}" if label != "↩️ Voltar" else "voltar")
            button.callback = self.button_callback
            self.add_item(button)
    
    async def button_callback(self, interaction):
        button_id = interaction.data["custom_id"]
        
        if button_id == "voltar":
            view = ExploracaoView()
            embed = discord.Embed(
                title="🗺️ Serviços de Exploração",
                description="Selecione o tipo de serviço de exploração que deseja:",
                color=0x3498db
            )
            embed.add_field(name="⚙️ Opções Disponíveis", value=
                "• **Regiões**: Exploração de nações principais\n"
                "• **Áreas Específicas**: Exploração de áreas especiais\n"
                "• **Reputação**: Subir níveis de reputação\n"
                "• **Árvores**: Árvores sagradas e monumentos"
            )
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            area = button_id.split("_", 1)[1]
            preco = PRECOS_AREAS_ESPECIFICAS.get(area)
            
            if preco:
                # Adicionar ao carrinho
                area_nome = area.replace('_', ' ').title()
                item = {
                    "tipo": "area_especial",
                    "nome": area_nome,
                    "preco": preco,
                    "detalhes": f"Exploração completa"
                }
                
                carrinho = adicionar_ao_carrinho(interaction.user.id, item)
                
                # Mostrar confirmação
                view = ComprarMaisView()
                embed = discord.Embed(
                    title="✅ Item adicionado ao carrinho",
                    description=f"**{area_nome}** foi adicionado ao seu carrinho!",
                    color=0x2ecc71
                )
                embed.add_field(name="💰 Preço", value=f"R$ {preco:.2f}", inline=False)
                embed.add_field(name="🛒 Total do carrinho", value=f"R$ {carrinho['total']:.2f} ({len(carrinho['itens'])} itens)", inline=False)
                
                await interaction.response.edit_message(embed=embed, view=view)

class ArvoresView(discord.ui.View):
    """Menu de seleção de árvores para upgrade"""
    def __init__(self):
        super().__init__(timeout=300)
        self.add_tree_buttons()
    
    def add_tree_buttons(self):
        trees = [
            ("Sabugueiro", discord.ButtonStyle.primary),
            ("Árvore Chenyu", discord.ButtonStyle.primary),
            ("Sakura", discord.ButtonStyle.primary),
            ("Árvore Sonhos", discord.ButtonStyle.primary), 
            ("Lago Pari", discord.ButtonStyle.primary),
            ("Fonte Lucine", discord.ButtonStyle.primary),
            ("↩️ Voltar", discord.ButtonStyle.danger)
        ]
        
        for i, (label, style) in enumerate(trees):
            tree_id = label.lower().replace(' ', '_').replace('árvore_', 'arvore_')
            button = discord.ui.Button(label=label, style=style, custom_id=f"tree_{tree_id}" if label != "↩️ Voltar" else "voltar")
            button.callback = self.button_callback
            self.add_item(button)
    
    async def button_callback(self, interaction):
        button_id = interaction.data["custom_id"]
        
        if button_id == "voltar":
            view = ExploracaoView()
            embed = discord.Embed(
                title="🗺️ Serviços de Exploração",
                description="Selecione o tipo de serviço de exploração que deseja:",
                color=0x3498db
            )
            embed.add_field(name="⚙️ Opções Disponíveis", value=
                "• **Regiões**: Exploração de nações principais\n"
                "• **Áreas Específicas**: Exploração de áreas especiais\n"
                "• **Reputação**: Subir níveis de reputação\n"
                "• **Árvores**: Árvores sagradas e monumentos"
            )
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            arvore = button_id.split("_", 1)[1]
            # Modal para coletar informações extras
            modal = ArvoreOptionsModal(arvore)
            await interaction.response.send_modal(modal)

class ReputacaoView(discord.ui.View):
    """Menu de seleção de região para reputação"""
    def __init__(self):
        super().__init__(timeout=300)
        self.add_reputation_buttons()
    
    def add_reputation_buttons(self):
        regions = [
            ("Mondstadt", discord.ButtonStyle.primary),
            ("Liyue", discord.ButtonStyle.primary),
            ("Inazuma", discord.ButtonStyle.primary),
            ("Sumeru", discord.ButtonStyle.primary),
            ("Fontaine", discord.ButtonStyle.primary),
            ("Natlan", discord.ButtonStyle.primary),
            ("↩️ Voltar", discord.ButtonStyle.danger)
        ]
        
        for i, (label, style) in enumerate(regions):
            button = discord.ui.Button(label=label, style=style, custom_id=f"rep_{label.lower()}" if label != "↩️ Voltar" else "voltar")
            button.callback = self.button_callback
            self.add_item(button)
    
    async def button_callback(self, interaction):
        button_id = interaction.data["custom_id"]
        
        if button_id == "voltar":
            view = ExploracaoView()
            embed = discord.Embed(
                title="🗺️ Serviços de Exploração",
                description="Selecione o tipo de serviço de exploração que deseja:",
                color=0x3498db
            )
            embed.add_field(name="⚙️ Opções Disponíveis", value=
                "• **Regiões**: Exploração de nações principais\n"
                "• **Áreas Específicas**: Exploração de áreas especiais\n"
                "• **Reputação**: Subir níveis de reputação\n"
                "• **Árvores**: Árvores sagradas e monumentos"
            )
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            regiao = button_id.split("_")[1]
            # Modal para coletar informações extras
            modal = ReputacaoOptionsModal(regiao)
            await interaction.response.send_modal(modal)

class PersonagensView(discord.ui.View):
    """Menu de serviços de personagens"""
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='🧙‍♂️ Construção Completa', style=discord.ButtonStyle.primary)
    async def build_button(self, interaction, button):
        # Modal para coletar nome do personagem
        modal = PersonagemBuildModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label='📦 Com Itens Coletados', style=discord.ButtonStyle.primary)
    async def itens_button(self, interaction, button):
        # Modal para coletar nome do personagem e itens
        modal = PersonagemItensModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label='↩️ Voltar', style=discord.ButtonStyle.danger)
    async def voltar_button(self, interaction, button):
        view = MenuPrincipalView()
        embed = discord.Embed(
            title="🤖 Dori - Calculadora Genshin Impact", 
            description="Selecione uma categoria abaixo:",
            color=0x00ff00
        )
        embed.add_field(name="📊 Funcionalidades", value="• Serviços de exploração\n• Serviços de personagens\n• Ver seu carrinho de compras", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)

class CarrinhoView(discord.ui.View):
    """Menu de gerenciamento do carrinho"""
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='🛍️ Continuar Comprando', style=discord.ButtonStyle.primary)
    async def continuar_button(self, interaction, button):
        view = MenuPrincipalView()
        embed = discord.Embed(
            title="🤖 Dori - Calculadora Genshin Impact", 
            description="Selecione uma categoria abaixo:",
            color=0x00ff00
        )
        embed.add_field(name="📊 Funcionalidades", value="• Serviços de exploração\n• Serviços de personagens\n• Ver seu carrinho de compras", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='💰 Finalizar Compra', style=discord.ButtonStyle.success)
    async def finalizar_button(self, interaction, button):
        carrinho = obter_carrinho(interaction.user.id)
        
        if not carrinho["itens"]:
            embed = discord.Embed(
                title="❌ Erro",
                description="Seu carrinho está vazio!",
                color=0xe74c3c
            )
            await interaction.response.edit_message(embed=embed, view=self)
            return
        
        embed = discord.Embed(
            title="✅ Compra finalizada!",
            description=f"Obrigado por comprar com a Dori! Um atendente entrará em contato em breve.",
            color=0x2ecc71
        )
        embed.add_field(name="📋 Resumo do pedido", value=gerar_resumo_pedido(carrinho), inline=False)
        embed.add_field(name="💰 Total", value=f"R$ {carrinho['total']:.2f}", inline=False)
        embed.set_footer(text=f"Pedido feito por {interaction.user.name} • {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        # Limpa o carrinho após a compra
        limpar_carrinho(interaction.user.id)
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label='🗑️ Limpar Carrinho', style=discord.ButtonStyle.danger)
    async def limpar_button(self, interaction, button):
        limpar_carrinho(interaction.user.id)
        
        embed = discord.Embed(
            title="🗑️ Carrinho limpo",
            description="Todos os itens foram removidos do seu carrinho.",
            color=0xe74c3c
        )
        
        view = MenuPrincipalView()
        await interaction.response.edit_message(embed=embed, view=view)

class ComprarMaisView(discord.ui.View):
    """Menu após adicionar item ao carrinho"""
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label='🛍️ Continuar Comprando', style=discord.ButtonStyle.primary)
    async def continuar_button(self, interaction, button):
        view = MenuPrincipalView()
        embed = discord.Embed(
            title="🤖 Dori - Calculadora Genshin Impact", 
            description="Selecione uma categoria abaixo:",
            color=0x00ff00
        )
        embed.add_field(name="📊 Funcionalidades", value="• Serviços de exploração\n• Serviços de personagens\n• Ver seu carrinho de compras", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label='🛒 Ver Carrinho', style=discord.ButtonStyle.secondary)
    async def carrinho_button(self, interaction, button):
        carrinho = obter_carrinho(interaction.user.id)
        
        view = CarrinhoView()
        embed = gerar_embed_carrinho(carrinho)
        await interaction.response.edit_message(embed=embed, view=view)

# Classes de modais para coletar informações adicionais
class RegionOptionsModal(discord.ui.Modal, title="Opções de Exploração"):
    def __init__(self, regiao):
        super().__init__()
        self.regiao = regiao
        
    exploracao = discord.ui.TextInput(
        label='Porcentagem atual de exploração (0-80)',
        placeholder='Digite um valor entre 0 e 80',
        required=True,
        min_length=1,
        max_length=2
    )
    
    bussola = discord.ui.TextInput(
        label='Possui a bússola? (sim/não)',
        placeholder='Digite sim ou não',
        required=True,
        min_length=2,
        max_length=3
    )
    
    async def on_submit(self, interaction):
        try:
            porcentagem = int(self.exploracao.value)
            tem_bussola = self.bussola.value.lower() == "sim"
            
            if porcentagem < 0 or porcentagem > 80:
                raise ValueError("Porcentagem deve estar entre 0 e 80")
            
            preco = calcular_preco_regiao(self.regiao, tem_bussola, porcentagem)
            
            if preco:
                # Adicionar ao carrinho
                regiao_nome = self.regiao.title()
                item = {
                    "tipo": "regiao",
                    "nome": regiao_nome,
                    "preco": preco,
                    "detalhes": f"Exploração: {porcentagem}% | Bússola: {'Sim' if tem_bussola else 'Não'}"
                }
                
                carrinho = adicionar_ao_carrinho(interaction.user.id, item)
                
                # Mostrar confirmação
                view = ComprarMaisView()
                embed = discord.Embed(
                    title="✅ Item adicionado ao carrinho",
                    description=f"**Exploração de {regiao_nome}** foi adicionada ao seu carrinho!",
                    color=0x2ecc71
                )
                embed.add_field(name="🗺️ Detalhes", value=f"Exploração atual: {porcentagem}%\nBússola: {'Sim ✅' if tem_bussola else 'Não ❌'}", inline=False)
                embed.add_field(name="💰 Preço", value=f"R$ {preco:.2f}", inline=False)
                embed.add_field(name="🛒 Total do carrinho", value=f"R$ {carrinho['total']:.2f} ({len(carrinho['itens'])} itens)", inline=False)
                
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                await interaction.response.edit_message(content="Erro ao calcular preço da região.", view=None)
        
        except ValueError:
            await interaction.response.send_message("Por favor, insira valores válidos!", ephemeral=True)

class ArvoreOptionsModal(discord.ui.Modal, title="Opções da Árvore"):
    def __init__(self, arvore):
        super().__init__()
        self.arvore = arvore
        
    niveis = discord.ui.TextInput(
        label='Quantidade de níveis para upar',
        placeholder='Digite a quantidade de níveis',
        required=True,
        min_length=1,
        max_length=2
    )
    
    exploracao_completa = discord.ui.TextInput(
        label='Exploração completa? (sim/não)',
        placeholder='Digite sim ou não',
        required=True,
        min_length=2,
        max_length=3
    )
    
    async def on_submit(self, interaction):
        try:
            niveis = int(self.niveis.value)
            exploracao_completa = self.exploracao_completa.value.lower() == "sim"
            
            if niveis <= 0:
                raise ValueError("A quantidade de níveis deve ser maior que zero")
            
            preco = calcular_preco_arvore(self.arvore, niveis, exploracao_completa)
            
            if preco:
                # Adicionar ao carrinho
                arvore_nome = self.arvore.replace('_', ' ').title()
                item = {
                    "tipo": "arvore",
                    "nome": arvore_nome,
                    "preco": preco,
                    "detalhes": f"{niveis} níveis | Exploração completa: {'Sim' if exploracao_completa else 'Não'}"
                }
                
                carrinho = adicionar_ao_carrinho(interaction.user.id, item)
                
                # Mostrar confirmação
                view = ComprarMaisView()
                embed = discord.Embed(
                    title="✅ Item adicionado ao carrinho",
                    description=f"**Upgrade de {arvore_nome}** foi adicionado ao seu carrinho!",
                    color=0x2ecc71
                )
                embed.add_field(name="🌳 Detalhes", value=f"Níveis: {niveis}\nExploração completa: {'Sim ✅' if exploracao_completa else 'Não ❌'}", inline=False)
                embed.add_field(name="💰 Preço", value=f"R$ {preco:.2f}", inline=False)
                embed.add_field(name="🛒 Total do carrinho", value=f"R$ {carrinho['total']:.2f} ({len(carrinho['itens'])} itens)", inline=False)
                
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                await interaction.response.edit_message(content="Erro ao calcular preço da árvore.", view=None)
        
        except ValueError:
            await interaction.response.send_message("Por favor, insira valores válidos!", ephemeral=True)

class ReputacaoOptionsModal(discord.ui.Modal, title="Níveis de Reputação"):
    def __init__(self, regiao):
        super().__init__()
        self.regiao = regiao
        
    niveis = discord.ui.TextInput(
        label='Quantidade de níveis para upar',
        placeholder='Digite a quantidade de níveis',
        required=True,
        min_length=1,
        max_length=2
    )
    
    async def on_submit(self, interaction):
        try:
            niveis = int(self.niveis.value)
            
            if niveis <= 0:
                raise ValueError("A quantidade de níveis deve ser maior que zero")
            
            preco_por_nivel = PRECOS_REPUTACAO.get(self.regiao.lower())
            if not preco_por_nivel:
                await interaction.response.send_message(f"Região {self.regiao} não encontrada.", ephemeral=True)
                return
                
            preco_total = niveis * preco_por_nivel
            
            # Adicionar ao carrinho
            regiao_nome = self.regiao.title()
            item = {
                "tipo": "reputacao",
                "nome": f"Reputação de {regiao_nome}",
                "preco": preco_total,
                "detalhes": f"{niveis} níveis"
            }
            
            carrinho = adicionar_ao_carrinho(interaction.user.id, item)
            
            # Mostrar confirmação
            view = ComprarMaisView()
            embed = discord.Embed(
                title="✅ Item adicionado ao carrinho",
                description=f"**Reputação de {regiao_nome}** foi adicionada ao seu carrinho!",
                color=0x2ecc71
            )
            embed.add_field(name="🏆 Detalhes", value=f"{niveis} níveis de reputação", inline=False)
            embed.add_field(name="💰 Preço", value=f"R$ {preco_total:.2f}", inline=False)
            embed.add_field(name="🛒 Total do carrinho", value=f"R$ {carrinho['total']:.2f} ({len(carrinho['itens'])} itens)", inline=False)
            
            await interaction.response.edit_message(embed=embed, view=view)
        
        except ValueError:
            await interaction.response.send_message("Por favor, insira valores válidos!", ephemeral=True)

class PersonagemBuildModal(discord.ui.Modal, title="Construção de Personagem"):
    nome = discord.ui.TextInput(
        label='Nome do personagem',
        placeholder='Ex: Kazuha, Bennett, Furina',
        required=True
    )
    
    async def on_submit(self, interaction):
        nome_personagem = self.nome.value.lower()
        resultado = calcular_preco_personagem(nome_personagem)
        
        if resultado:
            preco, info = resultado
            
            # Adicionar ao carrinho
            nome_formatado = nome_personagem.title()
            item = {
                "tipo": "personagem",
                "nome": nome_formatado,
                "preco": preco,
                "detalhes": info
            }
            
            carrinho = adicionar_ao_carrinho(interaction.user.id, item)
            
            # Mostrar confirmação
            view = ComprarMaisView()
            embed = discord.Embed(
                title="✅ Item adicionado ao carrinho",
                description=f"**Construção de {nome_formatado}** foi adicionado ao seu carrinho!",
                color=0x2ecc71
            )
            embed.add_field(name="⚔️ Detalhes", value=info, inline=False)
            embed.add_field(name="💰 Preço", value=f"R$ {preco:.2f}", inline=False)
            embed.add_field(name="🛒 Total do carrinho", value=f"R$ {carrinho['total']:.2f} ({len(carrinho['itens'])} itens)", inline=False)
            
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(f"Personagem '{self.nome.value}' não encontrado no banco de dados.", ephemeral=True)

class PersonagemItensModal(discord.ui.Modal, title="Construção com Itens"):
    nome = discord.ui.TextInput(
        label='Nome do personagem',
        placeholder='Ex: Kazuha, Bennett, Furina',
        required=True
    )
    
    itens_cinza = discord.ui.TextInput(
        label='Itens cinza (comum)',
        placeholder='Quantidade (0 se não tiver)',
        required=False,
        default="0"
    )
    
    itens_verde = discord.ui.TextInput(
        label='Itens verde (incomum)',
        placeholder='Quantidade (0 se não tiver)',
        required=False,
        default="0"
    )
    
    itens_boss = discord.ui.TextInput(
        label='Itens de boss',
        placeholder='Quantidade (0 se não tiver)',
        required=False,
        default="0"
    )
    
    itens_coleta = discord.ui.TextInput(
        label='Itens de coleta',
        placeholder='Quantidade (0 se não tiver)',
        required=False,
        default="0"
    )
    
    async def on_submit(self, interaction):
        try:
            nome_personagem = self.nome.value.lower()
            cinza = int(self.itens_cinza.value or "0")
            verde = int(self.itens_verde.value or "0")
            boss = int(self.itens_boss.value or "0")
            coleta = int(self.itens_coleta.value or "0")
            
            itens = {
                'cinza': cinza,
                'verde': verde,
                'boss': boss,
                'coleta': coleta
            }
            
            # Remove itens com quantidade 0
            itens = {k: v for k, v in itens.items() if v > 0}
            
            resultado = calcular_preco_personagem(nome_personagem, itens if itens else None)
            
            if resultado:
                preco, info = resultado
                
                # Adicionar ao carrinho
                nome_formatado = nome_personagem.title()
                item = {
                    "tipo": "personagem_itens",
                    "nome": nome_formatado,
                    "preco": preco,
                    "detalhes": f"{info} | Com itens coletados"
                }
                
                carrinho = adicionar_ao_carrinho(interaction.user.id, item)
                
                # Mostrar confirmação
                view = ComprarMaisView()
                embed = discord.Embed(
                    title="✅ Item adicionado ao carrinho",
                    description=f"**Construção de {nome_formatado} com itens** foi adicionado ao seu carrinho!",
                    color=0x2ecc71
                )
                
                itens_texto = []
                for tipo, qtd in itens.items():
                    if qtd > 0:
                        itens_texto.append(f"• {qtd}x {tipo}")
                
                embed.add_field(name="⚔️ Detalhes", value=info, inline=False)
                embed.add_field(name="📦 Itens coletados", value="\n".join(itens_texto) if itens_texto else "Nenhum", inline=False)
                embed.add_field(name="💰 Preço", value=f"R$ {preco:.2f}", inline=False)
                embed.add_field(name="🛒 Total do carrinho", value=f"R$ {carrinho['total']:.2f} ({len(carrinho['itens'])} itens)", inline=False)
                
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                await interaction.response.send_message(f"Personagem '{self.nome.value}' não encontrado no banco de dados.", ephemeral=True)
        
        except ValueError:
            await interaction.response.send_message("Por favor, insira valores válidos para as quantidades!", ephemeral=True)

# Funções auxiliares para o carrinho
def gerar_embed_carrinho(carrinho):
    """Gera um embed para exibir o carrinho"""
    if not carrinho["itens"]:
        return discord.Embed(
            title="🛒 Seu carrinho está vazio",
            description="Adicione itens ao seu carrinho primeiro.",
            color=0xe74c3c
        )
    
    embed = discord.Embed(
        title="🛒 Seu carrinho de compras",
        description=f"Você tem {len(carrinho['itens'])} itens no seu carrinho.",
        color=0x3498db
    )
    
    embed.add_field(name="📋 Itens", value=gerar_resumo_pedido(carrinho), inline=False)
    embed.add_field(name="💰 Total", value=f"R$ {carrinho['total']:.2f}", inline=False)
    
    return embed

def gerar_resumo_pedido(carrinho):
    """Gera um resumo textual do pedido"""
    itens = carrinho["itens"]
    
    # Agrupar itens por tipo
    itens_por_tipo = {}
    for item in itens:
        tipo = item["tipo"]
        if tipo not in itens_por_tipo:
            itens_por_tipo[tipo] = []
        itens_por_tipo[tipo].append(item)
    
    resumo = []
    
    # Para cada tipo, gerar um resumo
    for tipo, lista_itens in itens_por_tipo.items():
        if tipo == "regiao":
            regioes = [f"{item['nome']} ({item['detalhes']})" for item in lista_itens]
            resumo.append(f"🗺️ **Exploração de regiões**:\n• " + "\n• ".join(regioes))
        
        elif tipo == "area_especial":
            areas = [f"{item['nome']} ({item['preco']:.2f} R$)" for item in lista_itens]
            resumo.append(f"🏔️ **Áreas especiais**:\n• " + "\n• ".join(areas))
        
        elif tipo == "arvore":
            arvores = [f"{item['nome']} - {item['detalhes']} ({item['preco']:.2f} R$)" for item in lista_itens]
            resumo.append(f"🌳 **Árvores/Monumentos**:\n• " + "\n• ".join(arvores))
        
        elif tipo == "reputacao":
            reputacoes = [f"{item['nome']} - {item['detalhes']} ({item['preco']:.2f} R$)" for item in lista_itens]
            resumo.append(f"🏆 **Reputações**:\n• " + "\n• ".join(reputacoes))
        
        elif tipo in ["personagem", "personagem_itens"]:
            personagens = [f"{item['nome']} - {item['detalhes']} ({item['preco']:.2f} R$)" for item in lista_itens]
            resumo.append(f"⚔️ **Personagens**:\n• " + "\n• ".join(personagens))
    
    return "\n\n".join(resumo) if resumo else "Nenhum item no carrinho."

@bot.tree.command(name="dori", description="🤖 Calculadora de preços Genshin Impact - Menu principal")
async def dori_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Dori - Calculadora Genshin Impact", 
        description="Selecione uma categoria abaixo:",
        color=0x00ff00
    )
    embed.add_field(name="📊 Funcionalidades", value="• Serviços de exploração\n• Serviços de personagens\n• Ver seu carrinho de compras", inline=False)
    
    view = MenuPrincipalView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="carrinho", description="🛒 Ver seu carrinho de compras atual")
async def carrinho_slash(interaction: discord.Interaction):
    carrinho = obter_carrinho(interaction.user.id)
    
    if not carrinho["itens"]:
        embed = discord.Embed(
            title="🛒 Seu carrinho está vazio",
            description="Adicione itens ao seu carrinho primeiro.",
            color=0xe74c3c
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    view = CarrinhoView()
    embed = gerar_embed_carrinho(carrinho)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="limpar_carrinho", description="🗑️ Limpar seu carrinho de compras")
async def limpar_carrinho_slash(interaction: discord.Interaction):
    limpar_carrinho(interaction.user.id)
    
    embed = discord.Embed(
        title="🗑️ Carrinho limpo",
        description="Todos os itens foram removidos do seu carrinho.",
        color=0xe74c3c
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="sync", description="🔄 Sincronizar comandos slash (apenas para administradores)")
@app_commands.default_permissions(administrator=True)
async def sync_commands(interaction: discord.Interaction):
    try:
        synced = await bot.tree.sync()
        await interaction.response.send_message(f"✅ Sincronizados {len(synced)} comandos!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao sincronizar comandos: {e}", ephemeral=True)

# Tratamento de erros
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"⏳ Comando em cooldown! Tente novamente em {error.retry_after:.1f}s", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Erro ao executar comando: {error}", ephemeral=True)
        print(f"Erro no comando {interaction.command.name}: {error}")

# Roda o bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("⚠️ Token não encontrado! Configure a variável DISCORD_TOKEN no arquivo .env")