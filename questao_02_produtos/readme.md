# ✦ Questão 02 - Trabalhando com produtos 🛒

Nessa tarefa, é necessário trabalhar com a normalização dos dados do dataset de [Produtos](../datasets/produtos_raw.csv) com Pyhton! A normalização, padronização e limpeza são etapas fundamentais que garantem integridade e consistência para os dados que dessejamos trabalhar. Portanto, nessa questão, iremos trabalhar com a biblioteca **Pandas** as seguintes tarefas:

## ⮞ Premissas Obrigatórias

- Utilize apenas o CSV [produtos_raw.csv](../datasets/produtos_raw.csv)
- Utilize obrigatoriamente Python 3 (nesse caso, **Python 3.11** em um ambiente virtual conda)

**Obs:** Essa limpeza foi realizada no arquivo [script.py](./artefatos/script.py), onde os códigos foram testados e validados.
 

### 🏷️ Padronização das categorias
Nessa tarefa, é necessário realizar um agrupamento das categorias de produtos em **eletrônicos, propulsão e ancoragem**, o que permite que a variável seja entendida mais facilmente e também que sua dimensionalidade seja reduzida.

```python
# mapeia as ocorrências de 'actual_category' em novas categorias
produtos["actual_category"] = produtos["actual_category"].map(
    lambda x: "Eletrônicos" if "eletr" in x else (
        "Propulsão" if "prop" in x else (
            "Ancoragem" if "ncora" in x else "Outros"
        )
    )
)

produtos["actual_category"].value_counts()
```

**O output obtido:**
```text
actual_category
Propulsão      53
Ancoragem      53
Eletrônicos    51
```

A utilização do `map()` em conjunto com a função **lambda** é interessante por conta da sua legibilidade e flexibilidade lógica. Essa função tem um ótimo desempenho para datasets pequenos, mas em caso de datasets maiores, é mais interessante utilizar uma abordagem vetorizada com `numpy select`, por exemplo.

### 🏷️ Conversão dos valores para tipo númerico
Trabalhar com o tipo correto das variáveis é muito importante para extrair inteligência dos dados corretamente.

```python
produtos["price"] = produtos["price"].str.replace("R$", "").str.strip().astype(float)
```
A coluna que está em um formato errado no dataset de Produtos é a `price`, que está em um formato de **string**, portanto, da maneira acima, a conversão é realizada de maneira simples.

### 🏷️ Remoção de duplicatas
Remover duplicatas é essencial para que a base de dados seja compreendida da sua real forma. Valores repetidos podem distorcer o resultado de diversas tarefas que podem ter sido realizada com os dados.

```python
# exibe duplicatas em todas as colunas
produtos.duplicated().sum()

# remove duplicatas
produtos = produtos.drop_duplicates()
```

Para remover duplicatas, pode-se verificar, com o comando acima as duplicatas de todas as colunas do conjunto de dados, em segida, removê-las. Nesse caso, após a etapa de padronização de categorias do produto, foram geradas **7 linhas duplicadas**.