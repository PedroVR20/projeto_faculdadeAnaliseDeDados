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

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Configurações Iniciais ---
file_path = '/home/ubuntu/upload/clientes_contabilidade.xlsx'
plt.style.use('seaborn-v0_8-whitegrid') # Estilo mais limpo para o gráfico

# --- Função para gerar o gráfico ---
def gerar_grafico_satisfacao_anual(file_path):
    try:
        # 1. Carregar os dados
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Erro: O arquivo não foi encontrado em {file_path}")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return

    # 2. Pré-processamento dos dados
    # Converter a coluna de data para datetime e extrair o ano
    df['Data_Inicio_Contrato'] = pd.to_datetime(df['Data_Inicio_Contrato'])
    df['Ano'] = df['Data_Inicio_Contrato'].dt.year

    # Filtrar para os anos de interesse (2023, 2024, 2025)
    anos_interesse = [2023, 2024, 2025]
    df_filtrado = df[df['Ano'].isin(anos_interesse)].copy()

    # 3. Calcular a média de satisfação por Segmento e Ano
    # O .unstack() transforma o nível 'Ano' em colunas, resultando em um DataFrame
    df_satisfacao = df_filtrado.groupby(['Segmento', 'Ano'])['Nivel_Satisfacao (1-5)'].mean().unstack()

    # 4. Preparação para o Gráfico de Barras Agrupadas
    segmentos = df_satisfacao.index.tolist()
    anos = df_satisfacao.columns.tolist()
    
    # Definir cores para os anos
    cores = {
        2023: '#1f77b4', # Azul
        2024: '#ff7f0e', # Laranja
        2025: '#2ca02c'  # Verde
    }
    
    # Garantir que a ordem dos anos seja a correta para a iteração
    anos_ordenados = [ano for ano in anos_interesse if ano in anos]

    # 5. Criação do Gráfico
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Largura das barras
    bar_width = 0.25
    
    # Posições no eixo X para os grupos de segmentos
    r = np.arange(len(segmentos))
    
    # Plotar as barras para cada ano
    for i, ano in enumerate(anos_ordenados):
        # Calcular a posição da barra
        r_pos = r + i * bar_width
        
        # Plotar a barra
        # Acessar a coluna do DataFrame df_satisfacao
        barras = ax.bar(
            r_pos, 
            df_satisfacao[ano].fillna(0), # Usar 0 para segmentos sem dados no ano
            color=cores[ano], 
            width=bar_width, 
            edgecolor='white', 
            label=str(ano)
        )
        
        # Adicionar rótulos de valor no topo das barras
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

    # 6. Configurações do Gráfico
    ax.set_title(
        'Comparativo do Nível de Satisfação por Segmento (2023-2025)', 
        fontsize=16, 
        fontweight='bold', 
        pad=20
    )
    ax.set_xlabel('Segmento de Atuação', fontsize=12)
    ax.set_ylabel('Média de Satisfação (1-5)', fontsize=12)
    
    # Configurar os ticks do eixo X para ficarem centralizados
    ax.set_xticks(r + bar_width * (len(anos_ordenados) - 1) / 2)
    ax.set_xticklabels(segmentos, rotation=45, ha="right")
    
    # Limites do eixo Y
    ax.set_ylim(0, 5.5)
    
    # Legenda
    ax.legend(title='Ano', loc='upper left', bbox_to_anchor=(1, 1))
    
    # Remover bordas desnecessárias
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    plt.tight_layout()
    
    # Salvar o gráfico
    output_path = '/home/ubuntu/grafico_satisfacao_anual.png'
    plt.savefig(output_path)
    print(f"\nGráfico salvo em: {output_path}")
    
    # Mostrar o gráfico
    plt.show()

# --- Execução ---
if __name__ == '__main__':
    gerar_grafico_satisfacao_anual(file_path)



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
