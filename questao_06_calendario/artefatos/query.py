import pandas as pd
import duckdb as db

sales_df = pd.read_csv("../../datasets/vendas_2023_2024.csv")

# formatting sale_date column (yyyy-MM-dd)
sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"], format="mixed")

# duckdb connection and table creation
con = db.connect()
con.execute('CREATE TABLE sales AS SELECT * FROM sales_df')

def execute_query(query: str, con:db.DuckDBPyConnection = con) -> pd.DataFrame:
    return con.execute(query).df()

date_dimension_query = """
    -- recursive CTE to get the all dates
    WITH 
        RECURSIVE dim_calendar AS (
            SELECT MIN(sale_date) AS base_date
            FROM sales
            
            UNION ALL
            
            SELECT base_date + INTERVAL 1 DAY
            FROM dim_calendar
            WHERE base_date < (SELECT MAX(sale_date) FROM sales)
        ),
        
        -- calculates the revenue of each day that had sales
        daily_sales AS (
            SELECT 
                sale_date,
                SUM(total) AS daily_revenue
            FROM sales
            GROUP BY sale_date
        ),
        
        -- brings the complete calendar and get the week days codes
        calendar_sales AS (
            SELECT
                dc.base_date,
                EXTRACT(DOW FROM dc.base_date) AS day_code,
                COALESCE(ds.daily_revenue, 0) AS real_revenue -- replace null values of daily_revenue with 0
            FROM dim_calendar dc
            LEFT JOIN daily_sales ds
            ON dc.base_date = ds.sale_date
        )

    -- writes the days of the week in portuguese and calculates the average for each day
    SELECT 
        CASE day_code
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS day_of_week_name,
        ROUND(AVG(real_revenue), 2) AS average_daily_revenue
    FROM calendar_sales
    GROUP BY day_of_week_name
    ORDER BY average_daily_revenue ASC;
"""

query_result = execute_query(date_dimension_query)
# 2024 was a leap year (366 + 365 = 731)
print(query_result)

query_result.to_csv("media_receita_dias_semana.csv", index=False)