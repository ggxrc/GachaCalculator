import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext # Importa módulos necessários para GUI, caixas de mensagem e área de texto com scroll
from reportlab.pdfgen import canvas # Para gerar documentos PDF
from reportlab.lib.pagesizes import A4 # Para definir o tamanho da página do PDF
from datetime import datetime # Para obter a data e hora atual para nomes de arquivo e registro

# Importa os preços e funções de cálculo do seu arquivo genshin_calculator.py.
# É crucial que 'genshin_calculator.py' esteja no mesmo diretório,
# não tenha erros de sintaxe na linha 1 e não execute código diretamente (sem o bloco main()).
try:
    from genshin_calculator import PRECOS, \
                                   calcular_exploracao_regiao_principal, \
                                   calcular_exploracao_regiao_extra, \
                                   calcular_upar_arvore_sistema, \
                                   calcular_farm_chefe, \
                                   calcular_build_personagem
except ImportError as e:
    # Exibe uma mensagem de erro se o arquivo de preços não puder ser importado
    messagebox.showerror("Erro de Importação", f"Não foi possível importar os dados de 'genshin_calculator.py'.\nVerifique se o arquivo existe e não tem erros de sintaxe na linha 1, e se o bloco main() foi removido/comentado.\nErro: {e}")
    # Define PRECOS como um dicionário vazio para evitar erros posteriores, mas a funcionalidade será limitada.
    PRECOS = {}

# Variável global para acumular o total geral dos serviços adicionados ao carrinho
total_geral_gui = 0.0

# O Carrinho: Uma lista global para armazenar cada item de serviço adicionado.
# Cada item é um dicionário com "servico", "detalhes" e "valor".
carrinho = []

# Variáveis globais para os widgets que precisam ser acessados e atualizados por diferentes funções.
total_label = None # Label que exibe o total geral na interface
root = None # A janela principal do Tkinter, tornada global para acesso por 'nametowidget'


def exibir_resultado(valor, tipo_servico, detalhes_servico):
    """
    Adiciona um serviço ao carrinho, atualiza o total geral e exibe uma mensagem de confirmação.
    """
    global total_geral_gui
    global carrinho

    # Cria um dicionário para o item do carrinho
    item_carrinho = {
        "servico": tipo_servico,
        "detalhes": detalhes_servico,
        "valor": valor
    }
    carrinho.append(item_carrinho) # Adiciona o item à lista do carrinho

    total_geral_gui += valor # Soma o valor ao total geral
    atualizar_total_geral_label() # Chama a função para atualizar o texto do label do total

    # Exibe uma caixa de mensagem com os detalhes do item adicionado e o total acumulado
    messagebox.showinfo("Item Adicionado ao Carrinho",
                        f"Serviço: {tipo_servico}\n"
                        f"Detalhes: {detalhes_servico}\n"
                        f"Valor: R$ {valor:.2f}\n"
                        f"Total acumulado no carrinho: R$ {total_geral_gui:.2f}")

def atualizar_total_geral_label():
    """
    Atualiza o texto do Label que mostra o total geral na interface.
    """
    if total_label: # Verifica se o label já foi criado (evita erro no início do programa)
        total_label.config(text=f"Total Geral: R$ {total_geral_gui:.2f}")

def limpar_conteudo_dinamico(frame):
    """
    Remove todos os widgets filhos de um dado frame, limpando sua área.
    Usado para alternar entre as seções de cálculo.
    """
    for widget in frame.winfo_children(): # Itera sobre todos os widgets dentro do frame
        widget.destroy() # Destroi cada widget

