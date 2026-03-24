# %%
import pandas as pd
sales_df = pd.read_csv("../../datasets/vendas_2023_2024.csv")
sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"], format="mixed")

# %%
daily_sales = (
    sales_df.groupby("sale_date")[["total", "qtd"]]
    .sum()
    .reset_index()
)

dim_calendar = pd.date_range(
    start=daily_sales["sale_date"].min(),
    end=daily_sales["sale_date"].max(),
    freq="D"
)

dim_calendar_df = pd.DataFrame({
    "sale_date": dim_calendar
})

# %%
daily_sales_df = pd.merge(
    dim_calendar_df,
    daily_sales,
    how="left",
    on="sale_date"
)

daily_sales_df[["total", "qtd"]] = daily_sales_df[["total", "qtd"]].fillna(0)

print(daily_sales_df)
daily_sales_df.to_csv("vendas_diarias.csv")
# %%
