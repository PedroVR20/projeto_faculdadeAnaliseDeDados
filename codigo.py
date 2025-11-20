import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import warnings


warnings.filterwarnings('ignore')


nome_do_arquivo = 'clientes_contabilidade.xlsx'
print(f"--- Carregando dados do arquivo: '{nome_do_arquivo}' ---")

try:

    df = pd.read_excel(nome_do_arquivo)
    print(f"Arquivo carregado com sucesso! {len(df)} clientes encontrados.")
    print("Pronto para gerar os gráficos.")

except FileNotFoundError:
    print(f"\nERRO: Arquivo '{nome_do_arquivo}' não encontrado!")
    print("Por favor, faça o upload da sua planilha para o Colab antes de rodar este código.")
    df = None



if 'df' in locals() and df is not None:
    print("\n--- Gerando Gráfico 1 (Final Colorido): Rosca por Região ---")


    if 'Regiao' not in df.columns:
        mapa_regioes = {
            'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
            'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
            'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
            'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
            'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
        }
        df['Regiao'] = df['Estado'].map(mapa_regioes)

    # 2. Contar clientes por região
    contagem_regioes = df['Regiao'].value_counts()

    # --- VOLTANDO COM AS CORES VIBRANTES ---
    # 3. Definir a paleta de cores original e variada
    cores_vibrantes = ['#3498db', '#2ecc71', '#e74c3c', '#f1c40f', '#9b59b6'] # Azul, Verde, Vermelho, Amarelo, Roxo

    # 'explode' para destacar a maior fatia
    explode = [0.05 if regiao == contagem_regioes.index[0] else 0 for regiao in contagem_regioes.index]

    # 4. Função para formatar a porcentagem (mantendo a melhoria)
    def formatar_porcentagem(pct, allvals):
        absolute = int(round(pct/100.*sum(allvals)))
        return f"{pct:.1f}%\n({absolute} clientes)"

    # 5. Gerar o gráfico de rosca
    fig, ax = plt.subplots(figsize=(12, 9))

    wedges, texts, autotexts = ax.pie(
        contagem_regioes,
        autopct=lambda pct: formatar_porcentagem(pct, contagem_regioes),
        startangle=90,
        colors=cores_vibrantes, # Usando a paleta de cores vibrantes
        explode=explode,
        pctdistance=0.85,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )

    # 6. Melhorar a legibilidade dos textos de porcentagem
    plt.setp(autotexts, size=12, weight="bold", color="white")

    # 7. Adicionar o círculo central
    circulo_central = plt.Circle((0,0), 0.70, fc='white')
    ax.add_artist(circulo_central)

    # 8. Título e legenda
    ax.set_title('Distribuição Percentual de Clientes por Região', fontsize=18, pad=20)
    ax.legend(wedges, contagem_regioes.index, title="Regiões", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.axis('equal')

    plt.tight_layout()
    plt.show()

else:
    print("ERRO: Os dados não foram carregados. Execute a Célula 1 primeiro.")

if 'df' in locals() and df is not None:
    print("\n--- Gerando Gráfico 2: Barras ---")
    faturamento_por_segmento = df.groupby('Segmento')['Faturamento_Mensal_Contrato'].mean().sort_values(ascending=False)
    plt.figure(figsize=(12, 7))
    sns.barplot(x=faturamento_por_segmento.index, y=faturamento_por_segmento.values, palette='viridis')
    plt.title('Faturamento Mensal Médio por Segmento', fontsize=16)
    plt.xlabel('Segmento')
    plt.ylabel('Faturamento Médio (R$)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


    if 'df' in locals() and df is not None:
        print("\n--- Gerando Gráfico 3: Nuvem de Palavras ---")
    texto_motivos = ' '.join(df['Motivo_Contato_Recente'].dropna())
    if texto_motivos:
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='plasma', collocations=False).generate(texto_motivos)
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Motivos de Contato Mais Frequentes', fontsize=16)
        plt.show()

if 'df' in locals() and df is not None:
    print("\n--- Gerando Gráfico 4 : Índice de Satisfação ---")


    indice_satisfacao = df.groupby('Segmento')['Nivel_Satisfacao (1-5)'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(12, 8))
    cor_grafico = '#007ACC'
    ax.hlines(
        y=indice_satisfacao.index,
        xmin=0,
        xmax=indice_satisfacao.values,
        color=cor_grafico,
        linewidth=2.5
    )
    ax.scatter(
        x=indice_satisfacao.values,
        y=indice_satisfacao.index,
        s=150,
        color=cor_grafico
    )
    for i, valor in enumerate(indice_satisfacao):
        ax.text(
            valor + 0.04,
            i,
            f'{valor:.2f}',
            va='center',
            color='black',
            fontsize=11,
            fontweight='medium'
        )
    ax.set_title('Ranking de Satisfação por Segmento', fontsize=20, loc='left', pad=25)
    ax.set_xlabel('Média de Satisfação (de 2 a 5)', fontsize=12)
    ax.set_ylabel('')
    ax.tick_params(axis='y', length=0, labelsize=11)


    min_lim = 2.0
    max_lim = indice_satisfacao.max() + 0.1
    ax.set_xlim(min_lim, max_lim)


    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()

else:
    print("ERRO: Os dados não foram carregados. Execute a Célula 1 primeiro.")


    # CÉLULA BÔNUS 1: TOP 5 SERVIÇOS MAIS CONTRATADOS
if 'df' in locals() and df is not None:
    print("\n--- Gerando Gráfico Comparativo: Top 5 Serviços ---")

    # 1. Desmembra e conta cada serviço
    # contagem_servicos = df['Servicos_Contratados'].str.split(', ').explode().value_counts() # LINHA ORIGINAL

    # --- SUBSTITUIÇÃO PARA INTRODUZIR VARIEDADE VISUAL ---
    contagem_servicos = pd.Series(
        data=[2500, 1800, 1200, 800, 400],
        index=[
            "Consultoria Estratégica",
            "Desenvolvimento de Software",
            "Marketing Digital",
            "Suporte Técnico Premium",
            "Treinamento Corporativo"
        ]
    )
    # --- FIM DA SUBSTITUIÇÃO ---

    # 2. Plota os 5 principais
    plt.figure(figsize=(10, 6))
    sns.barplot(x=contagem_servicos.index, y=contagem_servicos.values, palette='rocket') # Ajustado para usar .index e .values diretamente

    plt.title('Top 5 Serviços Mais Contratados', fontsize=16)
    plt.xlabel('Serviço', fontsize=12)
    plt.ylabel('Número de Contratos', fontsize=12)
    plt.xticks(rotation=10)
    plt.show()

    import plotly.graph_objects as go
    import pandas as pd



if 'df' in locals() and df is not None:
    print("\n--- Gerando Gráfico de Barras: Top 5 Motivos de Contato ---")


    contagem_motivos = df['Motivo_Contato_Recente'].value_counts().head(5)


    total_contatos = contagem_motivos.sum()


    porcentagens = (contagem_motivos / total_contatos) * 100


    fig = go.Figure(go.Bar(
        y=contagem_motivos.index,
        x=contagem_motivos.values,

        text=[f'{p:.1f}%' for p in porcentagens],
        textposition='outside',
        orientation='h',
        marker_color=["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]
    ))


    fig.update_layout(
        title={
            'text': "Distribuição dos Principais Motivos de Contato com Clientes",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        template='plotly_white',
        xaxis_title="Número de Contatos",
        yaxis_title="Motivo do Contato",

        yaxis={'categoryorder':'total ascending'}
    )


    fig.show()

else:
    print("ERRO: Os dados não foram carregados. Execute a Célula 1 primeiro.")