# --- Funções para criar as seções de cálculo específicas na interface ---
def criar_secao_exploracao_principal(parent_frame):
    """
    Cria e exibe a interface para cálculo de Exploração de Região Principal.
    """
    limpar_conteudo_dinamico(parent_frame) # Limpa a área de conteúdo dinâmico

    # Cria um novo frame para esta seção, com padding e estilo
    secao_frame = ttk.Frame(parent_frame, padding="10", style='Content.TFrame')
    secao_frame.pack(fill=tk.BOTH, expand=True) # Empacota o frame para preencher o espaço

    # Título da seção
    ttk.Label(secao_frame, text="Exploração de Região Principal", style='SectionTitle.TLabel').pack(pady=5)

    # Widget para seleção da Região
    ttk.Label(secao_frame, text="Selecione a Região:", style='TLabel').pack(anchor=tk.W) # Texto
    regioes = list(PRECOS["exploracao_regiao_principal"].keys()) if "exploracao_regiao_principal" in PRECOS else [] # Obtém as regiões dos preços
    regiao_var = tk.StringVar(secao_frame) # Variável para armazenar a seleção da Combobox
    if regioes:
        regiao_var.set(regioes[0]) # Define a primeira região como padrão
    regiao_combobox = ttk.Combobox(secao_frame, textvariable=regiao_var, values=regioes, state="readonly", style='TCombobox') # Combobox (dropdown)
    regiao_combobox.pack(fill=tk.X, pady=2) # Empacota e preenche a largura

    # Campo para Progresso Geral
    ttk.Label(secao_frame, text="Progresso de Exploração Atual (0-100%):", style='TLabel').pack(anchor=tk.W)
    progresso_entry = ttk.Entry(secao_frame, style='TEntry') # Campo de entrada de texto
    progresso_entry.insert(0, "100") # Valor padrão "100"
    progresso_entry.pack(fill=tk.X, pady=2)

    # Checkbox para Bússola de Exploração
    bussola_var = tk.StringVar(secao_frame, value="n") # Variável para armazenar "s" (sim) ou "n" (não)
    ttk.Checkbutton(secao_frame, text="Cliente tem bússola de exploração?", variable=bussola_var, onvalue="s", offvalue="n", style='TCheckbutton').pack(anchor=tk.W, pady=2)

    # Campo para Nível da Estátua dos Sete
    ttk.Label(secao_frame, text="Nível atual da Estátua dos Sete (0-10):", style='TLabel').pack(anchor=tk.W)
    estatua_entry = ttk.Entry(secao_frame, style='TEntry')
    estatua_entry.insert(0, "10") # Valor padrão "10"
    estatua_entry.pack(fill=tk.X, pady=2)

    # Campo para Nível de Reputação da Cidade
    ttk.Label(secao_frame, text="Nível atual de Reputação da Cidade (0-10):", style='TLabel').pack(anchor=tk.W)
    reputacao_entry = ttk.Entry(secao_frame, style='TEntry')
    reputacao_entry.insert(0, "10") # Valor padrão "10"
    reputacao_entry.pack(fill=tk.X, pady=2)

    def adicionar_ao_carrinho():
        """
        Função chamada ao clicar no botão "Adicionar ao Carrinho" nesta seção.
        Coleta os dados, chama a função de cálculo e adiciona ao carrinho.
        """
        try:
            # Coleta os valores dos widgets
            regiao_selecionada = regiao_var.get()
            progresso = float(progresso_entry.get())
            bussola = bussola_var.get()
            estatua_lvl = int(estatua_entry.get())
            reputacao_lvl = int(reputacao_entry.get())

            # Chama a função de cálculo importada de genshin_calculator.py
            valor = calcular_exploracao_regiao_principal(
                regiao_selecionada, progresso, bussola, estatua_lvl, reputacao_lvl
            )
            # Monta a string de detalhes para o carrinho e PDF
            detalhes = (f"{regiao_selecionada} ({progresso}%), "
                        f"Bússola: {'Sim' if bussola == 's' else 'Não'}, "
                        f"Estátua Nv: {estatua_lvl}, Rep. Nv: {reputacao_lvl}")
            # Exibe o resultado e adiciona ao carrinho
            exibir_resultado(valor, "Exploração Região Principal", detalhes)
        except ValueError as e:
            # Captura erros de conversão de tipo (ex: texto em campo numérico)
            messagebox.showerror("Erro de Entrada", f"Por favor, insira valores numéricos válidos. Detalhes: {e}")
        except Exception as e:
            # Captura outros erros que podem ocorrer no cálculo
            messagebox.showerror("Erro", f"Ocorreu um erro ao calcular a exploração: {e}")

    # Botão para adicionar o serviço ao carrinho
    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho, style='Action.TButton').pack(pady=10)

