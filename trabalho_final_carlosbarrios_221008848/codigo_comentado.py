# ============================================================
# BLOCO 1 — IMPORTAÇÃO DAS BIBLIOTECAS DO SISTEMA
#
# Nesta primeira parte são importadas todas as bibliotecas que
# o programa precisa para funcionar.
#
# A biblioteca tkinter é usada para criar a interface gráfica,
# ou seja, a janela do sistema, os botões, textos, caixas de
# seleção e áreas onde os dados aparecem.
#
# De dentro do tkinter também são importados:
# - ttk: usado para componentes visuais mais modernos, como Combobox;
# - filedialog: usado para abrir a janela de salvar arquivos;
# - messagebox: usado para mostrar mensagens de erro ou sucesso.
#
# A biblioteca pandas, importada como pd, é responsável por ler,
# limpar, filtrar e cruzar os dados dos arquivos CSV e Excel.
#
# A biblioteca matplotlib é usada para gerar os gráficos.
# O comando matplotlib.use("TkAgg") faz com que os gráficos do
# Matplotlib funcionem dentro da janela criada pelo Tkinter.
#
# Também são importados Figure e FigureCanvasTkAgg, que permitem
# criar figuras/gráficos e colocá-los dentro da interface gráfica.
# ============================================================
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# ============================================================
# BLOCO 2 — ARQUIVOS, REGIÕES ADMINISTRATIVAS E FUNÇÕES AUXILIARES
#
# Nesta parte são definidos os arquivos utilizados pelo sistema:
# - ARQ_MORADORES: arquivo CSV com dados dos moradores;
# - ARQ_DOMICILIOS: arquivo Excel com dados dos domicílios.
#
# O dicionário RAS guarda a relação entre o código numérico de
# cada localidade e o nome da Região Administrativa correspondente.
# Por exemplo, o código 5301 representa Plano Piloto.
#
# Funções desta parte:
#
# nome_ra(cod):
# Recebe o código de uma RA como parâmetro e retorna o nome dela.
# Caso o código não esteja no dicionário, retorna um texto padrão
# como "RA 5301". Isso evita erro caso apareça algum código novo.
#
# texto_ra(cod):
# Recebe o código de uma RA e monta um texto mais completo para
# aparecer no Combobox, como "5301 - Plano Piloto".
# Isso melhora a visualização para o usuário.
#
# codigo_ra(texto):
# Recebe o texto escolhido no Combobox e extrai somente o código
# numérico da RA. Por exemplo, transforma "5301 - Plano Piloto"
# em 5301. Também trata os casos "Todas" e "Nenhuma".
#
# fmt(n):
# Recebe um número e formata com ponto como separador de milhar.
# Por exemplo, 15000 vira "15.000". Essa função é usada para
# mostrar totais de moradores e domicílios de forma mais legível.
#
# Essa parte é importante porque organiza os dados básicos usados
# em todo o programa e evita repetição de código.
# ============================================================
ARQ_MORADORES = "moradores.csv"
ARQ_DOMICILIOS = "domicilios.xlsx"

RAS = {
    5301: "Plano Piloto", 5302: "Gama", 5303: "Taguatinga", 5304: "Brazlândia",
    5305: "Sobradinho", 5306: "Planaltina", 5307: "Paranoá",
    5308: "Núcleo Bandeirante", 5309: "Ceilândia", 5310: "Guará",
    5311: "Cruzeiro", 5312: "Samambaia", 5313: "Santa Maria",
    5314: "São Sebastião", 5315: "Recanto das Emas", 5316: "Lago Sul",
    5317: "Riacho Fundo", 5318: "Lago Norte", 5319: "Candangolândia",
    5320: "Águas Claras", 5321: "Riacho Fundo II", 5322: "Sudoeste e Octogonal",
    5323: "Varjão", 5324: "Park Way", 5325: "SCIA", 5326: "Sobradinho II",
    5327: "Jardim Botânico", 5328: "Itapoã", 5329: "SIA",
    5330: "Vicente Pires", 5331: "Fercal", 5332: "Sol Nascente / Pôr do Sol",
    5333: "Arniqueira", 5334: "Arapoanga", 5335: "Água Quente",
    5336: "Área Rural", 5241: "Águas Lindas de Goiás", 5242: "Alexânia",
    5243: "Cidade Ocidental", 5244: "Cristalina", 5245: "Cocalzinho de Goiás",
    5246: "Formosa", 5247: "Luziânia", 5248: "Novo Gama",
    5249: "Padre Bernardo", 5250: "Planaltina de Goiás",
    5251: "Santo Antônio do Descoberto", 5252: "Valparaíso de Goiás"
}

