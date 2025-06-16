# genshin_calculator_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext # scrolledtext para exibir o carrinho
from reportlab.pdfgen import canvas # Para gerar PDF
from reportlab.lib.pagesizes import A4
from datetime import datetime # Para timestamp no PDF

# Importa os preços e funções do seu arquivo genshin_calculator.py
try:
    from genshin_calculator import PRECOS, \
                                   calcular_exploracao_regiao_principal, \
                                   calcular_exploracao_regiao_extra, \
                                   calcular_upar_arvore_sistema, \
                                   calcular_farm_chefe, \
                                   calcular_build_personagem
except ImportError as e:
    messagebox.showerror("Erro de Importação", f"Não foi possível importar os dados de 'genshin_calculator.py'.\nVerifique se o arquivo existe e não tem erros de sintaxe na linha 1, e se o bloco main() foi removido/comentado.\nErro: {e}")
    # Se o import falhar, define PRECOS como vazio para que o programa possa iniciar, mas com funcionalidade limitada.
    PRECOS = {}

# Variável para acumular o total geral (simulando o total_geral do terminal)
total_geral_gui = 0.0

# O Carrinho: Uma lista para armazenar os itens (dicionários)
carrinho = [] # Cada item será um dicionário: {"servico": "...", "detalhes": "...", "valor": ...}

def exibir_resultado(valor, tipo_servico, detalhes_servico):
    global total_geral_gui
    global carrinho

    item_carrinho = {
        "servico": tipo_servico,
        "detalhes": detalhes_servico,
        "valor": valor
    }
    carrinho.append(item_carrinho)

    total_geral_gui += valor
    atualizar_total_geral_label() # Atualiza o label do total

    messagebox.showinfo("Item Adicionado ao Carrinho",
                        f"Serviço: {tipo_servico}\n"
                        f"Detalhes: {detalhes_servico}\n"
                        f"Valor: R$ {valor:.2f}\n"
                        f"Total acumulado no carrinho: R$ {total_geral_gui:.2f}")

# Função para atualizar o Label do Total Geral na GUI
def atualizar_total_geral_label():
    total_label.config(text=f"Total Geral: R$ {total_geral_gui:.2f}")


def limpar_conteudo_dinamico(frame):
    # Destroi todos os widgets dentro do frame dinâmico, exceto ele mesmo
    for widget in frame.winfo_children():
        widget.destroy()

# --- Funções para criar seções de cálculo (modificadas para chamar as funções de genshin_calculator.py) ---

def criar_secao_exploracao_principal(parent_frame):
    limpar_conteudo_dinamico(parent_frame)

    secao_frame = ttk.Frame(parent_frame, padding="10")
    secao_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(secao_frame, text="Exploração de Região Principal", font=("Arial", 14, "bold")).pack(pady=5)

    # Região
    ttk.Label(secao_frame, text="Selecione a Região:").pack(anchor=tk.W)
    regioes = list(PRECOS["exploracao_regiao_principal"].keys()) if "exploracao_regiao_principal" in PRECOS else []
    regiao_var = tk.StringVar(secao_frame)
    if regioes:
        regiao_var.set(regioes[0])
    regiao_combobox = ttk.Combobox(secao_frame, textvariable=regiao_var, values=regioes, state="readonly")
    regiao_combobox.pack(fill=tk.X, pady=2)

    # Progresso Geral
    ttk.Label(secao_frame, text="Progresso de Exploração Atual (0-100%):").pack(anchor=tk.W)
    progresso_entry = ttk.Entry(secao_frame)
    progresso_entry.insert(0, "100")
    progresso_entry.pack(fill=tk.X, pady=2)

    # Bússola
    bussola_var = tk.StringVar(secao_frame, value="n")
    ttk.Checkbutton(secao_frame, text="Cliente tem bússola de exploração?", variable=bussola_var, onvalue="s", offvalue="n").pack(anchor=tk.W, pady=2)

    # Nível Estátua Sete
    ttk.Label(secao_frame, text="Nível atual da Estátua dos Sete (0-10):").pack(anchor=tk.W)
    estatua_entry = ttk.Entry(secao_frame)
    estatua_entry.insert(0, "10")
    estatua_entry.pack(fill=tk.X, pady=2)

    # Nível Reputação Cidade
    ttk.Label(secao_frame, text="Nível atual de Reputação da Cidade (0-10):").pack(anchor=tk.W)
    reputacao_entry = ttk.Entry(secao_frame)
    reputacao_entry.insert(0, "10")
    reputacao_entry.pack(fill=tk.X, pady=2)

    def adicionar_ao_carrinho():
        try:
            regiao_selecionada = regiao_var.get()
            progresso = float(progresso_entry.get())
            bussola = bussola_var.get()
            estatua_lvl = int(estatua_entry.get())
            reputacao_lvl = int(reputacao_entry.get())

            # Chamar a função de cálculo do genshin_calculator.py
            valor = calcular_exploracao_regiao_principal(
                regiao_selecionada, progresso, bussola, estatua_lvl, reputacao_lvl
            )
            detalhes = (f"{regiao_selecionada} ({progresso}%), "
                        f"Bússola: {'Sim' if bussola == 's' else 'Não'}, "
                        f"Estátua Nv: {estatua_lvl}, Rep. Nv: {reputacao_lvl}")
            exibir_resultado(valor, "Exploração Região Principal", detalhes)
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Por favor, insira valores numéricos válidos. Detalhes: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao calcular a exploração: {e}")

    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=10)


