import requests
import pandas as pd 

"""
-- custos_importacao.csv --
Multiplicar o valor do dolar no dia da venda (start_date) e 
obter o valor em REAL

-- vendas_2023_2024.csv --
Verificar se o valor total vendido por produto (que está EM 
REAL) bate com o valor total vendido por produto convertido
para REAL. 

A TAXA DE CÂMBIO É A MÉDIA DAS COTAÇÕES DE VENDA DO DIA
"""

import_costs = pd.read_csv('../../questao_03_custos/artefatos/custos_importacao.csv')

# date must be in the format 'MM-DD-YYYY' for the API request
import_costs["start_date"] = pd.to_datetime(import_costs["start_date"], format="%d/%m/%Y")
import_costs["start_date"] = pd.to_datetime(import_costs["start_date"], format="%m-%d-%Y").dt.strftime("%m-%d-%Y")

print(import_costs)

def get_import_costs_quote(date: str) -> float:
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

# use apply function to get the mean quote for each date in the 'start_date' column
import_costs["mean_quote"] = import_costs["start_date"].apply(get_import_costs_quote)
print(import_costs)

#%%
import_costs.to_csv("custos_importacao_com_cambio.csv", index=False)

