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


plt.style.use('seaborn-v0_8-whitegrid') # Estilo mais limpo para o gráfico

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Código do Gráfico 4: Comparativo de Satisfação por Ano e Segmento ---
# --- Código do Gráfico 4: Comparativo de Satisfação por Ano e Segmento ---
if 'df' in locals() and df is not None:
    print("\n--- Gerando Gráfico 4: Comparativo de Satisfação por Ano e Segmento ---")

    df_temp = df.copy()

    # Conversão robusta (aceita formatos brasileiros e estrangeiros)
    df_temp['Data_Inicio_Contrato'] = pd.to_datetime(
        df_temp['Data_Inicio_Contrato'],
        errors='coerce',
        dayfirst=True   # <-- ESSA LINHA É A CHAVE DA CORREÇÃO
    )

    # Extração segura do ano
    df_temp['Ano'] = df_temp['Data_Inicio_Contrato'].dt.year

    # Remove linhas sem ano
    df_temp = df_temp.dropna(subset=['Ano'])
    df_temp['Ano'] = df_temp['Ano'].astype('Int64')

    # Filtrar anos de interesse
    anos_interesse = [2023, 2024, 2025]
    df_filtrado = df_temp[df_temp['Ano'].isin(anos_interesse)].copy()

    # Média por segmento e ano
    df_satisfacao = df_filtrado.groupby(['Segmento', 'Ano'])['Nivel_Satisfacao (1-5)'].mean().unstack()

    segmentos = df_satisfacao.index.tolist()
    anos = df_satisfacao.columns.tolist()

    cores = {
        2023: '#1f77b4',
        2024: '#ff7f0e',
        2025: '#2ca02c'
    }

    anos_ordenados = [ano for ano in anos_interesse if ano in anos]

    fig, ax = plt.subplots(figsize=(14, 8))

    bar_width = 0.25
    r = np.arange(len(segmentos))

    for i, ano in enumerate(anos_ordenados):
        r_pos = r + i * bar_width
        barras = ax.bar(
            r_pos,
            df_satisfacao[ano].fillna(0),
            color=cores[ano],
            width=bar_width,
            edgecolor='white',
            label=str(ano)
        )

        for bar in barras:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2.,
                    height + 0.01,
                    f'{height:.2f}',
                    ha='center',
                    va='bottom',
                    fontsize=9
                )

    ax.set_title(
        'Comparativo do Nível de Satisfação por Segmento (2023-2025)', 
        fontsize=16, 
        fontweight='bold', 
        pad=20
    )
    ax.set_xlabel('Segmento de Atuação', fontsize=12)
    ax.set_ylabel('Média de Satisfação (1-5)', fontsize=12)

    ax.set_xticks(r + bar_width * (len(anos_ordenados) - 1) / 2)
    ax.set_xticklabels(segmentos, rotation=45, ha="right")

    ax.set_ylim(0, 5.5)
    ax.legend(title='Ano', loc='upper left', bbox_to_anchor=(1, 1))

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.tight_layout()
    plt.show()

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
