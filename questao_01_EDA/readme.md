# ✦ Questão 01 - Análise Exploratória dos Dados 🕵️‍♀️

A missão dessa primeira questão é realizar uma EDA (*Exploratory Data Analysis*) sob a base de dados de [Vendas de 2023/2024](../datasets/vendas_2023_2024.csv). A EDA  é um passo fundamental ao se trabalhar com dados, pois é nessa etapa que se adquire **conhecimento** a respeito da base de dados que se irá trabalhar. Isso é de extrema importância para que decisões a respeito das etapas de tratamento, modelagem, um possível treinamento de modelos machine learning ou extração de insights BI sejam feitos da melhor forma possível. 

Nesse caso, é necessário verificar se podemos confiar nos dados de Vendas para tomar decisões de negócios. Por isso, abaixo, foi realizada uma série de tarefas que nos permite entender a base de dados, respondendo perguntas importantes. 

**Obs:** Essa análise exploratória foi realizada no arquivo [query.py](./artefatos/query.py), onde as queries foram testadas e os valores foram obtidos.

## ⮞ Premissas Obrigatórias

### 🏷️ Visão geral do dataset 

```sql
    --- Número de linhas da tabela de vendas
    SELECT COUNT(*) AS num_rows 
    FROM sales

    -- Número de linhas da tabela de vendas
    SELECT COUNT(*) AS num_cols
    FROM information_schema.columns
    WHERE table_name = 'sales'

    -- Cálculo do intervalo de datas
    ALTER TABLE sales
    ALTER sale_date TYPE DATE USING sale_date::DATE; 
    
    SELECT 
        MAX(sale_date) - MIN(sale_date) AS date_interval
    FROM sales
```

### 🏷️ Análise de valores numéricos (total)

```sql
    SELECT 
        -- Análises Obrigatórias
        MIN(total) AS min_total,
        SELECT MAX(total) AS max_total,
        ROUND(AVG(total), 2) AS mean_total,
        -- 🌟 Bônus
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total) AS median_total,
        ROUND(STDDEV(total), 2) AS std_total
    FROM sales
```

### 🏷️ Interpretação

- **Possíveis outliers na coluna (total):** Considerando que o valor **mínimo** da coluna total é de `294,50` e que o valor **máximo** é `2.222.973`, percebe-se uma discrepância bem grande entre os extremos. Olhando para o valor da média de `263.797,83`, é possível perceber outra discrepância em relação ao valor máximo, o que indica, em uma métrica **sensível**, que valores altos estão puxando o seu valor para cima, sendo considerado um clássico exemplo de uma **distribuição de cauda longa(assimétrica) para a direita**.

    Nesses casos, é muito interessante que se analise a **mediana** também, que aqui, tem o valor de `82.225`. Ela confirma a hipótese da distribuição assimétrica, pois a média é pelo menos **3x maior** que o seu valor, indicando que valores altos a distorcem. Adicionalmente, o valor do **desvio padrão** é de `390.007,18`, sendo maior que a própria média, apontando volatilidade e alta dispersão dos dados, o que confirma mais uma vez a presença de outliers.

- **Qualidade dos dados**: A base de dados não possui valores nulos e nem duplicados, o que é um ótimo sinal de integridade. Porém, a coluna `sale_date` apresenta inconsistência em seu tipo, estando armazenada como `VARCHAR` em vez de `DATE`, permitindo a presença de diversos tipos de formatações de data (ex: dd-MM-yyyy e yyyy-MM-dd), impedindo análises e operações. A query exemplifica o que foi explicado, através do retorno do seguinte erro:
    
    ```text
    Conversion Error: invalid date field format: "15-09-2024", expected format is (YYYY-MM-DD)
    ```
- **Conclusão:** O dataset apresenta boa integridade de dados, mas necessita de uma investigação apurada dos *outliers* apresentados na coluna `total`, a fim de identificar se são vendas reais, ou erros de cálculo/digitação e se valem a pena mantê-los na base. Além disso, é preciso tratar a coluna `sale_date` ao converter o seu formato para `DATE` e ajustar os seus registros para o padrão ISO 8601 (**yyyy-MM-dd**) para que a análise temporal se torne viável.