def criar_secao_exploracao_extra(parent_frame):
    limpar_conteudo_dinamico(parent_frame)

    secao_frame = ttk.Frame(parent_frame, padding="10")
    secao_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(secao_frame, text="Exploração de Região Extra", font=("Arial", 14, "bold")).pack(pady=5)

    ttk.Label(secao_frame, text="Selecione a Região Extra:").pack(anchor=tk.W)
    regioes_extras = list(PRECOS["exploracao_regiao_extra"].keys()) if "exploracao_regiao_extra" in PRECOS else []
    regiao_extra_var = tk.StringVar(secao_frame)
    if regioes_extras:
        regiao_extra_var.set(regioes_extras[0])
    regiao_extra_combobox = ttk.Combobox(secao_frame, textvariable=regiao_extra_var, values=regioes_extras, state="readonly")
    regiao_extra_combobox.pack(fill=tk.X, pady=2)

    def adicionar_ao_carrinho():
        try:
            regiao_selecionada = regiao_extra_var.get()
            valor = calcular_exploracao_regiao_extra(regiao_selecionada)
            detalhes = f"{regiao_selecionada} (100% Exploração)"
            exibir_resultado(valor, "Exploração Região Extra", detalhes)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=10)


def criar_secao_upar_arvore_sistema(parent_frame):
    limpar_conteudo_dinamico(parent_frame)

    secao_frame = ttk.Frame(parent_frame, padding="10")
    secao_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(secao_frame, text="Upar Árvores/Sistemas de Oferenda", font=("Arial", 14, "bold")).pack(pady=5)

    ttk.Label(secao_frame, text="Selecione a Árvore/Sistema:").pack(anchor=tk.W)
    sistemas = list(PRECOS["upar_arvore_sistema"].keys()) if "upar_arvore_sistema" in PRECOS else []
    sistema_var = tk.StringVar(secao_frame)
    if sistemas:
        sistema_var.set(sistemas[0])
    sistema_combobox = ttk.Combobox(secao_frame, textvariable=sistema_var, values=sistemas, state="readonly")
    sistema_combobox.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Nível Inicial:").pack(anchor=tk.W)
    lvl_inicial_entry = ttk.Entry(secao_frame)
    lvl_inicial_entry.insert(0, "0")
    lvl_inicial_entry.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Nível Desejado (Máx 50 para Natlan, 12 para Espinha, 10 para Abismo):").pack(anchor=tk.W)
    lvl_final_entry = ttk.Entry(secao_frame)
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

    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=10)


def criar_secao_farm_chefe(parent_frame):
    limpar_conteudo_dinamico(parent_frame)

    secao_frame = ttk.Frame(parent_frame, padding="10")
    secao_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(secao_frame, text="Farm de Chefes", font=("Arial", 14, "bold")).pack(pady=5)
    ttk.Label(secao_frame, text=f"Preço por material de chefe: R$ {PRECOS.get('farm_chefe', 0.0):.2f}").pack(anchor=tk.W)

    ttk.Label(secao_frame, text="Quantidade atual de materiais:").pack(anchor=tk.W)
    qtd_atual_entry = ttk.Entry(secao_frame)
    qtd_atual_entry.insert(0, "0")
    qtd_atual_entry.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Quantidade desejada de materiais:").pack(anchor=tk.W)
    qtd_desejada_entry = ttk.Entry(secao_frame)
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

    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=10)


