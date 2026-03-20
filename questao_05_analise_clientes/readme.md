# ✦ Questão 05 - Análise de Clientes 👥    

O objetivo dessa questão é mapear os **clientes fiéis da LH Nautical**. O cliente fiel é aquele que possui um gasto médio alto por transação e navega por diversas categorias da loja.


## ⮞ Premissas Obrigatórias 

- **Faturamento Total:** Soma da coluna total por cliente.
- **Frequência:** Contagem total de transações (IDs de venda) por cliente.
- **Ticket Médio:** Faturamento Total / Frequência.
- **Diversidade de Categorias:** Quantidade de categorias distintas que o cliente comprou.
- **Nota:** É necessário limpar os nomes das categorias no arquivo [produtos_raw.csv](../datasets/produtos_raw.csv) 
- **Filtro de Elite:** Apenas clientes que compraram produtos de **3 ou mais categorias distintas** devem ser considerados no ranking.
- **Desempate:** Em caso de empate no Ticket Médio, utilize o **id_cliente em ordem crescente**.

**Obs:** Essas premissas foram realizadas nos seguintes arquivos:
- [query.py](./artefatos/query.py): construção das queries de resultados.
- [script.py](./artefatos/script.py): manipulações e merges das bases de dados utilizadas.
 
### 🏷️ Ranking de clientes

- **Limpeza das categorias de produtos**:
    ```python
    # utilização do map para agrupar as categorias
    products["actual_category"] = products["actual_category"].map(
        lambda x: "Eletrônicos" if "eletr" in x else (
            "Propulsão" if "prop" in x else (
                "Ancoragem" if "ncora" in x else "Outros"
            )
        )
    )
    ```

- **Cálculo do Ticket Médio e da diversidade de Categorias para cada cliente**

- **Quais são os 10 clientes com maior Ticket médio que estão em 3 ou mais categorias?**

    Para a realização das duas tarefas acima, foi necessário transformar o json de clientes para um dataframe, realizar o merge com dataset de vendas e posteriormente, com o dataset de produtos. Dessa forma, obtém-se um dataset completo, onde é possível realizar a seguinte query:

    ```sql
    -- products_sales representa a base de dados 'mergeada'
    SELECT 
        id_client,
        ROUND(SUM(total), 2) AS annual_revenue,
        COUNT(DISTINCT(id)) AS frequency,
        ROUND((SUM(total) / COUNT(DISTINCT(id))), 2) AS mean_ticket,
        COUNT(DISTINCT(actual_category)) AS diversity
    FROM products_sales
    GROUP BY id_client
    HAVING diversity >= 3
    ORDER BY mean_ticket DESC, id_client ASC
    LIMIT 10;
    ```

### 🏷️ Para este grupo específico de 10 clientes, identifique qual categoria de produto concentra a maior quantidade total de itens comprados (sum(qtd)).

```sql
SELECT
    actual_category,
    SUM(qtd) AS items_bought_qnt
FROM products_sales
WHERE id_client IN (
    SELECT 
        id_client
    FROM products_sales
    GROUP BY id_client
    HAVING COUNT(DISTINCT actual_category) >= 3
    ORDER BY (SUM(total) / COUNT(DISTINCT id)) DESC, id_client ASC
    LIMIT 10
)
GROUP BY actual_category
ORDER BY items_bought_qnt DESC;
```
A query acima retorna que a seguinte tabela:

| Categoria | # itens comprados |
| :--- | :--- |
| Propulsão | 6030 |
| Ancoragem | 5632 |
| Eletrônicos | 5214 |

Observa-se que a categoria **Propulsão** é que concentra o maior volume de itens comprados pela elite, seguido por ancoragem e eletrônicos.

### 🏷️ Interpretação

#### Como foi realizada a limpeza das categorias?
A estratégia utilizada para tratar as categorias de produtos foi a **normalização por mapeamento de padrões**. Mesmo que as categorias possuam erros de digitação, variação de caixa e espaçamentos, ao converter todas as strings para minúsculas e remover espaços em branco excedentes, foi possível perceber um padrão de escrita em cada tipo de categoria.

Em vez de uma limpeza manual, foi utilizado uma lógica de **busca por substrings**.
- Variações contendo `'eletr'` foram mapeadas para a categoria **Eletrônicos**
- Variações contendo `'prop'` foram mapeadas para a categoria **Propulsão**
- Variações contendo `'ncora'`foram mapeadas para a categoria **Ancoragem**

#### Qual lógica foi utilizada para filtrar os clientes com diversidade mínima?
Primeiramente, é importante ressaltar que para obter esse insight, é necessário que as dimensões de **vendas, clientes e produtos** sejam consolidades através de um merge.

Com essa nova base, ao aplicar um agrupamento por `id_client`, basta combinar a função `COUNT()` com o atributo `DISTINCT` em SQL (*COUNT(DISTINCT actual_category) AS diversity*). Dessa forma, pode-se utilizar essa nova coluna criada para definir explicitamente que queremos no filtro de elite apenas aqueles clientes que apresentam movimentações em 3 ou mais categorias únicas.

#### Como foi garantido que a contagem de itens refletisse apenas os Top 10?

Para garantir que essa operação fosse realizada corretamente, a ideia é utilizar o resultado do ranking do Ticket Médio dentro de uma **subquery**. Essa subquery é parte da query que compõe o Top 10, isto é, o **agrupamento por id_client**, respeitando a **diversidade mínima** e o **desempate**. Após essa identificação, volta-se novamente a base de dados na query principal, extraindo apenas as linhas de consumo que pertencem aos 10 perfis encontrados. A soma da coluna `qtd` através de um **agrupamento da categoria** fornece com precisão, qual categoria é mais vendida no ranking de elite.