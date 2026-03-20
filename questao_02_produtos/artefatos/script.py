import pandas as pd  # type: ignore

produtos = pd.read_csv("../../datasets/produtos_raw.csv")

# initial analysis
def initial_analysis(df: pd.DataFrame) -> None:
    print("First 5 rows:\n", df.head(5))
    print("\nShape: ", df.shape)
    print("\nColumns types:\n", df.dtypes)
    print("\nNull values:\n", df.isna().sum())
    print("\nDuplicated values:\n", df.duplicated().sum())
    print("\nDistinct values in 'actual_category':\n", df["actual_category"].value_counts())

initial_analysis(produtos)

# standardizing actual_category values
produtos["actual_category"] = produtos["actual_category"].str.lower().str.strip().str.replace(" ", "")
print("\n", produtos["actual_category"].value_counts())

# visualizing the standardized values
eletronic_products_mask = produtos["actual_category"].str.contains("eletr")
print("\nEletronic products: ", produtos[eletronic_products_mask]["actual_category"].unique())

propulsion_products_mask = produtos["actual_category"].str.contains("prop")
print("\nPropulsion products: ", produtos[propulsion_products_mask]["actual_category"].unique())

anchoring_products_mask = produtos["actual_category"].str.contains("ncora")
print("\nAnchoring products: ", produtos[anchoring_products_mask]["actual_category"].unique())

# mapping actual_category values to standardized categories
produtos["actual_category"] = produtos["actual_category"].map(
    lambda x: "Eletrônicos" if "eletr" in x else (
        "Propulsão" if "prop" in x else (
            "Ancoragem" if "ncora" in x else "Outros"
        )
    )
)

print("\nStandardized 'actual_category' values:\n", produtos["actual_category"].value_counts())

# converting price to float
produtos["price"] = produtos["price"].str.replace("R$", "").str.strip().astype(float)


# removing duplicates
print("Duplicated values: ", produtos.duplicated().sum())
print("Linhas duplicadas:\n", produtos[produtos.duplicated()])
produtos = produtos.drop_duplicates()
