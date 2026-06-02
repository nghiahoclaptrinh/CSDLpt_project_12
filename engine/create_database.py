import pandas as pd
import sqlite3
import os

# =========================================
# BASE DIRECTORY
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================================
# DATABASE FOLDER
# =========================================

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "../databases"
)

os.makedirs(DATABASE_DIR, exist_ok=True)

# =========================================
# FRAGMENT FILES
# =========================================

FILES = {
    "north": os.path.join(
        BASE_DIR,
        "../datasets/fragments/sales_north.csv"
    ),

    "south": os.path.join(
        BASE_DIR,
        "../datasets/fragments/sales_south.csv"
    ),

    "west": os.path.join(
        BASE_DIR,
        "../datasets/fragments/sales_west.csv"
    )
}

# =========================================
# CREATE DATABASES
# =========================================

for region, csv_path in FILES.items():

    print(f"\nReading: {csv_path}")

    if not os.path.exists(csv_path):

        print(f"[ERROR] File not found: {csv_path}")
        continue

    df = pd.read_csv(csv_path)

    db_path = os.path.join(
        DATABASE_DIR,
        f"sales_{region}.db"
    )

    conn = sqlite3.connect(db_path)

    df.to_sql(
        "Sales",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print(f"[SUCCESS] Created: {db_path}")

print("\n====================================")
print(" DATABASE CREATION COMPLETE ")
print("====================================")