# %%
import pandas as pd
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ #
# Reading dataframes #
# ------------------ #
sales_df = pd.read_csv("../../datasets/vendas_2023_2024.csv")
products_df = pd.read_csv("../../questao_02_produtos/artefatos/produtos_tratados.csv")

# visualizing ID of the taget product
target_product = products_df[products_df["name"] == "GPS Garmin Vortex Maré Drift"]
print("ID do produto alvo: ", target_product["code"].values)

# ------------------------------------------------ #
# Creating interaction matrix (Customer x Product) #
# ------------------------------------------------ #
sales_df["purchased"] = 1

interaction_matrix = sales_df.pivot_table(
    index="id_client",
    columns="id_product",
    values="purchased",
    aggfunc="max",
    fill_value=0
)
print(interaction_matrix)

# %%
# ----------------------------- #
# Calculating Cosine Similarity #
# ----------------------------- #

"""
A product with many customers in common -> high similarity
A product with few customers in common  -> low similarity

Cos similarity of sklearn compares rows, and we want to compare 
products (Product x Product). Transpose the dataframe will make
each row become a product.

- lines: products
- columns: clients
"""
print()
cosine_sim_matrix = cosine_similarity(interaction_matrix.transpose())

cosine_similarity_df = pd.DataFrame(
    cosine_sim_matrix,
    index=interaction_matrix.columns,
    columns=interaction_matrix.columns
)

print(cosine_similarity_df)

# %%
# ---------------------------------------- #
# Ranking similar products with the target #
# ---------------------------------------- #

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

# adjusting products dataframe
products_df = products_df.rename(columns={"code": "id_product"})
products_df["id_product"] = products_df["id_product"].astype(int)

# recover product name
top5_ranking = top5_ranking.merge(
    products_df[["id_product", "name"]],
    on="id_product",
    how="left"
)

print(top5_ranking)

# plotting
plt.figure(figsize=(10, 6))

sns.barplot(
    data=top5_ranking.sort_values("cos_similarity"),
    x="cos_similarity",
    y="name",
    palette="Blues",
    hue="name",
    legend=False
)

plt.title("Top 5 produtos mais similares ao produto 27")
plt.xlabel("Similaridade de Cosseno")
plt.ylabel("Produto")

plt.tight_layout()
plt.savefig("top5_ranking.png")

# %%