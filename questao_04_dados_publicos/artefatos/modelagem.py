import pandas as pd
import duckdb as db

import_costs_df = pd.read_csv("../../questao_03_custos/artefatos/custos_importacao.csv")
print("Número de produtos únicos: ", import_costs_df["product_id"].nunique())

sales_with_quotes_df = pd.read_csv("vendas_com_cambio.csv")
print("Número de produtos únicos: ", sales_with_quotes_df["id_product"].nunique())

# sort dataframes by date 
import_costs_df["start_date"] = pd.to_datetime(import_costs_df["start_date"], format="mixed", dayfirst=True)
import_costs_df = import_costs_df.sort_values(["start_date", "product_id"])
print(import_costs_df)

sales_with_quotes_df["sale_date"] = pd.to_datetime(sales_with_quotes_df["sale_date"], format="mixed", dayfirst=True)
sales_with_quotes_df = sales_with_quotes_df.sort_values(["sale_date", "id_product"])
print(sales_with_quotes_df)

"""
merge_asof looks for the closest match of sale_date
in the start_date column of import_costs, then
merges the mean_quote value from import_costs into sales
"""
merged_data = pd.merge_asof(
    sales_with_quotes_df,
    import_costs_df.rename({"product_id": "id_product"}, axis=1),
    left_on="sale_date",
    right_on="start_date",
    by="id_product",
    direction="backward" # get the last import before the sale date
)

print(merged_data)
print("\nColunas: ",merged_data.columns.values)
print("\nNulos: \n", merged_data.isna().sum())
print("\nDuplicados: ", merged_data.duplicated().sum())

merged_data.to_csv("vendas_com_usd_e_cambio.csv", index=False)