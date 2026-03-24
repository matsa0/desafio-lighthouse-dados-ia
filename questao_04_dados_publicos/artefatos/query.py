import pandas as pd
import duckdb as db
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

sales_with_quotes_df = pd.read_csv("vendas_com_usd_e_cambio.csv")

# create duckdb connection
con = db.connect()
# create 'sales_quotes' table in duckdb
con.execute("CREATE TABLE sales_quotes AS SELECT * FROM sales_with_quotes_df")

def execute_query(query: str, con:db.DuckDBPyConnection = con) -> pd.DataFrame:
    return con.execute(query).df()

query = """
    WITH transactions AS (
        SELECT 
            id_product,
            product_name,
            total AS transaction_revenue,
            (usd_price * mean_quote * qtd) AS transaction_cost_converted,
            
            -- LOSS: when converted value is higher than revenue transaction 
            CASE 
                WHEN (usd_price * mean_quote * qtd) > total 
                THEN (usd_price * mean_quote * qtd) - total
                ELSE 0 
            END AS transaction_loss
        FROM sales_quotes
    )

    SELECT 
        id_product,
        product_name,
        ROUND(SUM(transaction_revenue), 2) AS total_revenue,
        ROUND(SUM(transaction_loss), 2) AS total_loss,
        ROUND(
            CASE 
                WHEN SUM(transaction_revenue) > 0 
                THEN (SUM(transaction_loss) / SUM(transaction_revenue)) * 100
                ELSE 0
            END
        , 2) AS total_loss_pct
    FROM transactions
    GROUP BY id_product, product_name
    ORDER BY total_loss DESC;
"""

products_losses_df = execute_query(query)
print(products_losses_df)
print("\n")
print(products_losses_df[products_losses_df["total_loss"] > 0])

##### -------------------------------------------------------------- #####

higher_percent_losses = products_losses_df[
    products_losses_df["total_loss_pct"] == products_losses_df["total_loss_pct"].max()
]

higher_absolute_loss = products_losses_df[
    products_losses_df["total_loss"] == products_losses_df["total_loss"].max()
]

print("Produto com maior porcentagem de perda:")
print(higher_percent_losses[["id_product", "product_name", "total_loss_pct"]])

print("Produto com maior prejuío absoluto:")
print(higher_absolute_loss[["id_product", "product_name", "total_loss_pct"]])

loss_products = products_losses_df[products_losses_df["total_loss"] > 0]
loss_products.to_csv("produtos_com_prejuizo.csv", index=False)

##### -------------------------------------------------------------- #####

top_loss_products = loss_products.sort_values("total_loss", ascending=False).head(15)

plt.figure(figsize=(10,6))
ax = sns.barplot(
    data=top_loss_products,
    y="product_name",   
    x="total_loss" ,  
    palette="Blues_r"
)

ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

for i, p in enumerate(ax.patches):
    percentage = top_loss_products.iloc[i]["total_loss_pct"]
    
    ax.annotate(
        f'{percentage:.2f}%',
        (p.get_width(), p.get_y() + p.get_height() / 2),
        ha='left',
        va='center',
        xytext=(5, 0),
        textcoords='offset points',
        fontsize=9,
        fontweight='bold'
    )

plt.title("Top 15 produtos com maior prejuízo total")
plt.xlabel("Prejuízo total (R$)")
plt.ylabel("Produto")
ax.grid(True, color='grey', axis='x', linestyle="--", alpha=0.6)

plt.xlim(0, top_loss_products["total_loss"].max() * 1.2)

plt.tight_layout()
plt.savefig("produtos_com_prejuizo.png")