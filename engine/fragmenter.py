import pandas as pd
import os

# =========================================
# BASE DIRECTORY
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================================
# INPUT FILE
# =========================================

sales_file = os.path.join(
    BASE_DIR,
    "../datasets/sales.csv"
)

# =========================================
# READ DATASET
# =========================================

df = pd.read_csv(sales_file)

# =========================================
# CREATE FRAGMENT DIRECTORY
# =========================================

fragment_dir = os.path.join(
    BASE_DIR,
    "../datasets/fragments"
)

os.makedirs(fragment_dir, exist_ok=True)

# =========================================
# HORIZONTAL FRAGMENTATION
# =========================================

north = df[df["Region"] == "North"]

south = df[df["Region"] == "South"]

west = df[df["Region"] == "West"]

# =========================================
# SAVE FRAGMENTS
# =========================================

north.to_csv(
    os.path.join(fragment_dir, "sales_north.csv"),
    index=False
)

south.to_csv(
    os.path.join(fragment_dir, "sales_south.csv"),
    index=False
)

west.to_csv(
    os.path.join(fragment_dir, "sales_west.csv"),
    index=False
)

# =========================================
# OUTPUT
# =========================================

print("\n====================================")
print(" HORIZONTAL FRAGMENTATION COMPLETE ")
print("====================================")

print(f"North Fragment : {len(north)} rows")
print(f"South Fragment : {len(south)} rows")
print(f"West Fragment  : {len(west)} rows")

print("\nFragments saved to:")
print(fragment_dir)