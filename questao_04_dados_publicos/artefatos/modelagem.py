import pandas as pd
import duckdb as db

import_costs = pd.read_csv("custos_importacao_com_cambio.csv")
print(import_costs.dtypes)

sales = pd.read_csv("../../datasets/vendas_2023_2024.csv")
print("Número de produtos únicos: ", sales["id_product"].nunique())
print(sales.dtypes)

# sort dataframes by date 
import_costs["start_date"] = pd.to_datetime(import_costs["start_date"], format="%m-%d-%Y")
import_costs = import_costs.sort_values("start_date")
print(import_costs)

sales["sale_date"] = pd.to_datetime(sales["sale_date"], dayfirst=True, format='mixed')
sales = sales.sort_values("sale_date")
print(sales)

"""
merge_asof looks for the closest match of sale_date
in the start_date column of import_costs, then
merges the mean_quote value from import_costs into sales
"""
merged_data = pd.merge_asof(
    sales,
    import_costs,
    left_on="sale_date",
    right_on="start_date",
    left_by="id_product",
    right_by="product_id",
    direction="backward" # get the last import before the sale date
)

print(merged_data)
print("\nColunas: ",merged_data.columns.values)
print("\nNulos: \n", merged_data.isna().sum())
print("\nDuplicados: ", merged_data.duplicated().sum())

merged_data.to_csv("vendas_com_cambio.csv", index=False)