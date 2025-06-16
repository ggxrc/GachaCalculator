PRECOS = {
    "exploracao_regiao_principal": {
        "Mondstadt": {"base": 50.00, "por_area_nao_100": 5.00, "bussola_desconto": 0.10, "reputacao_por_lvl": 2.00, "estatua_por_lvl": 1.00},
        "Liyue": {"base": 60.00, "por_area_nao_100": 6.00, "bussola_desconto": 0.10, "reputacao_por_lvl": 2.00, "estatua_por_lvl": 1.00},
        "Inazuma": {"base": 80.00, "por_area_nao_100": 8.00, "bussola_desconto": 0.10, "reputacao_por_lvl": 2.50, "estatua_por_lvl": 1.20},
        "Sumeru": {"base": 100.00, "por_area_nao_100": 10.00, "bussola_desconto": 0.10, "reputacao_por_lvl": 3.00, "estatua_por_lvl": 1.50},
        "Fontaine": {"base": 120.00, "por_area_nao_100": 12.00, "bussola_desconto": 0.10, "reputacao_por_lvl": 3.50, "estatua_por_lvl": 1.80},
        "Natlan": {"base": 90.00, "por_area_nao_100": 9.00, "bussola_desconto": 0.10, "reputacao_por_lvl": 2.80, "estatua_por_lvl": 1.40} # Natlan incompleta
    },
    "exploracao_regiao_extra": {
        "Espinha do Dragao": 30.00,
        "Abismo": 40.00,
        "Enkanomiya": 45.00,
        "Mar Antigo": 50.00,
        "Vale Chenyu": 55.00, 
        "Montanha Sagrada Antiga": 40.00
    },
    "upar_arvore_sistema": {
        "Graca da Sakura Sagrada": 2.00,  # Preço por nível
        "Arvore dos Sonhos": 2.50,
        "Fonte de Lucine": 2.80,
        "Chama de Tona": 2.20,
        "Arvore do Sabugueiro": 1.50,
        "Lumen da Pedra": 1.80,
        "Chuva de Jade": 2.00
    },
    "farm_chefe": 0.50,  # Preço por material de chefe (por exemplo, 0.50 por material)
    "build_personagem": {
        "nivel_personagem_por_lvl": 0.80, # Por nível de personagem
        "talento_por_lvl": 5.00,        # Por nível de talento (para cada um dos 3 talentos)
        "farm_artefato_por_resina": 0.10, # Valor por resina gasta em domínios de artefatos
        "upgrade_artefato_por_20": 10.00, # Valor para upar um artefato para +20
        "arma_nivel_por_lvl": 0.50,      # Por nível de arma
        "farm_material_comum_por_item": 0.05, # Preço por material comum (flores, inimigos)
        "otimizacao_build_fixo": 30.00  # Valor fixo para otimização de build
    }
}

# --- FUNÇÕES DO PROGRAMA ---
def calcular_exploracao_regiao_principal(regiao_escolhida, progresso_geral, usou_bussola, lvl_estatua_atual, lvl_reputacao_atual):
    """
    Calcula o valor da exploração de uma região principal.
    Recebe os dados como parâmetros e retorna o valor calculado.
    """
    if regiao_escolhida not in PRECOS["exploracao_regiao_principal"]:
        raise ValueError(f"Região '{regiao_escolhida}' não encontrada nos preços.")

    detalhes_regiao = PRECOS["exploracao_regiao_principal"][regiao_escolhida]
    valor_total = detalhes_regiao["base"]

    # Ajuste por progresso atual
    valor_total = valor_total * (progresso_geral / 100)

    # Bússola de exploração
    if usou_bussola.lower() == 's':
        desconto = valor_total * detalhes_regiao["bussola_desconto"]
        valor_total -= desconto

    # Nível da Estátua dos Sete (até Nv 10)
    if lvl_estatua_atual < 10:
        custo_estatua = (10 - lvl_estatua_atual) * detalhes_regiao["estatua_por_lvl"]
        valor_total += custo_estatua

    # Nível de Reputação da Cidade (até Nv 10)
    if lvl_reputacao_atual < 10:
        custo_reputacao = (10 - lvl_reputacao_atual) * detalhes_regiao["reputacao_por_lvl"]
        valor_total += custo_reputacao

    return valor_total