def nome_ra(cod):
    """Retorna o nome da Região Administrativa."""
    return RAS.get(int(cod), f"RA {cod}")


def texto_ra(cod):
    """Retorna código e nome da RA para exibir no filtro."""
    return f"{int(cod)} - {nome_ra(cod)}"


def codigo_ra(texto):
    """Extrai o código da RA escolhido no Combobox."""
    if texto in ["Todas", "Nenhuma"]:
        return texto
    return int(texto.split(" - ")[0])


def fmt(n):
    """Formata números inteiros com ponto."""
    return f"{n:,.0f}".replace(",", ".")

# ============================================================
# BLOCO 3 — CARREGAMENTO, LIMPEZA, ESTATÍSTICAS E RANKING
#
# Esta parte contém funções responsáveis por preparar e analisar
# os dados antes de eles serem mostrados na interface.
#
# carregar_dados():
# Essa função lê os arquivos de moradores e domicílios.
# Ela usa pd.read_csv para carregar o arquivo CSV e pd.read_excel
# para carregar o arquivo Excel.
#
# Dentro dela existe um bloco try/except. O try tenta carregar os
# arquivos normalmente. Se acontecer erro, como arquivo não encontrado
# ou nome errado, o except mostra uma mensagem de erro usando
# messagebox.showerror e encerra o programa com SystemExit.
#
# Depois do carregamento, a função corrige possíveis problemas nos
# nomes das colunas, como o caractere estranho "ï»¿", que pode aparecer
# por causa da codificação do arquivo.
#
# Em seguida, são removidos os valores sentinela 88888 e 99999 das
# colunas principais. Esses valores não representam dados reais:
# - 88888 geralmente significa não declarado;
# - 99999 geralmente significa não se aplica.
#
# Depois, a função faz um merge entre moradores e domicílios usando
# a coluna A01nficha. O merge funciona como uma junção de tabelas,
# permitindo juntar informações do morador com informações do domicílio.
#
# estatisticas(df):
# Recebe um DataFrame como parâmetro e calcula os principais indicadores:
# - total de moradores;
# - porcentagem de pessoas com plano de saúde;
# - porcentagem de pessoas que utilizaram serviço de saúde;
# - idade média;
# - idade mediana;
# - quantidade de pessoas com plano de saúde.
#
# Se o DataFrame estiver vazio, a função retorna vários zeros para
# evitar erro de divisão por zero.
#
# bubble_sort(lista):
# Essa função ordena manualmente uma lista usando o algoritmo Bubble Sort.
# O Bubble Sort compara elementos vizinhos e troca suas posições quando
# estão fora da ordem desejada.
#
# Neste código, ele ordena do maior para o menor percentual de cobertura.
# Apesar de existirem formas prontas de ordenar em Python, o Bubble Sort
# mostra o funcionamento de um algoritmo de ordenação de forma didática.
#
# ranking_plano(df):
# Essa função percorre cada RA presente nos dados, calcula a taxa de
# cobertura de plano de saúde daquela região e guarda o resultado em
# uma lista. Depois, essa lista é ordenada com bubble_sort.
#
# O resultado final é um ranking das Regiões Administrativas com maior
# cobertura de plano de saúde.
# ============================================================
def carregar_dados():
    """Carrega, limpa sentinelas e cruza moradores com domicílios."""
    try:
        moradores = pd.read_csv(ARQ_MORADORES, sep=";", encoding="utf-8-sig", low_memory=False)
        domicilios = pd.read_excel(ARQ_DOMICILIOS)
    except Exception as erro:
        messagebox.showerror("Erro", f"Não foi possível carregar os arquivos.\n\n{erro}")
        raise SystemExit

    moradores.columns = moradores.columns.str.replace("ï»¿", "", regex=False)
    domicilios.columns = domicilios.columns.str.replace("ï»¿", "", regex=False)

    # Sentinelas da PDAD: 88888 = não declarado; 99999 = não se aplica.
    for col in ["localidade", "idade_calculada", "G01", "G05"]:
        moradores = moradores[~moradores[col].isin([88888, 99999])]

    dados = pd.merge(moradores.copy(), domicilios, on="A01nficha", how="left",
                     suffixes=("_morador", "_domicilio"))

    if "localidade_morador" in dados.columns:
        dados["localidade"] = dados["localidade_morador"]

    return moradores.copy(), domicilios, dados