def criar_secao_exploracao_extra(parent_frame):
    """
    Cria e exibe a interface para cálculo de Exploração de Região Extra.
    """
    limpar_conteudo_dinamico(parent_frame)

    secao_frame = ttk.Frame(parent_frame, padding="10", style='Content.TFrame')
    secao_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(secao_frame, text="Exploração de Região Extra", style='SectionTitle.TLabel').pack(pady=5)

    ttk.Label(secao_frame, text="Selecione a Região Extra:", style='TLabel').pack(anchor=tk.W)
    regioes_extras = list(PRECOS["exploracao_regiao_extra"].keys()) if "exploracao_regiao_extra" in PRECOS else []
    regiao_extra_var = tk.StringVar(secao_frame)
    if regioes_extras:
        regiao_extra_var.set(regioes_extras[0])
    regiao_extra_combobox = ttk.Combobox(secao_frame, textvariable=regiao_extra_var, values=regioes_extras, state="readonly", style='TCombobox')
    regiao_extra_combobox.pack(fill=tk.X, pady=2)

    def adicionar_ao_carrinho():
        try:
            regiao_selecionada = regiao_extra_var.get()
            # Chama a função de cálculo importada
            valor = calcular_exploracao_regiao_extra(regiao_selecionada)
            detalhes = f"{regiao_selecionada} (100% Exploração)"
            exibir_resultado(valor, "Exploração Região Extra", detalhes)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho, style='Action.TButton').pack(pady=10)

def criar_secao_upar_arvore_sistema(parent_frame):
    """
    Cria e exibe a interface para cálculo de Upar Árvores/Sistemas de Oferenda.
    """
    limpar_conteudo_dinamico(parent_frame)

    secao_frame = ttk.Frame(parent_frame, padding="10", style='Content.TFrame')
    secao_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(secao_frame, text="Upar Árvores/Sistemas de Oferenda", style='SectionTitle.TLabel').pack(pady=5)

    ttk.Label(secao_frame, text="Selecione a Árvore/Sistema:", style='TLabel').pack(anchor=tk.W)
    sistemas = list(PRECOS["upar_arvore_sistema"].keys()) if "upar_arvore_sistema" in PRECOS else []
    sistema_var = tk.StringVar(secao_frame)
    if sistemas:
        sistema_var.set(sistemas[0])
    sistema_combobox = ttk.Combobox(secao_frame, textvariable=sistema_var, values=sistemas, state="readonly", style='TCombobox')
    sistema_combobox.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Nível Inicial:", style='TLabel').pack(anchor=tk.W)
    lvl_inicial_entry = ttk.Entry(secao_frame, style='TEntry')
    lvl_inicial_entry.insert(0, "0")
    lvl_inicial_entry.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Nível Desejado (Máx 50 para Natlan, 12 para Espinha, 10 para Abismo):", style='TLabel').pack(anchor=tk.W)
    lvl_final_entry = ttk.Entry(secao_frame, style='TEntry')
    lvl_final_entry.insert(0, "10")
    lvl_final_entry.pack(fill=tk.X, pady=2)

    def adicionar_ao_carrinho():
        try:
            sistema_selecionado = sistema_var.get()
            lvl_inicial = int(lvl_inicial_entry.get())
            lvl_final = int(lvl_final_entry.get())

            valor = calcular_upar_arvore_sistema(sistema_selecionado, lvl_inicial, lvl_final)
            detalhes = f"{sistema_selecionado} de Nv {lvl_inicial} para Nv {lvl_final}"
            exibir_resultado(valor, "Upar Árvore/Sistema", detalhes)
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Por favor, insira níveis numéricos válidos e verifique a lógica de níveis. Detalhes: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho, style='Action.TButton').pack(pady=10)

