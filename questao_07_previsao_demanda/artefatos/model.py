# %%
import pandas as pd
from sklearn.metrics import mean_absolute_error

# %%
sales_df = pd.read_csv("../../datasets/vendas_2023_2024.csv")
products_df = pd.read_csv("../../questao_02_produtos/artefatos/produtos_tratados.csv")

# %%
products_sales_df = pd.merge(
    sales_df,
    products_df.rename({"code": "id_product"}, axis=1),
    how="left",
    on="id_product"
).reset_index(drop=True)

display(products_sales_df.head()) # type: ignore
print("Shape: ", products_sales_df.shape)
print("\nDuplicates number: ", products_sales_df.duplicated().sum())
print("\nNull values:\n", products_sales_df.isna().sum())
print("\nVariable types:\n", products_sales_df.dtypes)

# %%
# selecting only the target product ('Motor de Popa Yamaha Evo Dash 155HP')
products_sales_df["name"] = products_sales_df["name"].str.lower().str.strip()
target_product = products_sales_df[products_sales_df["name"].str.contains('motor de popa yamaha evo dash 155hp')]

target_product["name"] = target_product["name"].str.capitalize

# %%
# formatting sale_date column
target_product["sale_date"] = pd.to_datetime(target_product["sale_date"], format="mixed")

# get the quantity sold of the target product in each date
daily_sales = (
    target_product.groupby("sale_date")["qtd"]
    .sum()
    .reset_index()
)

# creates temporal dimension (ensure to include days without sales)
dim_calendar = pd.date_range(
    start=daily_sales["sale_date"].min(),
    end=daily_sales["sale_date"].max(),
    freq="D" # daily frequency
)
# transforming to dataframe
dim_calendar_df = pd.DataFrame({
    "sale_date": dim_calendar
})
# print(dim_calendar_df)

daily_sales_df = pd.merge(
    dim_calendar_df,
    daily_sales,
    how="left",
    on="sale_date"
).fillna(0).reset_index(drop=True)
daily_sales["qtd"] = daily_sales_df["qtd"].astype(int)
print(daily_sales_df)

# filtering train dataset
train_df = daily_sales_df[daily_sales_df["sale_date"] <= '2023-12-31']
print("Train dataframe shape: ", train_df.shape)
print(f"Min date train dataframe: {train_df['sale_date'].min()}\nMax date train dataframe: {train_df['sale_date'].max()}")

# filtering test dataset
test_df = daily_sales_df[(daily_sales_df["sale_date"] > '2023-12-31') &
                            (daily_sales_df["sale_date"] <= '2024-01-31')]
print("Test dataframe shape: ", test_df.shape)
print(f"Min date test dataframe: {test_df['sale_date'].min()}\nMax date test dataframe: {test_df['sale_date'].max()}")

print(test_df)

# %%
"""
calculating the moving average

moving average is a calculation to analyze data points by creating
a series of averages of different selections of the full dataset

window_size = the number of consecutive data points (time periods -> days)
included in each average calculation.

here, we want to calculate the average sales of the 7 previous days of an date

example: we want to predict the amount of sales of 2024-01-08
we'll use the average of the 7 previous days:
2024-01-01
2024-01-02
2024-01-03
2024-01-04
2024-01-05
2024-01-06
2024-01-07
"""

# building model baseline
january_2024_predictions = []
# begins with december days but its updated as january days are calculated
days_history_qtds = train_df["qtd"].tolist()

for actual_day_qtd in test_df["qtd"]:
    # get the last 7 days
    moving_avg = round(sum(days_history_qtds[-7:]) / 7)
    
    # appends the new predction
    january_2024_predictions.append(moving_avg)
    
    # appends the quantity of the actual day being used
    days_history_qtds.append(actual_day_qtd)
    
print(january_2024_predictions)

# %%
# comparing test with predictions with MAE

test_df["prediction"] = january_2024_predictions
mae = round(mean_absolute_error(test_df["qtd"], test_df["prediction"]), 2)
display(test_df) # type: ignore
print("Mean Absolute Error (MAE): ", mae)
# %%
non_zero_days = test_df[test_df["qtd"] > 0]

mae_non_zero = mean_absolute_error(
    non_zero_days["qtd"],
    non_zero_days["prediction"]
)

print("MAE (dias com venda):", mae_non_zero)
# %%
