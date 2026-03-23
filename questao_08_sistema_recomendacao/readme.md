# ✦ Questão 08 - Sistema de recomendação 🎯

Nesta questão deve-se criar um **sistema de recomendação de produtos** que é baseado na similaridade de compra dos clientes da LH Nauticals. Ess motor de recomendação deve responder a seguinte pergunta: **Qual produto deve ser recomendado junto ao item "GPS Garmin Vortex Maré Drift"**?

## ⮞ Premissas Obrigatórias 

- O sistema de recomendação deve ser criado através do cálculo de Similaridade de Cossenos (**Cosine Similarity**)
- Considere apenas o produto **"GPS Garmin Vortex Maré Drift"** como referência e o desconsidere do ranking
- O ranking deve conter os **5 produtos mais similares** ao produto alvo

**0bs:** A criação do ranking dos 5 produtos mais similares ao produto alvo foi realizada no arquivo [script.py](./artefatos/script.py).


### 🏷️ Crie uma matriz de interação Usuário x Produto

```python
products_sales_df["purchased"] = 1
interaction_matrix = products_sales_df.pivot_table(
    index="id_client",
    columns="id_product",
    values="purchased",
    aggfunc="max",
    fill_value=0
)
```

### 🏷️ Calcule a similaridade entre produtos

```python
cosine_similarity = cosine_similarity(interaction_matrix.transpose())

cosine_similarity_df = pd.DataFrame(
    cosine_similarity,
    index=interaction_matrix.columns,
    columns=interaction_matrix.columns
)
```

### 🏷️ Faça um ranking de produotos similares

```python
reference_product = (
    cosine_similarity_df.loc[27]
    .drop(27) # removing target product from the ranking
    .sort_values(ascending=False)
)

top5_ranking = (
    reference_product
    .reset_index()
    .rename(columns={
        "index": "id_product",
        27: "cos_similarity"
    })
    .head(5)
)
```
| ID do produto | Similaridade   | Nome do produto                               |
| :-----------  |:--------------:|-----------------------------------------------|
| 94            | 0.869          | Motor de Popa Volvo Magnum 276HP              |
| 11            | 0.868          | GPS Furuno Swift Leviathan Poseidon           |
| 35            | 0.853          | Radar Furuno Swift                            |
| 1             | 0.850          | Transponder AIS Maré Magnum                   |
| 115           | 0.850          | Cabo de Nylon Delta Force Magnum Leviathan    |

- **Qual é o id_produto com MAIOR similaridade ao “GPS Garmin Vortex Maré Drift”?**

    O produto com maior similaridade é o **"Motor de Popa Volvo Magnum 276HP"** com o `ID 94`.

### 🏷️ Interpretação

- **Como a matriz foi construída?** 
    
    A martriz foi construída com base na tabela de vendas, que já possuí informações a respeito da relação entre clientes e produtos.

    Na matriz de interação, cada linha representa um cliente e cada coluna representa um produto, porém, para que a similaridade seja calculada **Produto x Produto** e para se adaptar ao cálculo feito pela biblioteca **scikit-learn**, é necessário fazer a transposição do *dataframe*, de forma que **cada linha se torne um produto** representado por um vetor binário.

- **O que significa a similaridade de cosseno nesse contexto?**

    Nesse contexto, a similaridade de cosseno vai auxiliar a medir o grau de semelhança entre produtos diferentes com base no comportamento de compra dos clientes que são capturados pela tabela de vendas.

    Cada produto é representado por um vetor binário, indicando quais clientes realizaram ao menos uma compra daquele item. A similaridade é calculada comparando esses vetores, avaliando o quanto dois produtos são comprados pelos mesmos clientes.
    
    Como os vetores são binários, a similaridade de cosseno varia entre 0 a 1, sendo mais próximo de 1, aqueles produtos frequentemente comprados pelos mesmos clientes e mais próximos de 0, produtos raramente comprados pelos mesmos clientes. Assim, os produtos com maior similaridade em relação ao item alvo são aqueles mais indicados para recomendação.

- **Cite uma limitação desse método de recomendação.**

    Como a matriz de similaridade é binária(presência/ausência), ela **ignora a frequência(quantidade)** e isso gera um grande problema, pois por exemplo, dois produtos comprados juntos uma única vez terão o mesmo peso que produtos frequentemente comprados em conjunto, o que pode **distorcer a relevância das recomendações**.