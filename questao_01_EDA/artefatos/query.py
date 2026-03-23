import pandas as pd 
import duckdb as db 

# ----------------------------- #
# Dataframe & DuckDB connection #
# ----------------------------- #
sales_df = pd.read_csv("../../datasets/vendas_2023_2024.csv")

con = db.connect()
# create 'sales' table in duckdb
con.execute("CREATE TABLE sales AS SELECT * FROM sales_df")

def execute_query(query: str, con:db.DuckDBPyConnection = con) -> pd.DataFrame:
    """
    Executes the query and converts to a pandas dataframe
    """
    return con.execute(query).df()

rows_num = """
    SELECT COUNT(*) AS num_rows 
    FROM sales
"""

cols_num = """
    SELECT COUNT(*) AS num_cols
    FROM information_schema.columns
    WHERE table_name = 'sales'
"""

date_interval = """
    ALTER TABLE sales
    ALTER sale_date TYPE DATE USING sale_date::DATE; 
    
    SELECT 
        MAX(sale_date) - MIN(sale_date) AS date_interval
    FROM sales
"""

total_value_query = """
    SELECT 
        MIN(total) AS min_total,
        MAX(total) AS max_total,
        ROUND(AVG(total), 2) AS mean_total,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total) AS median_total,
        ROUND(STDDEV(total), 2) AS std_total
    FROM sales
"""

duplicated_values = sales_df.duplicated().sum()
null_values = sales_df.isna().sum()


print("Rows number: \n", execute_query(rows_num))
print("\nColumns number: \n", execute_query(cols_num))
# print("\nDate interval: \n", execute_query(date_interval))
print("\nTotal value analysis: \n", execute_query(total_value_query))
print("\nNull values: \n", null_values)
print("\nDuplicated values: \n", duplicated_values)
print("\nFirst 5 rows: \n", sales_df.head(5))
print("\nColumns types: \n", sales_df.dtypes)