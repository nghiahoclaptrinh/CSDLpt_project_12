import pandas as pd
import sqlite3
import os

# Create database folder
os.makedirs("../databases", exist_ok=True)

files = {
    "north": "../datasets/fragments/sales_north.csv",
    "south": "../datasets/fragments/sales_south.csv",
    "west": "../datasets/fragments/sales_west.csv"
}

for region, path in files.items():

    df = pd.read_csv(path)

    conn = sqlite3.connect(f"../databases/sales_{region}.db")

    df.to_sql(
        "Sales",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print(f"Database sales_{region}.db created!")