def criar_secao_farm_chefe(parent_frame):
    """
    Cria e exibe a interface para cálculo de Farm de Chefes.
    """
    limpar_conteudo_dinamico(parent_frame)

    secao_frame = ttk.Frame(parent_frame, padding="10", style='Content.TFrame')
    secao_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(secao_frame, text="Farm de Chefes", style='SectionTitle.TLabel').pack(pady=5)
    ttk.Label(secao_frame, text=f"Preço por material de chefe: R$ {PRECOS.get('farm_chefe', 0.0):.2f}", style='TLabel').pack(anchor=tk.W)

    ttk.Label(secao_frame, text="Quantidade atual de materiais:", style='TLabel').pack(anchor=tk.W)
    qtd_atual_entry = ttk.Entry(secao_frame, style='TEntry')
    qtd_atual_entry.insert(0, "0")
    qtd_atual_entry.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Quantidade desejada de materiais:", style='TLabel').pack(anchor=tk.W)
    qtd_desejada_entry = ttk.Entry(secao_frame, style='TEntry')
    qtd_desejada_entry.insert(0, "0")
    qtd_desejada_entry.pack(fill=tk.X, pady=2)

    def adicionar_ao_carrinho():
        try:
            qtd_atual = int(qtd_atual_entry.get())
            qtd_desejada = int(qtd_desejada_entry.get())

            valor = calcular_farm_chefe(qtd_atual, qtd_desejada)
            detalhes = f"Farm de {qtd_desejada - qtd_atual} materiais"
            exibir_resultado(valor, "Farm de Chefes", detalhes)
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Por favor, insira quantidades numéricas válidas. Detalhes: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho, style='Action.TButton').pack(pady=10)

def criar_secao_build_personagem(parent_frame):
    """
    Cria e exibe a interface para cálculo de Build de Personagem.
    """
    limpar_conteudo_dinamico(parent_frame)

    secao_frame = ttk.Frame(parent_frame, padding="10", style='Content.TFrame')
    secao_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(secao_frame, text="Build de Personagem", style='SectionTitle.TLabel').pack(pady=5)

    # Nível do Personagem
    ttk.Label(secao_frame, text="Nível Inicial do Personagem:", style='TLabel').pack(anchor=tk.W)
    lvl_personagem_inicial_entry = ttk.Entry(secao_frame, style='TEntry')
    lvl_personagem_inicial_entry.insert(0, "1")
    lvl_personagem_inicial_entry.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Nível Desejado do Personagem:", style='TLabel').pack(anchor=tk.W)
    lvl_personagem_final_entry = ttk.Entry(secao_frame, style='TEntry')
    lvl_personagem_final_entry.insert(0, "90")
    lvl_personagem_final_entry.pack(fill=tk.X, pady=2)

    # Níveis de Talento (total a upar para *todos* os talentos)
    ttk.Label(secao_frame, text="Total de Níveis de Talento a upar (ex: 3 talentos de 1 para 10 = 27):", style='TLabel').pack(anchor=tk.W)
    niveis_talento_entry = ttk.Entry(secao_frame, style='TEntry')
    niveis_talento_entry.insert(0, "0")
    niveis_talento_entry.pack(fill=tk.X, pady=2)

    # Farm de Artefatos (por resina gasta)
    ttk.Label(secao_frame, text="Resina gasta em Domínios de Artefatos (múltiplos de 20):", style='TLabel').pack(anchor=tk.W)
    resina_artefatos_entry = ttk.Entry(secao_frame, style='TEntry')
    resina_artefatos_entry.insert(0, "0")
    resina_artefatos_entry.pack(fill=tk.X, pady=2)

    # Upar Artefato para +20
    ttk.Label(secao_frame, text="Quantos artefatos para upar para +20:", style='TLabel').pack(anchor=tk.W)
    qtd_artefatos_20_entry = ttk.Entry(secao_frame, style='TEntry') # CORREÇÃO DE SINTAXE AQUI
    qtd_artefatos_20_entry.insert(0, "0")
    qtd_artefatos_20_entry.pack(fill=tk.X, pady=2)

    # Nível de Arma
    ttk.Label(secao_frame, text="Nível Inicial da Arma:", style='TLabel').pack(anchor=tk.W)
    lvl_arma_inicial_entry = ttk.Entry(secao_frame, style='TEntry')
    lvl_arma_inicial_entry.insert(0, "1")
    lvl_arma_inicial_entry.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Nível Desejado da Arma:", style='TLabel').pack(anchor=tk.W)
    lvl_arma_final_entry = ttk.Entry(secao_frame, style='TEntry')
    lvl_arma_final_entry.insert(0, "90")
    lvl_arma_final_entry.pack(fill=tk.X, pady=2)

    # Farm de Materiais Comuns
    ttk.Label(secao_frame, text="Quantidade de Materiais Comuns a farmar:", style='TLabel').pack(anchor=tk.W)
    qtd_materiais_comuns_entry = ttk.Entry(secao_frame, style='TEntry')
    qtd_materiais_comuns_entry.insert(0, "0")
    qtd_materiais_comuns_entry.pack(fill=tk.X, pady=2)

    # Otimização de Build (checkbox)
    otimizacao_build_var = tk.StringVar(secao_frame, value="no")
    ttk.Checkbutton(secao_frame, text=f"Incluir Otimização de Build (R$ {PRECOS.get('build_personagem', {}).get('otimizacao_build_fixo', 0.0):.2f})?", variable=otimizacao_build_var, onvalue="yes", offvalue="no", style='TCheckbutton').pack(anchor=tk.W, pady=5)

    def adicionar_ao_carrinho():
        """
        Função chamada ao clicar no botão "Adicionar ao Carrinho" para Build de Personagem.
        Coleta os dados, chama a função de cálculo e adiciona ao carrinho.
        """
        try:
            # Coleta os valores dos widgets
            lvl_personagem_inicial = int(lvl_personagem_inicial_entry.get())
            lvl_personagem_final = int(lvl_personagem_final_entry.get())
            niveis_talento_total = int(niveis_talento_entry.get())
            resina_artefatos_gasta = int(resina_artefatos_entry.get())
            qtd_artefatos_20 = int(qtd_artefatos_20_entry.get())
            lvl_arma_inicial = int(lvl_arma_inicial_entry.get())
            lvl_arma_final = int(lvl_arma_final_entry.get())
            qtd_materiais_comuns = int(qtd_materiais_comuns_entry.get())
            incluir_otimizacao_build = (otimizacao_build_var.get() == "yes")

            # Chama a função de cálculo importada
            valor = calcular_build_personagem(
                lvl_personagem_inicial, lvl_personagem_final,
                niveis_talento_total,
                resina_artefatos_gasta,
                qtd_artefatos_20,
                lvl_arma_inicial, lvl_arma_final,
                qtd_materiais_comuns,
                incluir_otimizacao_build
            )
            # Monta a string de detalhes para o carrinho e PDF
            detalhes = (f"Personagem Nv {lvl_personagem_inicial}-{lvl_personagem_final}, "
                        f"Talentos Nv: {niveis_talento_total}, "
                        f"Artefatos Res: {resina_artefatos_gasta}, Artefatos +20: {qtd_artefatos_20}, "
                        f"Arma Nv {lvl_arma_inicial}-{lvl_arma_final}, Mat. Comuns: {qtd_materiais_comuns}, "
                        f"Otimização: {'Sim' if incluir_otimizacao_build else 'Não'}")
            # Exibe o resultado e adiciona ao carrinho
            exibir_resultado(valor, "Build de Personagem", detalhes)
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Por favor, insira valores numéricos válidos. Detalhes: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao calcular a build: {e}")

    # Botão para adicionar o serviço ao carrinho
    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho, style='Action.TButton').pack(pady=10)