def criar_secao_build_personagem(parent_frame):
    limpar_conteudo_dinamico(parent_frame)

    secao_frame = ttk.Frame(parent_frame, padding="10")
    secao_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(secao_frame, text="Build de Personagem", font=("Arial", 14, "bold")).pack(pady=5)

    # Nível Personagem
    ttk.Label(secao_frame, text="Nível Inicial do Personagem:").pack(anchor=tk.W)
    lvl_personagem_inicial_entry = ttk.Entry(secao_frame)
    lvl_personagem_inicial_entry.insert(0, "1")
    lvl_personagem_inicial_entry.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Nível Desejado do Personagem:").pack(anchor=tk.W)
    lvl_personagem_final_entry = ttk.Entry(secao_frame)
    lvl_personagem_final_entry.insert(0, "90")
    lvl_personagem_final_entry.pack(fill=tk.X, pady=2)

    # Níveis de Talento (total a upar para *todos* os talentos)
    ttk.Label(secao_frame, text="Total de Níveis de Talento a upar (ex: 3 talentos de 1 para 10 = 27):").pack(anchor=tk.W)
    niveis_talento_entry = ttk.Entry(secao_frame)
    niveis_talento_entry.insert(0, "0")
    niveis_talento_entry.pack(fill=tk.X, pady=2)

    # Farm de Artefatos
    ttk.Label(secao_frame, text="Resina gasta em Domínios de Artefatos (múltiplos de 20):").pack(anchor=tk.W)
    resina_artefatos_entry = ttk.Entry(secao_frame)
    resina_artefatos_entry.insert(0, "0")
    resina_artefatos_entry.pack(fill=tk.X, pady=2)

    # Upar Artefato para +20
    ttk.Label(secao_frame, text="Quantos artefatos para upar para +20:").pack(anchor=tk.W)
    qtd_artefatos_20_entry = ttk.Entry(secao_frame)
    qtd_artefatos_20_entry.insert(0, "0")
    qtd_artefatos_20_entry.pack(fill=tk.X, pady=2)

    # Nível de Arma
    ttk.Label(secao_frame, text="Nível Inicial da Arma:").pack(anchor=tk.W)
    lvl_arma_inicial_entry = ttk.Entry(secao_frame)
    lvl_arma_inicial_entry.insert(0, "1")
    lvl_arma_inicial_entry.pack(fill=tk.X, pady=2)

    ttk.Label(secao_frame, text="Nível Desejado da Arma:").pack(anchor=tk.W)
    lvl_arma_final_entry = ttk.Entry(secao_frame)
    lvl_arma_final_entry.insert(0, "90")
    lvl_arma_final_entry.pack(fill=tk.X, pady=2)

    # Farm de Materiais Comuns
    ttk.Label(secao_frame, text="Quantidade de Materiais Comuns a farmar:").pack(anchor=tk.W)
    qtd_materiais_comuns_entry = ttk.Entry(secao_frame)
    qtd_materiais_comuns_entry.insert(0, "0")
    qtd_materiais_comuns_entry.pack(fill=tk.X, pady=2)

    # Otimização de Build (checkbox para um valor fixo)
    otimizacao_build_var = tk.StringVar(secao_frame, value="no")
    ttk.Checkbutton(secao_frame, text=f"Incluir Otimização de Build (R$ {PRECOS.get('build_personagem', {}).get('otimizacao_build_fixo', 0.0):.2f})?", variable=otimizacao_build_var, onvalue="yes", offvalue="no").pack(anchor=tk.W, pady=5)


    def adicionar_ao_carrinho():
        try:
            lvl_personagem_inicial = int(lvl_personagem_inicial_entry.get())
            lvl_personagem_final = int(lvl_personagem_final_entry.get())
            niveis_talento_total = int(niveis_talento_entry.get())
            resina_artefatos_gasta = int(resina_artefatos_entry.get())
            qtd_artefatos_20 = int(qtd_artefatos_20_entry.get())
            lvl_arma_inicial = int(lvl_arma_inicial_entry.get())
            lvl_arma_final = int(lvl_arma_final_entry.get())
            qtd_materiais_comuns = int(qtd_materiais_comuns_entry.get())
            incluir_otimizacao_build = (otimizacao_build_var.get() == "yes")

            valor = calcular_build_personagem(
                lvl_personagem_inicial, lvl_personagem_final,
                niveis_talento_total,
                resina_artefatos_gasta,
                qtd_artefatos_20,
                lvl_arma_inicial, lvl_arma_final,
                qtd_materiais_comuns,
                incluir_otimizacao_build
            )
            detalhes = (f"Personagem Nv {lvl_personagem_inicial}-{lvl_personagem_final}, "
                        f"Talentos Nv: {niveis_talento_total}, "
                        f"Artefatos Res: {resina_artefatos_gasta}, Artefatos +20: {qtd_artefatos_20}, "
                        f"Arma Nv {lvl_arma_inicial}-{lvl_arma_final}, Mat. Comuns: {qtd_materiais_comuns}, "
                        f"Otimização: {'Sim' if incluir_otimizacao_build else 'Não'}")
            exibir_resultado(valor, "Build de Personagem", detalhes)
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Por favor, insira valores numéricos válidos. Detalhes: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao calcular a build: {e}")

    ttk.Button(secao_frame, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).pack(pady=10)


