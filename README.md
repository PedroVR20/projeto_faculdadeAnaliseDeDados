# 📊 Análise de Dados de Clientes para Consultoria Contábil

Este projeto visa demonstrar a aplicação de técnicas de **Análise Exploratória de Dados (EDA)** e **Visualização de Dados** utilizando a linguagem Python e suas principais bibliotecas. O foco é extrair *insights* valiosos a partir de dados de clientes de uma empresa de contabilidade, auxiliando na tomada de decisões estratégicas.

## 🚀 Tecnologias Utilizadas

O projeto é construído sobre um *stack* robusto de análise de dados em Python:

| Tecnologia | Função Principal |
| :--- | :--- |
| **Python** | Linguagem de programação principal. |
| **Pandas** | Manipulação, limpeza e pré-processamento de dados. |
| **Seaborn** | Geração de gráficos estatísticos informativos. |
| **Matplotlib** | Customização e criação de visualizações detalhadas. |
| **WordCloud** | Visualização de frequência de texto (motivos de contato). |

## ⚙️ Estrutura do Projeto

O repositório contém os seguintes arquivos:

| Arquivo | Descrição |
| :--- | :--- |
| `codigo.py` | O *script* principal que carrega os dados, realiza o pré-processamento e gera todas as visualizações. |
| `clientes_contabilidade.xlsx` | O conjunto de dados de exemplo contendo informações sobre os clientes (segmento, faturamento, região, satisfação, etc.). |
| `README.md` | Este arquivo de documentação. |

## 📈 Visualizações Geradas

O *script* `codigo.py` gera as seguintes análises visuais:

1.  **Distribuição Percentual de Clientes por Região:** Gráfico de Rosca que mostra a concentração de clientes por região geográfica.
2.  **Faturamento Mensal Médio por Segmento:** Gráfico de Barras que compara o faturamento médio dos contratos entre os diferentes segmentos de mercado.
3.  **Motivos de Contato Mais Frequentes:** Nuvem de Palavras que destaca os temas mais recorrentes nos contatos recentes dos clientes.
4.  **Ranking de Satisfação por Segmento:** Gráfico de Pontos (Dumbbell Plot) que exibe o índice médio de satisfação dos clientes, segmentado por área de atuação.
5.  **Top 5 Serviços Mais Contratados:** Gráfico de Barras que ilustra a popularidade dos serviços oferecidos pela contabilidade.
6.  **Top 5 Motivos de Contato:** G´rafico de Barras que ilustra a popularidade dos Motivos de Contato.

## 💻 Como Executar o Projeto

Para rodar o projeto em sua máquina ou ambiente de desenvolvimento (como Google Colab ou Jupyter Notebook), siga os passos abaixo:

### Pré-requisitos

Certifique-se de ter o Python instalado e as seguintes bibliotecas:

```bash
pip install pandas openpyxl matplotlib seaborn wordcloud
```

### Execução

1.  Clone o repositório para sua máquina local:
    ```bash
    git clone https://github.com/PedroVR20/projeto123.git
    cd projeto123
    ```
2.  Certifique-se de que o arquivo de dados (`clientes_contabilidade.xlsx`) esteja no mesmo diretório que o *script* `codigo.py`.
3.  Execute o *script* Python:
    ```bash
    python codigo.py
    ```

O *script* carregará os dados e exibirá as quatro visualizações geradas.

## 🤝 Contribuição

Este projeto foi desenvolvido por:

*   **[Pedro Valim Rivera]** - Papel: Analista de Dados / Engenheiro de Dados
*   **[Erik Figueiredo]** - Papel: Cientista de Dados / Pesquisador
*   **[Davi De Lima Martins]** - Papel: Especialista em Otimização e Entrega

Sinta-se à vontade para sugerir melhorias ou reportar problemas.


