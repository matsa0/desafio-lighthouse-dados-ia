# %%
# ---------------------------------- #
# Import libs & read sales dataframe #
# ---------------------------------- #
import requests
import pandas as pd 

sales_df = pd.read_csv("../../datasets/vendas_2023_2024.csv")

# date must be in the format 'MM-DD-YYYY' for the API request
sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"], format="mixed")
sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"], format="%m-%d-%Y").dt.strftime("%m-%d-%Y")
print(sales_df.dtypes)

# %%
# ----------------------------------------- #
# Get mean quote through Olinda API (BACEN) #
# ----------------------------------------- #
unique_sale_dates = sales_df["sale_date"].unique()

def get_import_costs_quote(date: str) -> float:
    """
    Queries the Olinda API for each unique date corresponding to the sales dataset, 
    and calculates the average of all daily dollar-to-real selling rates.
    """
    try:
        response = requests.get(f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=\'USD\',dataCotacao=\'{date}\')')
        if response.status_code == 200:
            data = response.json()
            quote = 0.0
            quote_count = 0
            
            for item in data["value"]:
                for field, value in item.items():
                    if field == "cotacaoVenda":
                        quote = quote + value
                        quote_count = quote_count + 1
                        
            mean_quote = quote / quote_count if quote_count > 0 else 0.0          
            return round(mean_quote, 2)
                        
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")

mean_quotes = []
for date in unique_sale_dates:
    mean_quote = get_import_costs_quote(date)
    mean_quotes.append(mean_quote)

dates_quotes_df = pd.DataFrame({
    "sale_date": unique_sale_dates,
    "mean_quote": mean_quotes
})

# %%
"""
BACEN API doesn't returns quotes for saturdays, sundays and holidays.
So, we can use the mean quote referring to the nearest date of NA rows
to fill dates without quotes.
"""

# sort by date to allow correctly use of foward fill
dates_quotes_df["sale_date"] = pd.to_datetime(dates_quotes_df["sale_date"], format="%m-%d-%Y")
dates_quotes_df = dates_quotes_df.sort_values("sale_date", ascending=True)
dates_quotes_df["mean_quote"] = dates_quotes_df["mean_quote"].replace(0, pd.NA)

# foward fill get the last valid value for mean_quote and replace the NA value
dates_quotes_df["mean_quote"] = dates_quotes_df["mean_quote"].ffill()
# if there still NA values, fill with the next mean_quote
dates_quotes_df["mean_quote"] = dates_quotes_df["mean_quote"].bfill()
print(dates_quotes_df)
print(dates_quotes_df.isna().sum())


# %%
# ------------------------------- #
# Saves complete merged dataframe #
# ------------------------------- #
sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"], format="%m-%d-%Y")

sales_with_quotes = pd.merge(
    sales_df,
    dates_quotes_df,
    on="sale_date",
    how="left"
)
sales_with_quotes.to_csv("vendas_com_cambio.csv", index=False)
