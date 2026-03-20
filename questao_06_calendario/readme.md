# ✦ Questão 06 - Dimensão de Calendário 🗓️

Nesta questão, ao construir uma dimensão de calendário buscamos saber: **"Qual é o dia da semana que tem-se a pior média de vendas?"**. Esse conhecimento impacta a decisão de se vale a pena ou não, fechar a loja nos dias de baixa venda.

## ⮞ Premissas Obrigatórias 

- O período de análise deve considerar **todas as datas entre a menor e a maior** `data_venda` presentes no arquivo.
- A loja esteve aberta em **todos os dias** do período (inclusive fins de semana).
- Dias sem registro na tabela de vendas devem ser considerados como **valor_venda = 0**.
- “Vendas diárias” correspondem à **soma de valor_venda por dia**.
- A média de vendas por dia da semana deve considerar **todos os dias do calendário**, inclusive os dias sem venda.
- O nome do dia da semana deve ser apresentado em **português** (Segunda-feira, Terça-feira, etc.).

**Obs:** A query foi construída no arquivo [query.py](./artefatos/query.py) gerando o resultado descrito na [Tabela de receita média pra cada dia da semana](./artefatos/media_receita_dias_semana.csv).

### 🏷️ Construa uma dimensão de datas utilizando sql

```sql
-- recursive CTE to get the all dates
WITH 
    RECURSIVE dim_calendar AS (
        SELECT MIN(sale_date) AS base_date
        FROM sales
        
        UNION ALL
        
        SELECT base_date + INTERVAL 1 DAY
        FROM dim_calendar
        WHERE base_date < (SELECT MAX(sale_date) FROM sales)
    )
```
A dimensão de datas consistiu em uma CTE que utiliza como base as datas mínima e máxima da tabela de vendas. Posteriomente, na query principal, o código é extraído

### 🏷️ Cruze a dimensão de datas com a tabela de vendas para análise (não esqueça de considerar os dias sem vendas).

```sql
-- calculates the revenue of each day that had sales
daily_sales AS (
    SELECT 
        sale_date,
        SUM(total) AS daily_revenue
    FROM sales
    GROUP BY sale_date
),

-- brings the complete calendar and get the week days codes
calendar_sales AS (
    SELECT
        dc.base_date,
        EXTRACT(DOW FROM dc.base_date) AS day_code,
        COALESCE(ds.daily_revenue, 0) AS real_revenue -- replace null values of daily_revenue with 0
    FROM dim_calendar dc
    LEFT JOIN daily_sales ds
    ON dc.base_date = ds.sale_date
)
```

### 🏷️ Qual dia da semana apresenta a menor média de vendas histórica, e qual é o valor dessa média?

| Dia da semana | Média de faturamento |
| :--- | :--- |
| Segunda-feira | 3.285.975,58 |
| Domingo | 3.366.781,09 |
| Quinta-feira | 3.560.174,45 |
| Quarta-feira | 3.649.345,28 |
| Sexta-feira | 3.651.962,65 |
| Sábado | 3.667.602,92 |
| Terça-feira | 3.816.335,14 |

A tabela acima ilustra o resultado da query obtida. É possível notar que **Segunda-feira** é o dia mais fraco de vendas da LH Nauticals, performando cerca de **R$530 mil a menos** que a Terça-feira (o melhor dia de vendas), por dia. Portanto, para reduzir custos operacionais, a Segunda-feira é o melhoe dia para fechar a loja.

### 🏷️ Interpretação:

- **Por que é necessário utilizar uma tabela de datas (calendário) em vez de agrupar diretamente a tabela de vendas?**

    Criar a dimensão de datas é o que garante a **integridade temporal**, pois a tabela de vendas apenas registr dias em que a loja operou e fez vendas. O erro que o estagiário cometeu de agrupar diretamente pela tabela de vendas gera uma **média incoerente**, que não demonstra o cenário real por não considerar a verdadeira produtividade da loja.
    
- **O que aconteceria com a média de vendas se um dia da semana tivesse muitos dias sem nenhuma venda registrada?**

    Ao ignorar dias que a loja não funcionou, ou não tiveram vendas, a **média fica extremamente inflada** demonstrando um valor que não corresponde ao cenário real da LH Nauticals. A média é uma métrica sensível a discrepância de valores, portanto, se os **zeros**, que correspondem a dias sem venda, não forem contabilizados no cálculo da média, o Sr. Almir pode se enganar com dias que não valem a pena deixar a loja aberta, gerando grande prejuízo operacional.
