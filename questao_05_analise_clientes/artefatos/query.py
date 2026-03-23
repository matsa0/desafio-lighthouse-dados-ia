# ----------------------------------------- #
# Imports and creating products sales table #
# ----------------------------------------- #
import duckdb as db
import pandas as pd

products_sales_df = pd.read_csv("products_sales.csv")
con = db.connect()
con.execute("CREATE TABLE products_sales AS SELECT * FROM products_sales_df")

# ----------------------- #
# Calculating Mean Ticket #
# ----------------------- #
def execute_query(query: str, con:db.DuckDBPyConnection = con) -> pd.DataFrame:
    """
    Executes the query and converts to a pandas dataframe
    """
    return con.execute(query).df()

ranking_query = """
    SELECT 
        id_client,
        ROUND(SUM(total), 2) AS annual_revenue,
        COUNT(DISTINCT id) AS frequency,
        ROUND((SUM(total) / COUNT(DISTINCT id)), 2) AS mean_ticket,
        COUNT(DISTINCT actual_category) AS diversity
    FROM products_sales
    GROUP BY id_client
    HAVING diversity >= 3
    ORDER BY mean_ticket DESC, id_client ASC
    LIMIT 10;
"""

ranking_result_df = execute_query(ranking_query)
print(ranking_result_df)

ranking_result_df.to_csv("ranking_ticket_medio.csv", index=False)

# -------------------------------------------------------------------------------- #
# Among top 10 clients, which category have the largest amount of items purchased? #
# -------------------------------------------------------------------------------- #
categories_query = """
    SELECT
        actual_category,
        SUM(qtd) AS items_bought_qnt
    FROM products_sales
    WHERE id_client IN (
        SELECT 
            id_client
        FROM products_sales
        GROUP BY id_client
        HAVING COUNT(DISTINCT actual_category) >= 3
        ORDER BY (SUM(total) / COUNT(DISTINCT id)) DESC, id_client ASC
        LIMIT 10
    )
    GROUP BY actual_category
    ORDER BY items_bought_qnt DESC;
"""

categories_revenue_df = execute_query(categories_query)
print(categories_revenue_df)

categories_revenue_df.to_csv("quantidade_comprada_por_categoria.csv", index=False)