# --- Nova Seção: Visualizar Carrinho ---
def criar_secao_carrinho(parent_frame):
    limpar_conteudo_dinamico(parent_frame)

    carrinho_frame = ttk.Frame(parent_frame, padding="10")
    carrinho_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(carrinho_frame, text="Conteúdo do Carrinho", font=("Arial", 14, "bold")).pack(pady=5)

    if not carrinho:
        ttk.Label(carrinho_frame, text="O carrinho está vazio.").pack(pady=10)
    else:
        # Usar um ScrolledText para exibir os itens do carrinho
        carrinho_text = scrolledtext.ScrolledText(carrinho_frame, wrap=tk.WORD, width=60, height=15)
        carrinho_text.pack(fill=tk.BOTH, expand=True, pady=10)

        for i, item in enumerate(carrinho):
            carrinho_text.insert(tk.END, f"Item {i+1}:\n")
            carrinho_text.insert(tk.END, f"  Serviço: {item['servico']}\n")
            carrinho_text.insert(tk.END, f"  Detalhes: {item['detalhes']}\n")
            carrinho_text.insert(tk.END, f"  Valor: R$ {item['valor']:.2f}\n")
            carrinho_text.insert(tk.END, "-" * 40 + "\n") # Separador
        
        carrinho_text.config(state=tk.DISABLED) # Impede edição


    ttk.Label(carrinho_frame, text=f"Total do Carrinho: R$ {total_geral_gui:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

    # Botão para Gerar PDF
    ttk.Button(carrinho_frame, text="Gerar PDF do Carrinho", command=gerar_pdf_carrinho).pack(pady=10)

    # Botão para Limpar Carrinho
    ttk.Button(carrinho_frame, text="Limpar Carrinho", command=limpar_carrinho).pack(pady=5)


def gerar_pdf_carrinho():
    if not carrinho:
        messagebox.showwarning("Carrinho Vazio", "Adicione itens ao carrinho antes de gerar o PDF.")
        return

    # Instalação do ReportLab: pip install reportlab
    # O arquivo PDF será salvo no mesmo diretório do script.
    
    filename = f"Orcamento_Genshin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4 # Tamanho da página A4

    y_pos = height - 50 # Posição inicial no topo da página

    # Título
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y_pos, "Orçamento de Serviços Genshin Impact")
    y_pos -= 30

    # Data
    c.setFont("Helvetica", 10)
    c.drawString(50, y_pos, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    y_pos -= 30

    # Itens do Carrinho
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos, "Itens do Carrinho:")
    y_pos -= 20

    c.setFont("Helvetica", 10)
    for i, item in enumerate(carrinho):
        if y_pos < 80: # Se estiver chegando no final da página, cria uma nova
            c.showPage()
            y_pos = height - 50
            c.setFont("Helvetica", 10) # Redefine a fonte para a nova página
        
        c.drawString(60, y_pos, f"Serviço: {item['servico']}")
        y_pos -= 12
        c.drawString(70, y_pos, f"Detalhes: {item['detalhes']}")
        y_pos -= 12
        c.drawString(70, y_pos, f"Valor: R$ {item['valor']:.2f}")
        y_pos -= 15 # Espaço entre os itens

    # Total Geral
    y_pos -= 20
    if y_pos < 80: # Garante que o total não fique cortado
        c.showPage()
        y_pos = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos, f"TOTAL GERAL: R$ {total_geral_gui:.2f}")

    c.save() # Salva o PDF
    messagebox.showinfo("PDF Gerado", f"O orçamento foi salvo como:\n{filename}")


