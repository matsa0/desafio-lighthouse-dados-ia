import pandas as pd # type: ignore
import duckdb as db # type: ignore

vendas = pd.read_csv("../../datasets/vendas_2023_2024.csv")
# duckdb connection
con = db.connect()

# create 'vendas' table in duckdb
con.execute("CREATE TABLE vendas AS SELECT * FROM vendas")

def execute_query(query: str, con:db.DuckDBPyConnection = con) -> pd.DataFrame:
    return con.execute(query).df()

rows_num = """
    SELECT COUNT(*) AS num_linhas 
    FROM vendas
"""

cols_num = """
    SELECT COUNT(*) AS num_colunas
    FROM information_schema.columns
    WHERE table_name = 'vendas'
"""

date_interval = """
    ALTER TABLE vendas
    ALTER sale_date TYPE DATE USING sale_date::DATE; 
    
    SELECT 
        MAX(sale_date) - MIN(sale_date) AS date_interval
    FROM vendas
"""

total_value_query = """
    SELECT 
        -- Análises Obrigatórias
        MIN(total) AS min_total,
        MAX(total) AS max_total,
        ROUND(AVG(total), 2) AS mean_total,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total) AS median_total,
        ROUND(STDDEV(total), 2) AS std_total
    FROM vendas
"""

duplicated_values = vendas.duplicated().sum()
null_values = vendas.isna().sum()


print("Rows number: \n", execute_query(rows_num))
print("\nColumns number: \n", execute_query(cols_num))
print("\nDate interval: \n", execute_query(date_interval))
print("\nTotal value analysis: \n", execute_query(total_value_query))
print("\nNull values: \n", null_values)
print("\nDuplicated values: \n", duplicated_values)
print("\nFirst 5 rows: \n", vendas.head(5))
print("\nColumns types: \n", vendas.dtypes)