# --- Nova Seção: Visualizar Carrinho ---
def criar_secao_carrinho(parent_frame):
    """
    Cria e exibe a interface para visualizar o conteúdo do carrinho.
    """
    limpar_conteudo_dinamico(parent_frame) # Limpa a área de conteúdo dinâmico

    carrinho_frame = ttk.Frame(parent_frame, padding="10", style='Content.TFrame')
    carrinho_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(carrinho_frame, text="Conteúdo do Carrinho", style='SectionTitle.TLabel').pack(pady=5)

    if not carrinho: # Se o carrinho estiver vazio
        ttk.Label(carrinho_frame, text="O carrinho está vazio.", style='TLabel').pack(pady=10)
    else:
        # Usa um ScrolledText (área de texto com barra de rolagem) para exibir os itens
        carrinho_text = scrolledtext.ScrolledText(carrinho_frame, wrap=tk.WORD, width=60, height=15, 
                                                  font=("Arial", 10), background="#34495E", 
                                                  foreground="#ECF0F1", insertbackground="white", 
                                                  relief="flat", borderwidth=0) # Estilos para o ScrolledText
        carrinho_text.pack(fill=tk.BOTH, expand=True, pady=10)

        # Adiciona cada item do carrinho ao ScrolledText
        for i, item in enumerate(carrinho):
            carrinho_text.insert(tk.END, f"Item {i+1}:\n")
            carrinho_text.insert(tk.END, f"  Serviço: {item['servico']}\n")
            carrinho_text.insert(tk.END, f"  Detalhes: {item['detalhes']}\n")
            carrinho_text.insert(tk.END, f"  Valor: R$ {item['valor']:.2f}\n")
            carrinho_text.insert(tk.END, "-" * 40 + "\n") # Adiciona um separador
        
        carrinho_text.config(state=tk.DISABLED) # Impede que o usuário edite o texto

    # Exibe o total do carrinho
    ttk.Label(carrinho_frame, text=f"Total do Carrinho: R$ {total_geral_gui:.2f}", style='SectionTitle.TLabel').pack(pady=10)

    # Botões de ação para o carrinho
    ttk.Button(carrinho_frame, text="Gerar PDF do Carrinho", command=gerar_pdf_carrinho, style='Action.TButton').pack(pady=10)
    ttk.Button(carrinho_frame, text="Limpar Carrinho", command=limpar_carrinho, style='Action.TButton').pack(pady=5)

