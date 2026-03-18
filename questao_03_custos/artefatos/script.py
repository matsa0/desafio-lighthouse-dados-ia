import json
import pandas as pd # type: ignore

file_path = "../../datasets/custos_importacao.json"

try:
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
        print("\nDataframe Normalized:\n", import_costs_df)

        # saves the DataFrame to a CSV file
        import_costs_df.to_csv("custos_importacao.csv", index=False)
    
    
except FileNotFoundError:
    print(f"File not found at '{file_path}'. Please check the path and try again.")
except json.JSONDecodeError:
    print(f"Error decoding JSON. Please check the file format and try again.")