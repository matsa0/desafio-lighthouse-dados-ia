# 🏁🎯 Desafio Técnico - LH Nauticals
### Processo Seletivo: Lighthouse Indicium

---

## 📌 Visão Geral do Projeto
Este repositório contém a solução analítica para o desafio técnico da LH Nauticals, desenvolvido como parte do processo seletivo do programa Lighthouse da Indicium. O projeto consiste na extração, tratamento e análise de dados, resultando em um **Dashboard** interativo projetado para apoiar a tomada de decisão.

A análise foi estruturada em quatro pilares principais:
1. **Desempenho de Vendas:** Mapeamento da evolução temporal do faturamento e identificação de sazonalidades (receita por dia da semana).
2. **Análise de Prejuízos:** Identificação e ranqueamento de produtos ofensores à margem financeira da empresa.
3. **Previsão de Demanda:** Comparativo histórico entre o volume real e a previsão do modelo para janeiro de 2024, mensurado através do Erro Médio Absoluto (MAE).
4. **Comportamento e Recomendação de Clientes:** Cruzamento de dados transacionais com CRM para traçar o perfil de clientes de elite (Ticket Médio, Frequência, Diversidade) e construção de um sistema de recomendação de produtos baseado em Similaridade de Cosseno.

### 🔴 Clique [aqui](https://youtu.be/Vi4QhS4UWQc) para ver o vídeo de apresentação do dashboard
---

## 🛠️ Ferramentas Utilizadas
* **Linguagem:** Python 3.11
* **Manipulação de Dados:** Pandas, DuckDB e Requests
* **Visualização:** Plotly Express, Seaborn
* **Métricas Estatísticas:** Scikit-learn (Similaridade de Cosseno, Erro Médio Absoluto)
* **Desenvolvimento Web/Interface:** Streamlit
* **Ambiente virtual**: Miniconda

---

## 🚀 Como rodar o projeto

```bash
# clone o repositório
git clone https://github.com/matsa0/desafio-lighthouse-dados-ia.git

# instale as dependências 
pip install -r requirements.txt
```

---

## 📁 Estrutura de Pastas
A arquitetura do repositório reflete a divisão das etapas lógicas do desafio, separando a camada de dados brutos dos artefatos processados e da interface final.

```text
├── datasets/                                 # Arquivos CSV e JSON fornecidos pelo desafio
├── questao_01_EDA/                           # Artefatos processados: queries que fornecem uma EDA básica
│   ├── artefatos/                            
│   └── README.md
├── questao_02_produtos/                      # Artefatos processados: manipulação de categorias dos produtos
│   ├── artefatos/
│   └── README.md
├── questao03_custos/                         # Artefatos processados: trabalho com JSON de custos de importação
│   ├── artefatos/
│   └── README.md
├── questao_04_dados_publicos/                # Artefatos processados: produtos com prejuízo
│   ├── artefatos/
│   └── README.md
├── questao_05_analise_clientes/              # Artefatos processados: ranking de clientes e categorias
│   ├── artefatos/
│   └── README.md
├── questao_06_calendario/                    # Artefatos processados: sazonalidade e receita por dia
│   ├── artefatos/
│   └── README.md
├── questao_07_previsao_demanda/              # Artefatos processados: histórico vs previsão (Jan/2024)
│   ├── artefatos/
│   └── README.md
├── questao_08_analise_clientes/              # Artefatos processados: matriz de similaridade de cosseno
│   ├── artefatos/
│   └── README.md
├── dashboard/                                # Artefatos processados: código do dashboard construído com streamlit
│   ├── artefatos/
│   └── README.md                             # Script principal da aplicação (UI/Front-end)
├── requirements.txt                          # Mapeamento de dependências do ambiente
└── README.md                                 # Documentação do repositório