def limpar_carrinho():
    global carrinho
    global total_geral_gui
    
    if messagebox.askyesno("Limpar Carrinho", "Tem certeza que deseja limpar todo o carrinho?"):
        carrinho = []
        total_geral_gui = 0.0
        atualizar_total_geral_label()
        # Redesenha a seção do carrinho para mostrar que está vazia
        criar_secao_carrinho(root.nametowidget(".!frame2")) # Pega o conteudo_frame pelo nome do widget. Uma forma mais robusta é passar o frame como parâmetro para limpar_carrinho
        messagebox.showinfo("Carrinho Limpo", "O carrinho foi esvaziado.")


def criar_interface():
    global total_label # Declara como global para poder ser atualizada por outras funções

    # 1. Configuração da Janela Principal
    root = tk.Tk()
    root.title("Calculadora de Serviços Genshin Impact")
    root.geometry("1000x700")
    root.resizable(True, True)

    # 2. Frame Principal (para os botões de seleção de serviço)
    main_frame = ttk.Frame(root, padding="10 10 10 10")
    main_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

    # 3. Frame para o Conteúdo Dinâmico (onde as seções de cálculo aparecerão)
    conteudo_frame = ttk.Frame(root, padding="10 10 10 10", relief=tk.RAISED, borderwidth=2)
    conteudo_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # 4. Adicionar um Título no main_frame (Painel Esquerdo)
    ttk.Label(main_frame, text="Serviços:", font=("Arial", 16, "bold")).pack(pady=10)

    # Botões dos Serviços (agora chamando funções que criarão as seções no conteudo_frame)
    ttk.Button(main_frame, text="Exploração Região Principal", command=lambda: criar_secao_exploracao_principal(conteudo_frame)).pack(fill=tk.X, pady=5)
    ttk.Button(main_frame, text="Exploração Região Extra", command=lambda: criar_secao_exploracao_extra(conteudo_frame)).pack(fill=tk.X, pady=5)
    ttk.Button(main_frame, text="Upar Árvores/Sistemas", command=lambda: criar_secao_upar_arvore_sistema(conteudo_frame)).pack(fill=tk.X, pady=5)
    ttk.Button(main_frame, text="Farm de Chefes", command=lambda: criar_secao_farm_chefe(conteudo_frame)).pack(fill=tk.X, pady=5)
    ttk.Button(main_frame, text="Build de Personagem", command=lambda: criar_secao_build_personagem(conteudo_frame)).pack(fill=tk.X, pady=5)
    
    ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=10)

    # Novo botão para ver o carrinho
    ttk.Button(main_frame, text="Ver Carrinho", command=lambda: criar_secao_carrinho(conteudo_frame)).pack(fill=tk.X, pady=5)

    ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=10)

    # Exibição do Total Geral
    total_label = ttk.Label(main_frame, text=f"Total Geral: R$ {total_geral_gui:.2f}", font=("Arial", 12, "bold"))
    total_label.pack(pady=10)

    def resetar_total():
        global total_geral_gui
        global carrinho
        if messagebox.askyesno("Confirmar Reset", "Tem certeza que deseja resetar o total e limpar o carrinho?"):
            carrinho = [] # Limpa a lista do carrinho
            total_geral_gui = 0.0
            atualizar_total_geral_label()
            limpar_conteudo_dinamico(conteudo_frame)
            messagebox.showinfo("Reset Concluído", "Total geral e carrinho resetados.")

    ttk.Button(main_frame, text="Resetar Tudo", command=resetar_total).pack(fill=tk.X, pady=5)

    root.mainloop()

# Chamada da função para criar e iniciar a interface
if __name__ == "__main__":
    criar_interface()