def calcular_exploracao_regiao_extra(regiao_escolhida):
    """
    Calcula o valor da exploração de uma região extra.
    Recebe a região como parâmetro e retorna o valor calculado.
    """
    if regiao_escolhida not in PRECOS["exploracao_regiao_extra"]:
        raise ValueError(f"Região extra '{regiao_escolhida}' não encontrada nos preços.")

    valor_total = PRECOS["exploracao_regiao_extra"][regiao_escolhida]
    return valor_total

def calcular_upar_arvore_sistema(sistema_escolhido, lvl_inicial, lvl_final):
    """
    Calcula o valor para upar árvores/sistemas de oferenda.
    Recebe o sistema e os níveis como parâmetros e retorna o valor calculado.
    """
    if sistema_escolhido not in PRECOS["upar_arvore_sistema"]:
        raise ValueError(f"Sistema '{sistema_escolhido}' não encontrado nos preços.")
    if lvl_final < lvl_inicial:
        raise ValueError("Nível final não pode ser menor que o nível inicial.")

    preco_por_lvl = PRECOS["upar_arvore_sistema"][sistema_escolhido]
    niveis_a_upar = lvl_final - lvl_inicial
    valor_total = niveis_a_upar * preco_por_lvl
    return valor_total

def calcular_farm_chefe(qtd_atual, qtd_desejada):
    """
    Calcula o valor para farmar materiais de chefe.
    Recebe as quantidades como parâmetros e retorna o valor calculado.
    """
    if qtd_desejada < qtd_atual:
        raise ValueError("Quantidade desejada não pode ser menor que a quantidade atual.")

    materiais_a_farmar = qtd_desejada - qtd_atual
    valor_total = materiais_a_farmar * PRECOS.get("farm_chefe", 0.0)
    return valor_total

def calcular_build_personagem(
    lvl_personagem_inicial, lvl_personagem_final,
    niveis_talento_total=0, # Níveis total a upar para *todos* os talentos (ex: 3 talentos * 10 níveis = 30)
    resina_artefatos_gasta=0, # Em múltiplos de 20
    qtd_artefatos_20=0,
    lvl_arma_inicial=0, lvl_arma_final=0,
    qtd_materiais_comuns=0,
    incluir_otimizacao_build=False
):
    """
    Calcula o valor para buildar um personagem.
    Recebe os parâmetros e retorna o valor calculado.
    """
    valor_total = 0.0
    precos_build = PRECOS.get("build_personagem", {})

    if lvl_personagem_final < lvl_personagem_inicial:
        raise ValueError("Nível final do personagem não pode ser menor que o nível inicial.")
    valor_total += (lvl_personagem_final - lvl_personagem_inicial) * precos_build.get("nivel_personagem_por_lvl", 0.0)

    # Níveis de Talento (total de níveis para *todos* os talentos juntos)
    valor_total += niveis_talento_total * precos_build.get("talento_por_lvl", 0.0)

    # Farm de Artefatos
    if resina_artefatos_gasta % 20 != 0:
        raise ValueError("Resina gasta em artefatos deve ser um múltiplo de 20.")
    valor_total += resina_artefatos_gasta * precos_build.get("farm_artefato_por_resina", 0.0)

    # Upar Artefato para +20
    valor_total += qtd_artefatos_20 * precos_build.get("upgrade_artefato_por_20", 0.0)

    # Upar Nível de Arma
    if lvl_arma_final < lvl_arma_inicial:
        raise ValueError("Nível final da arma não pode ser menor que o nível inicial.")
    valor_total += (lvl_arma_final - lvl_arma_inicial) * precos_build.get("arma_nivel_por_lvl", 0.0)

    # Farmar Materiais Comuns
    valor_total += qtd_materiais_comuns * precos_build.get("farm_material_comum_por_item", 0.0)

    # Otimização de Build (valor fixo)
    if incluir_otimizacao_build:
        valor_total += precos_build.get("otimizacao_build_fixo", 0.0)

    return valor_total