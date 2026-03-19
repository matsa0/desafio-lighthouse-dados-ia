import pandas as pd
import duckdb as db
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

sales = pd.read_csv("vendas_com_cambio.csv")

# create duckdb connection
con = db.connect()
# create 'sales' table in duckdb
con.execute("CREATE TABLE sales AS SELECT * FROM sales")

def execute_query(query: str, con:db.DuckDBPyConnection = con) -> pd.DataFrame:
    return con.execute(query).df()

query = """
    WITH transactions AS (
        SELECT 
            id_product,
            product_name,
            total AS transaction_revenue,
            (usd_price * mean_quote * qtd) AS transaction_revenue_converted,
            
            -- LOSS: when converted value is higher than revenue transaction 
            CASE 
                WHEN (usd_price * mean_quote * qtd) > total 
                THEN (usd_price * mean_quote * qtd) - total
                ELSE 0 
            END AS transaction_loss
        FROM sales
    )
    
    SELECT 
        id_product,
        product_name,
        ROUND(SUM(transaction_revenue), 2) AS total_revenue,
        ROUND(SUM(transaction_loss), 2) AS total_loss,
        ROUND((SUM(transaction_loss) / SUM(transaction_revenue)) * 100, 2) AS total_loss_pct
    FROM transactions
    GROUP BY id_product, product_name
    ORDER BY total_loss DESC;
"""

question_4_1_result = execute_query(query)
print(question_4_1_result)

##### -------------------------------------------------------------- #####

loss_products = question_4_1_result[question_4_1_result["total_loss"] > 0] \
    .head(15).sort_values(by="total_loss", ascending=True)

higher_percent_losses = loss_products[loss_products["total_loss_pct"] == loss_products["total_loss_pct"].max()]

print("Produto com maior porcentagem de perda:")
print(higher_percent_losses[["id_product", "product_name", "total_loss_pct"]])


plt.figure(figsize=(10,6))
ax = sns.barplot(
    data=loss_products,
    x=loss_products["id_product"].astype(str),
    y="total_loss",
    palette="ch:start=.2,rot=-.3",
    hue="total_loss",
    legend=False
)
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
plt.ylim(0, loss_products["total_loss"].max() * 1.2)

for i, p in enumerate(ax.patches):
    percentage = loss_products.iloc[i]["total_loss_pct"]
    
    ax.annotate(f'{percentage:.2f}%', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', 
                xytext = (0, 9), 
                textcoords = 'offset points',
                fontsize=9,
                fontweight='bold')

plt.title("Top 15 produtos com maior prejuízo total")
plt.xlabel("ID do produto")
plt.ylabel("Prejuízo total (R$)")

plt.ylim(0, loss_products["total_loss"].max() * 1.15)

plt.tight_layout()
plt.savefig("produtos_com_prejuizo.png")

