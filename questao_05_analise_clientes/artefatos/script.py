# -------------------------------------- #
# Imports and reading products dataframe #
# -------------------------------------- #
import pandas as pd 
import json

products_df = pd.read_csv("../../datasets/produtos_raw.csv")

print("Categorias antes da manipulação:\n", products_df["actual_category"].value_counts())

# ------------------------------------ #
# standardizing actual_category values #
# ------------------------------------ #
products_df["actual_category"] = products_df["actual_category"].str.lower().str.strip().str.replace(" ", "")

# mapping actual_category values to standardized categories
products_df["actual_category"] = products_df["actual_category"].map(
    lambda x: "Eletrônicos" if "eletr" in x else (
        "Propulsão" if "prop" in x else (
            "Ancoragem" if "ncora" in x else "Outros"
        )
    )
)

print("\nStandardized 'actual_category' values:\n", products_df["actual_category"].value_counts())

# converting price to float
products_df["price"] = products_df["price"].str.replace("R$", "").str.strip().astype(float)
# droping duplicates
products_df = products_df.drop_duplicates()

print("Após remoção de duplicatas: ", products_df["actual_category"].value_counts())

# --------------------------- #
# Obtaining data from clients #
# --------------------------- #
json_file_path = "../../datasets/clientes_crm.json"

try:
    with open(json_file_path, "r") as f:
        clients_crm = json.load(f) # parse JSON -> Python dict
        clients_crm_df = pd.DataFrame(clients_crm)
except FileNotFoundError:
    print(f"File not found at '{json_file_path}'. Please check the path and try again.")
except json.JSONDecodeError:
    print(f"Error decoding JSON. Please check the file format and try again.")

print(clients_crm_df)
print("Clients CRM dataftame columns: ", clients_crm_df.columns.values)
print(clients_crm_df.isna().sum())

# ------------------------------------------- #
# Reading sales dataset to merge with Clients # 
# ------------------------------------------- #
sales = pd.read_csv("../../datasets/vendas_2023_2024.csv")
print("Number of unique clients in Sales dataframe: ", sales["id_client"].nunique())
print(f"Min client ID(Sales): {sales['id_client'].min()}\nMax client ID(Sales): {sales['id_client'].max()}")

# creating id_client in Clients CRM dataframe
clients_crm_df["id_client"] = clients_crm_df.index + 1

sales_df = pd.merge(
    sales,
    clients_crm_df,
    how="left",
    on="id_client"
).reset_index(drop=True)

print(sales_df.columns)

# ------------------------------------------------ #
# Merging previous merged dataframe with Products  #
# ------------------------------------------------ #
products_sales_df = pd.merge(
    sales_df,
    products_df.rename(columns={"code": "id_product"}),
    how="left",
    on="id_product"
).reset_index(drop=True)

print("Dataframe merged:\n", products_sales_df.columns)
print(products_sales_df.isna().sum())
print(products_sales_df.duplicated().sum())

# saving merged dataset
products_sales_df.to_csv("produtos_vendidos.csv", index=False)