def gerar_pdf_carrinho():
    """
    Gera um arquivo PDF com o resumo do carrinho usando a biblioteca ReportLab.
    """
    if not carrinho: # Se o carrinho estiver vazio, não gera o PDF
        messagebox.showwarning("Carrinho Vazio", "Adicione itens ao carrinho antes de gerar o PDF.")
        return
    
    # Define o nome do arquivo PDF com a data e hora atual
    filename = f"Orcamento_Genshin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    # Cria um objeto Canvas para desenhar no PDF
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4 # Obtém as dimensões da página A4

    y_pos = height - 50 # Posição inicial Y (do topo para baixo)

    # Desenha o título no PDF
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y_pos, "Orçamento de Serviços Genshin Impact")
    y_pos -= 30

    # Desenha a data e hora no PDF
    c.setFont("Helvetica", 10)
    c.drawString(50, y_pos, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    y_pos -= 30

    # Desenha o título da seção de itens
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos, "Itens do Carrinho:")
    y_pos -= 20

    c.setFont("Helvetica", 10)
    # Itera sobre cada item do carrinho e o desenha no PDF
    for i, item in enumerate(carrinho):
        if y_pos < 80: # Verifica se está perto do final da página
            c.showPage() # Inicia uma nova página
            y_pos = height - 50 # Reinicia a posição Y
            c.setFont("Helvetica", 10) # Redefine a fonte para a nova página
        
        c.drawString(60, y_pos, f"Serviço: {item['servico']}")
        y_pos -= 12
        c.drawString(70, y_pos, f"Detalhes: {item['detalhes']}")
        y_pos -= 12
        c.drawString(70, y_pos, f"Valor: R$ {item['valor']:.2f}")
        y_pos -= 15 # Espaço entre os itens

    # Desenha o Total Geral no PDF
    y_pos -= 20
    if y_pos < 80: # Garante que o total não fique cortado no final da página
        c.showPage()
        y_pos = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos, f"TOTAL GERAL: R$ {total_geral_gui:.2f}")

    c.save() # Salva o arquivo PDF
    messagebox.showinfo("PDF Gerado", f"O orçamento foi salvo como:\n{filename}")

def limpar_carrinho():
    """
    Limpa todos os itens do carrinho e redefine o total geral.
    Pede confirmação ao usuário antes de limpar.
    """
    global carrinho
    global total_geral_gui
    
    if messagebox.askyesno("Limpar Carrinho", "Tem certeza que deseja limpar todo o carrinho?"):
        carrinho = [] # Esvazia a lista do carrinho
        total_geral_gui = 0.0 # Zera o total geral
        atualizar_total_geral_label() # Atualiza o label na interface
        
        # Referenciando o conteudo_frame pelo nome que lhe foi dado na criação.
        if root and root.nametowidget("conteudo_frame"):
            limpar_conteudo_dinamico(root.nametowidget("conteudo_frame"))
            # Opcional: recarregar uma tela inicial vazia após o reset
            # criar_secao_inicial(root.nametowidget("conteudo_frame"))
        
        messagebox.showinfo("Carrinho Limpo", "O carrinho foi esvaziado.")

