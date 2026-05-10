import pandas as pd
import os

df = pd.read_csv("../datasets/sales.csv")

os.makedirs("../datasets/fragments", exist_ok=True)

north = df[df["Region"] == "North"]
south = df[df["Region"] == "South"]
west = df[df["Region"] == "West"]

north.to_csv("../datasets/fragments/sales_north.csv", index=False)
south.to_csv("../datasets/fragments/sales_south.csv", index=False)    
west.to_csv("../datasets/fragments/sales_west.csv", index=False)

print("fragmentation complete")
