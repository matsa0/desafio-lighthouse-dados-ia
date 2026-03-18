# ✦ Questão 03 - Custos de importação 📥💲

Nessa terceira questão, iremos trabalhar com o arquivo [custos de importação](../datasets/custos_importacao.json), um arquivo JSON que possui dados a respeito de um produto e seu preços ao longo do tempo, um arquivo muito rico, que permite várias análises. O escopo dessa questão requisita as seguintes tarefas abaixo:

## ⮞ Premissas Obrigatórias
- Utilize apenas o JSON [custos_importacao.json](../datasets/custos_importacao.json)
- Utilize obrigatoriamente Python 3 (nesse caso, **Python 3.11** em um ambiente virtual conda)

**Obs:** O tratamento do JSON foi realizado no arquivo [script.py](./artefatos/script.py), onde os códigos foram testados.
 

### 🏷️ Carregue o JSON e organize-o em um CSV

```python
with open(file_path, "r") as f:
    import_costs = json.load(f) # parse JSON -> Python dict
    import_costs_df = pd.DataFrame(import_costs)
    
    # explode the 'historic_data' list into separate rows
    import_costs_df = import_costs_df.explode("historic_data")
    print("Dataframe Exploded:\n", import_costs_df)
    
    # extract 'start_date' and 'usd_price' from the 'historic_data' dict
    import_costs_df["start_date"] = import_costs_df["historic_data"].str["start_date"]
    import_costs_df["usd_price"] = import_costs_df["historic_data"].str["usd_price"]
    
    # remove the original 'historic_data' column 
    import_costs_df = import_costs_df.drop(["historic_data"], axis=1)
    print("Dataframe Normalized:\n", import_costs_df)

    # saves the DataFrame to a CSV file
    import_costs_df.to_csv("custos_importacao.csv", index=False)
```
O que é interessante ressaltar nessa abordagem, é o uso da função **explode** do `Pandas`. Ao trasnformar o JSON para DataFrame, a colunas **historic_data** vem em formato de lista, assim como representado abaixo:

```text 
[{'start_date': '10/08/2016', 'usd_price': 10583.63'}, {'start_date': '15/06/2018', 'usd_price': 8778.36'}, ...]
```

O explode faz a "explosão" dessas linhas, garantido que tenha **uma linha para cada elemento presente na lista original**. Nesse caso, o dataset para de ter uma linha por produto e sim uma linha para cada dado histórico, mantendo o alinhamento dos índices originais, sendo muito importante para que os registros explodidos continuem pertencendo ao produto correto. 

### 🏷️ Quantas entradas de importação o CSV recebeu ao todo após a normalização?

Após a normalização com **explode**, o CSV ficou com o total de **1260 entradas**.