def resetar_total(): # FUNÇÃO resetar_total MOVIDA PARA CIMA DE criar_interface PARA RESOLVER NameError
    """
    Reseta o total geral e limpa todos os itens do carrinho.
    Pede confirmação ao usuário antes de resetar.
    """
    global carrinho
    global total_geral_gui
    
    if messagebox.askyesno("Confirmar Reset", "Tem certeza que deseja resetar o total e limpar o carrinho?"):
        carrinho = [] # Limpa a lista do carrinho
        total_geral_gui = 0.0 # Zera o total geral
        atualizar_total_geral_label() # Atualiza o label na interface
        
        # Referenciando o conteudo_frame pelo nome que lhe foi dado na criação.
        if root and root.nametowidget("conteudo_frame"):
            limpar_conteudo_dinamico(root.nametowidget("conteudo_frame"))
            # Opcional: recarregar uma tela inicial vazia após o reset
            # criar_secao_inicial(root.nametowidget("conteudo_frame"))
        
        messagebox.showinfo("Reset Concluído", "Total geral e carrinho resetados.")

def criar_interface():
    """
    Função principal que configura e inicia a interface gráfica do Tkinter.
    """
    global total_label # Necessário para que a variável global total_label seja atribuída aqui
    global root # Necessário para que a variável global root seja atribuída e acessível


    # 1. Configuração da Janela Principal
    root = tk.Tk() # Cria a janela principal
    root.title("Calculadora de Serviços Genshin Impact") # Define o título da janela
    root.geometry("1000x700") # Define o tamanho inicial da janela (largura x altura)
    root.resizable(True, True) # Permite que o usuário redimensione a janela

    # Adicionar e configurar o estilo ttk para um visual moderno
    style = ttk.Style(root)
    # Experimente outros temas: 'alt', 'default', 'classic', 'vista', 'xpnative' (Windows), 'aqua' (macOS)
    style.theme_use('clam') 

    # --- Definição das Cores e Fontes para a Estilização (Inspiradas no Genshin Impact) ---
    cor_fundo_principal = "#2C3E50" # Azul escuro/cinza (para o painel de botões esquerdo)
    cor_fundo_secundario = "#34495E" # Um pouco mais claro (para a área de conteúdo principal)
    cor_texto_claro = "#ECF0F1"     # Branco acinzentado para a maioria dos textos
    cor_destaque = "#F39C12"        # Laranja/dourado Genshin para títulos e destaques
    cor_botoes_menu = "#1ABC9C"     # Verde água para botões do menu lateral
    cor_botoes_acao = "#3498DB"     # Azul para botões de ação (Adicionar, Gerar PDF)
    cor_reset = "#E74C3C"           # Vermelho para o botão de reset

    # --- Configuração de Estilos para Diferentes Widgets ---
    # Estilos para Frames
    style.configure('TFrame', background=cor_fundo_secundario) # Estilo padrão para todos os ttk.Frame
    style.configure('MainButtons.TFrame', background=cor_fundo_principal) # Estilo específico para o frame dos botões de menu
    style.configure('Content.TFrame', background=cor_fundo_secundario) # Estilo para o frame de conteúdo dinâmico

    # Estilos para Labels (Textos)
    style.configure('TLabel', foreground=cor_texto_claro, background=cor_fundo_secundario, font=("Arial", 10)) # Estilo padrão para ttk.Label
    style.configure('Title.TLabel', foreground=cor_destaque, background=cor_fundo_principal, font=("Arial", 16, "bold")) # Estilo para títulos principais
    style.configure('SectionTitle.TLabel', foreground=cor_destaque, background=cor_fundo_secundario, font=("Arial", 14, "bold")) # Estilo para títulos de seções de cálculo
    style.configure('TotalLabel.TLabel', foreground=cor_destaque, background=cor_fundo_principal, font=("Arial", 12, "bold")) # Estilo para o label do total geral

    # Estilos para Buttons
    style.configure('Menu.TButton', foreground=cor_texto_claro, background=cor_botoes_menu, font=("Arial", 10, "bold"), padding=10)
    style.map('Menu.TButton', background=[('active', cor_destaque)]) # Efeito de cor ao passar o mouse

    style.configure('Action.TButton', foreground=cor_texto_claro, background=cor_botoes_acao, font=("Arial", 10, "bold"), padding=10)
    style.map('Action.TButton', background=[('active', cor_destaque)])

    style.configure('Reset.TButton', foreground=cor_texto_claro, background=cor_reset, font=("Arial", 10, "bold"), padding=10)
    style.map('Reset.TButton', background=[('active', cor_destaque)])

    # Estilos para Combobox (Dropdowns)
    style.configure('TCombobox', fieldbackground='white', background=cor_fundo_secundario, foreground='black')
    style.map('TCombobox', fieldbackground=[('readonly', 'white')], selectbackground=[('readonly', cor_destaque)], selectforeground=[('readonly', 'black')])

    # Estilos para Entry (Campos de Texto)
    style.configure('TEntry', fieldbackground='white', foreground='black', borderwidth=1, relief="solid")

    # Estilos para Checkbutton
    style.configure('TCheckbutton', foreground=cor_texto_claro, background=cor_fundo_secundario, font=("Arial", 10))

    # Estilos para ScrolledText (área de texto com scroll no carrinho)
    # Observação: ScrolledText não é um widget ttk puro, então algumas propriedades de estilo
    # são passadas diretamente na criação do widget em criar_secao_carrinho.
    style.configure('TScrollbar', background=cor_fundo_principal, troughcolor=cor_fundo_secundario)
    style.map('TScrollbar', background=[('active', cor_destaque)])


    # 2. Frame Principal (main_frame): Painel lateral esquerdo com os botões de serviço
    main_frame = ttk.Frame(root, padding="10 10 10 10", style='MainButtons.TFrame')
    main_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False) # Empacota à esquerda, preenche Y, não expande X

    # 3. Frame para o Conteúdo Dinâmico (conteudo_frame): Área principal onde as seções de cálculo aparecem
    # Damos um 'name' para que possa ser referenciado de forma mais robusta em outras funções (ex: limpar_carrinho)
    conteudo_frame = ttk.Frame(root, padding="10 10 10 10", relief=tk.RAISED, borderwidth=2, style='Content.TFrame', name="conteudo_frame")
    conteudo_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True) # Empacota à direita, preenche tudo e expande

    # 4. Adicionar um Título no main_frame (Painel Esquerdo)
    ttk.Label(main_frame, text="Serviços:", style='Title.TLabel').pack(pady=10)

    # --- Botões de Seleção de Serviços (aplicando o estilo 'Menu.TButton') ---
    ttk.Button(main_frame, text="Exploração Região Principal", command=lambda: criar_secao_exploracao_principal(conteudo_frame), style='Menu.TButton').pack(fill=tk.X, pady=5)
    ttk.Button(main_frame, text="Exploração Região Extra", command=lambda: criar_secao_exploracao_extra(conteudo_frame), style='Menu.TButton').pack(fill=tk.X, pady=5)
    ttk.Button(main_frame, text="Upar Árvores/Sistemas", command=lambda: criar_secao_upar_arvore_sistema(conteudo_frame), style='Menu.TButton').pack(fill=tk.X, pady=5)
    ttk.Button(main_frame, text="Farm de Chefes", command=lambda: criar_secao_farm_chefe(conteudo_frame), style='Menu.TButton').pack(fill=tk.X, pady=5)
    ttk.Button(main_frame, text="Build de Personagem", command=lambda: criar_secao_build_personagem(conteudo_frame), style='Menu.TButton').pack(fill=tk.X, pady=5)
    
    ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=10) # Separador visual

    # Botão para ver o conteúdo do carrinho
    ttk.Button(main_frame, text="Ver Carrinho", command=lambda: criar_secao_carrinho(conteudo_frame), style='Menu.TButton').pack(fill=tk.X, pady=5)

    ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=10) # Separador visual

    # Label para exibir o total geral acumulado
    total_label = ttk.Label(main_frame, text=f"Total Geral: R$ {total_geral_gui:.2f}", style='TotalLabel.TLabel')
    total_label.pack(pady=10)

    # Botão para resetar o total e limpar o carrinho
    ttk.Button(main_frame, text="Resetar Tudo", command=resetar_total, style='Reset.TButton').pack(fill=tk.X, pady=5)

    # Inicia o loop principal do Tkinter, mantendo a janela aberta e responsiva
    root.mainloop()

# Esta condição garante que criar_interface() só é chamada quando o script é executado diretamente.
if __name__ == "__main__":
    criar_interface()