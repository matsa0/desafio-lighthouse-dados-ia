# -------------------------------------- #
# Initial analysis of products dataframe #
# -------------------------------------- #
import pandas as pd  

products_df = pd.read_csv("../../datasets/produtos_raw.csv")

def initial_analysis(df: pd.DataFrame) -> None:
    print("First 5 rows:\n", df.head(5))
    print("\nShape: ", df.shape)
    print("\nColumns types:\n", df.dtypes)
    print("\nNull values:\n", df.isna().sum())
    print("\nDuplicated values:\n", df.duplicated().sum())
    print("\nDistinct values in 'actual_category':\n", df["actual_category"].value_counts())

initial_analysis(products_df)

# ---------------------------- #
# Modeling products categories #
# ---------------------------- #
# standardizing actual_category values
products_df["actual_category"] = products_df["actual_category"].str.lower().str.strip().str.replace(" ", "")
print("\n", products_df["actual_category"].value_counts())

# visualizing the standardized values
eletronic_products_mask = products_df["actual_category"].str.contains("eletr")
print("\nEletronic products: ", products_df[eletronic_products_mask]["actual_category"].unique())

propulsion_products_mask = products_df["actual_category"].str.contains("prop")
print("\nPropulsion products: ", products_df[propulsion_products_mask]["actual_category"].unique())

anchoring_products_mask = products_df["actual_category"].str.contains("ncora")
print("\nAnchoring products: ", products_df[anchoring_products_mask]["actual_category"].unique())

# mapping actual_category values to standardized categories
products_df["actual_category"] = products_df["actual_category"].map(
    lambda x: "Eletrônicos" if "eletr" in x else (
        "Propulsão" if "prop" in x else (
            "Ancoragem" if "ncora" in x else "Outros"
        )
    )
)

print("\nStandardized 'actual_category' values:\n", products_df["actual_category"].value_counts())

# ------------------------------------- #
# Saving manipulated products dataframe #
# ------------------------------------- #
# converting price to float
products_df["price"] = products_df["price"].str.replace("R$", "").str.strip().astype(float)

# removing duplicates
print("Duplicated values: ", products_df.duplicated().sum())
print("Linhas duplicadas:\n", products_df[products_df.duplicated()])
products_df = products_df.drop_duplicates()

products_df.to_csv("produtos_tratados.csv", index=False)