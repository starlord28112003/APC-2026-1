import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