def estatisticas(df):
    """Calcula estatísticas principais de saúde."""
    total = len(df)
    if total == 0:
        return 0, 0, 0, 0, 0, 0

    plano = (df["G05"] == 1).sum()
    atendimento = (df["G01"] == 1).sum()

    return (
        total,
        plano / total * 100,
        atendimento / total * 100,
        df["idade_calculada"].mean(),
        df["idade_calculada"].median(),
        plano
    )


def bubble_sort(lista):
    """Ordena manualmente usando Bubble Sort."""
    lista = lista.copy()
    for i in range(len(lista)):
        for j in range(len(lista) - i - 1):
            if lista[j][1] < lista[j + 1][1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def ranking_plano(df):
    """Gera ranking das RAs por cobertura de plano."""
    ranking = []
    for ra in df["localidade"].dropna().unique():
        parte = df[df["localidade"] == ra]
        taxa = (parte["G05"] == 1).sum() / len(parte) * 100
        ranking.append((int(ra), taxa))
    return bubble_sort(ranking)
# ============================================================
# BLOCO 4 — MONTAGEM DA INTERFACE GRÁFICA
#
# Nesta parte o sistema começa a criar a janela visual que o usuário
# vai utilizar.
#
# Primeiro, a função carregar_dados() é chamada e retorna três bases:
# - moradores: dados dos moradores já tratados;
# - domicilios: dados dos domicílios;
# - dados: base unificada com moradores e domicílios juntos.
#
# Depois é criada a lista_ras, que contém os nomes das RAs formatados
# para aparecerem nos filtros.
#
# A variável janela recebe tk.Tk(), que cria a janela principal.
# Em seguida, são definidos o título, o tamanho inicial, o tamanho
# mínimo e a cor de fundo da aplicação.
#
# A variável topo cria a área superior azul da interface. Nela são
# colocados três textos:
# - o título principal do sistema;
# - o subtítulo explicando o recorte de saúde;
# - a quantidade de moradores e domicílios carregados.
#
# A variável filtros cria uma área específica para os filtros e botões.
# Nela ficam:
# - combo_ra: Combobox para escolher a RA principal;
# - combo_comp: Combobox para escolher uma RA de comparação;
# - botões de Atualizar, Limpar, Exportar CSV e Exportar TXT.
#
# A área estat cria os textos onde aparecem os resultados numéricos,
# como total de moradores, porcentagem com plano, idade média e mediana.
#
# A variável area cria o espaço onde os gráficos serão exibidos.
# São criadas duas figuras:
# - fig1 e ax1: gráfico de cobertura de plano de saúde;
# - fig2 e ax2: histograma da distribuição de idade.
#
# O rank_box é uma caixa de texto usada para mostrar o ranking das
# cinco RAs com maior cobertura de plano de saúde.
#
# O status é uma barra inferior que mostra mensagens ao usuário,
# como "Sistema carregado", "Filtros limpos" ou "CSV exportado".
#
# Essa parte não faz os cálculos principais, mas organiza toda a
# aparência do sistema e prepara os espaços onde os resultados serão
# exibidos.
# ============================================================
moradores, domicilios, dados = carregar_dados()
lista_ras = [texto_ra(c) for c in sorted(moradores["localidade"].dropna().unique())]
janela = tk.Tk()
janela.title("Sistema PDAD 2024 - Saúde")
janela.geometry("1150x720")
janela.minsize(1000, 650)
janela.configure(bg="#ECEFF1")
topo = tk.Frame(janela, bg="#0D47A1", pady=12)
topo.pack(fill="x")

tk.Label(topo, text="Sistema de Exploração da PDAD 2024",
         font=("Arial", 20, "bold"), bg="#0D47A1", fg="white").pack()

tk.Label(topo, text="Recorte C — Saúde e acesso a serviços no Distrito Federal",
         font=("Arial", 11), bg="#0D47A1", fg="white").pack()

tk.Label(topo, text=f"{fmt(len(moradores))} moradores · {fmt(len(domicilios))} domicílios carregados",
         font=("Arial", 10), bg="#0D47A1", fg="white").pack(pady=(5, 0))

filtros = tk.LabelFrame(janela, text="Filtros e ações", bg="#ECEFF1",
                        font=("Arial", 10, "bold"), padx=10, pady=10)
filtros.pack(fill="x", padx=20, pady=12)
tk.Label(filtros, text="RA principal:", bg="#ECEFF1").grid(row=0, column=0, padx=5)
combo_ra = ttk.Combobox(filtros, values=["Todas"] + lista_ras, state="readonly", width=31)
combo_ra.current(0)
combo_ra.grid(row=0, column=1, padx=5)

tk.Label(filtros, text="Comparar com:", bg="#ECEFF1").grid(row=0, column=2, padx=5)
combo_comp = ttk.Combobox(filtros, values=["Nenhuma"] + lista_ras, state="readonly", width=31)
combo_comp.current(0)
combo_comp.grid(row=0, column=3, padx=5)
botoes = [
    ("Atualizar", "#2E7D32"),
    ("Limpar", "#546E7A"),
    ("Exportar CSV", "#1565C0"),
    ("Exportar TXT", "#6A1B9A")
]
for i, (txt, cor) in enumerate(botoes, start=4):
    tk.Button(filtros, text=txt, bg=cor, fg="white", width=13,
              font=("Arial", 9, "bold")).grid(row=0, column=i, padx=4)

btn_atualizar, btn_limpar, btn_csv, btn_txt = filtros.grid_slaves(row=0)[3::-1]
estat = tk.LabelFrame(janela, text="Estatísticas", bg="#ECEFF1",
                      font=("Arial", 10, "bold"), padx=15, pady=10)
estat.pack(fill="x", padx=20)

labels = []
for _ in range(5):
    lab = tk.Label(estat, font=("Arial", 11), bg="#ECEFF1", anchor="w")
    lab.pack(fill="x")
    labels.append(lab)

area = tk.Frame(janela, bg="#ECEFF1")
area.pack(fill="both", expand=True, padx=20, pady=12)
fig1 = Figure(figsize=(5.5, 4), dpi=100)
ax1 = fig1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(fig1, master=area)
canvas1.get_tk_widget().pack(side="left", fill="both", expand=True, padx=(0, 8))
fig2 = Figure(figsize=(5.5, 4), dpi=100)
ax2 = fig2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(fig2, master=area)
canvas2.get_tk_widget().pack(side="right", fill="both", expand=True, padx=(8, 0))
rank_box = tk.Text(janela, height=5, font=("Consolas", 10))
rank_box.pack(fill="x", padx=20, pady=(0, 8))
status = tk.Label(janela, text="Sistema carregado.", bg="#CFD8DC",
                  anchor="w", padx=10)
status.pack(fill="x", side="bottom")
# ============================================================
# BLOCO 5 — FUNCIONAMENTO DO SISTEMA, GRÁFICOS, FILTROS E EXPORTAÇÃO
#
# Esta última parte contém as funções que fazem a interface responder
# às ações do usuário.
#
# filtrar():
# Verifica qual RA foi escolhida no combo_ra.
# Se a opção for "Todas", retorna uma cópia completa dos dados.
# Caso contrário, filtra o DataFrame para mostrar apenas os moradores
# da RA escolhida.
#
# comparar():
# Verifica se o usuário escolheu uma RA para comparação no combo_comp.
# Se a opção for "Nenhuma", retorna None.
# Caso exista uma RA escolhida, retorna os dados somente daquela região.
#
# desenhar_grafico_plano(df, df_comp=None):
# Cria o gráfico de barras da cobertura de plano de saúde.
# O parâmetro df representa os dados principais filtrados.
# O parâmetro df_comp é opcional e representa os dados da RA comparada.
#
# A função limpa o gráfico anterior, calcula a porcentagem de pessoas
# com plano de saúde e desenha uma ou duas barras, dependendo se existe
# comparação. Também coloca título, legenda dos eixos, grade e o valor
# percentual acima de cada barra.
#
# desenhar_grafico_idade(df):
# Cria um histograma com a distribuição de idade dos moradores.
# O histograma mostra quantas pessoas existem em diferentes faixas
# de idade. A função também calcula a média de idade e desenha uma
# linha vertical indicando essa média no gráfico.
#
# atualizar_ranking():
# Limpa a caixa de texto do ranking e escreve novamente o Top 5 das
# RAs com maior cobertura de plano de saúde. Para isso, usa a função
# ranking_plano(dados), que já calcula e ordena as regiões.
#
# atualizar():
# É uma das funções principais do sistema.
# Ela chama filtrar(), comparar(), estatisticas(), desenha os gráficos,
# atualiza os textos das estatísticas, atualiza o ranking e muda a barra
# de status. Sempre que o usuário altera um filtro ou clica em Atualizar,
# essa função reorganiza a tela com os dados mais recentes.
#
# limpar():
# Volta os filtros para o estado inicial:
# - RA principal como "Todas";
# - comparação como "Nenhuma".
# Depois chama atualizar() para redesenhar a tela.
#
# exportar_csv():
# Pega os dados filtrados e permite salvá-los em um arquivo CSV.
# A função usa filedialog.asksaveasfilename para o usuário escolher
# onde salvar. Se um caminho for escolhido, o DataFrame é salvo com
# df.to_csv.
#
# exportar_txt():
# Exporta um relatório simples em formato TXT.
# Esse relatório contém a RA analisada, a comparação escolhida,
# total de moradores, percentual com plano, uso de serviço de saúde,
# idade média e idade mediana.
#
# No final do código, os botões são conectados às funções:
# - btn_atualizar chama atualizar;
# - btn_limpar chama limpar;
# - btn_csv chama exportar_csv;
# - btn_txt chama exportar_txt.
#
# Os Combobox também são ligados à função atualizar, então a tela muda
# automaticamente quando o usuário seleciona outra RA.
#
# Por fim, atualizar() é chamado uma vez para preencher a tela inicial,
# e janela.mainloop() mantém a interface aberta esperando as ações do
# usuário.
# ============================================================
def filtrar():
    """Filtra pela RA principal."""
    escolha = combo_ra.get()
    if escolha == "Todas":
        return dados.copy()
    return dados[dados["localidade"] == codigo_ra(escolha)].copy()

def comparar():
    """Retorna os dados da RA de comparação."""
    escolha = combo_comp.get()
    if escolha == "Nenhuma":
        return None
    return dados[dados["localidade"] == codigo_ra(escolha)].copy()

def desenhar_grafico_plano(df, df_comp=None):
    """Desenha gráfico comparativo de plano de saúde."""
    ax1.clear()

    if len(df) == 0:
        ax1.set_title("Nenhum dado encontrado")
        canvas1.draw()
        return

    total, plano_pct, *_ = estatisticas(df)
    nome = "DF" if combo_ra.get() == "Todas" else nome_ra(codigo_ra(combo_ra.get()))

    nomes = [nome]
    valores = [plano_pct]

    if df_comp is not None and len(df_comp) > 0:
        _, plano_comp, *_ = estatisticas(df_comp)
        nomes.append(nome_ra(codigo_ra(combo_comp.get())))
        valores.append(plano_comp)

    barras = ax1.bar(nomes, valores)
    ax1.set_title("Cobertura de plano de saúde", fontsize=12, fontweight="bold", pad=12)
    ax1.set_ylabel("Percentual (%)")
    ax1.set_xlabel("Região analisada")
    ax1.set_ylim(0, 100)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.tick_params(axis="x", rotation=15, labelsize=8)

    for barra, valor in zip(barras, valores):
        ax1.text(barra.get_x() + barra.get_width() / 2,
                 valor + 1, f"{valor:.1f}%",
                 ha="center", fontsize=9)

    fig1.tight_layout()
    canvas1.draw()

def desenhar_grafico_idade(df):
    """Desenha histograma de idade."""
    ax2.clear()

    if len(df) == 0:
        ax2.set_title("Nenhum dado encontrado")
        canvas2.draw()
        return

    idades = df["idade_calculada"].dropna()

    ax2.hist(idades, bins=12, edgecolor="black")
    media = idades.mean()

    ax2.axvline(media, linestyle="--", linewidth=2)
    ax2.text(media, ax2.get_ylim()[1] * 0.9,
             f"Média: {media:.1f}",
             rotation=90, va="top", ha="right", fontsize=9)

    ax2.set_title("Distribuição etária", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xlabel("Idade")
    ax2.set_ylabel("Quantidade de moradores")
    ax2.grid(axis="y", linestyle="--", alpha=0.4)

    fig2.tight_layout()
    canvas2.draw()


def atualizar_ranking():
    """Mostra ranking manual das RAs."""
    rank_box.delete("1.0", tk.END)
    rank_box.insert(tk.END, "Top 5 RAs por cobertura de plano de saúde:\n")

    for pos, (ra, taxa) in enumerate(ranking_plano(dados)[:5], start=1):
        rank_box.insert(tk.END, f"{pos}º — {nome_ra(ra)}: {taxa:.1f}%\n")


def atualizar():
    """Atualiza estatísticas, gráficos e ranking."""
    df = filtrar()
    df_comp = comparar()

    total, plano, atendimento, media, mediana, qtd_plano = estatisticas(df)

    textos = [
        f"Total de moradores filtrados: {fmt(total)}",
        f"Com plano de saúde: {plano:.1f}% ({fmt(qtd_plano)} moradores)",
        f"Utilizaram serviço de saúde: {atendimento:.1f}%",
        f"Idade média: {media:.1f} anos",
        f"Idade mediana: {mediana:.1f} anos"
    ]

    for lab, txt in zip(labels, textos):
        lab.config(text=txt)

    desenhar_grafico_plano(df, df_comp)
    desenhar_grafico_idade(df)
    atualizar_ranking()

    status.config(text=f"Atualizado — {fmt(total)} moradores exibidos.")

def limpar():
    """Limpa os filtros."""
    combo_ra.current(0)
    combo_comp.current(0)
    atualizar()
    status.config(text="Filtros limpos.")

def exportar_csv():
    """Exporta dados filtrados para CSV."""
    df = filtrar()

    caminho = filedialog.asksaveasfilename(
        title="Salvar CSV",
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv")]
    )

    if caminho:
        df.to_csv(caminho, sep=";", index=False, encoding="utf-8-sig")
        messagebox.showinfo("Sucesso", "CSV exportado com sucesso!")
        status.config(text=f"CSV exportado: {caminho}")

def exportar_txt():
    """Exporta estatísticas para TXT."""
    df = filtrar()
    total, plano, atendimento, media, mediana, qtd_plano = estatisticas(df)

    caminho = filedialog.asksaveasfilename(
        title="Salvar TXT",
        defaultextension=".txt",
        filetypes=[("TXT", "*.txt")]
    )

    if caminho:
        with open(caminho, "w", encoding="utf-8") as arq:
            arq.write("Sistema PDAD 2024 — Saúde\n")
            arq.write("=" * 35 + "\n\n")
            arq.write(f"RA principal: {combo_ra.get()}\n")
            arq.write(f"Comparação: {combo_comp.get()}\n\n")
            arq.write(f"Total: {total}\n")
            arq.write(f"Com plano: {plano:.1f}%\n")
            arq.write(f"Usaram serviço de saúde: {atendimento:.1f}%\n")
            arq.write(f"Idade média: {media:.1f}\n")
            arq.write(f"Idade mediana: {mediana:.1f}\n\n")
            arq.write("Valores sentinela 88888 e 99999 foram removidos.\n")
            arq.write("Foi usado merge entre moradores e domicílios.\n")
            arq.write("O ranking foi ordenado manualmente com Bubble Sort.\n")

        messagebox.showinfo("Sucesso", "TXT exportado com sucesso!")
        status.config(text=f"TXT exportado: {caminho}")

btn_atualizar.config(command=atualizar)
btn_limpar.config(command=limpar)
btn_csv.config(command=exportar_csv)
btn_txt.config(command=exportar_txt)
combo_ra.bind("<<ComboboxSelected>>", lambda e: atualizar())
combo_comp.bind("<<ComboboxSelected>>", lambda e: atualizar())
atualizar()
janela.mainloop()
