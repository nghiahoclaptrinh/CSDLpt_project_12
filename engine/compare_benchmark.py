import time
import pandas as pd
import os

from executor import execute_global_query
from localizer import (
    execute_localized_query,
    detect_target_site
)

# =========================================
# TEST QUERIES
# =========================================

queries = [
    "SELECT * FROM Sales WHERE Region='North'",
    "SELECT * FROM Sales WHERE Region='South'",
    "SELECT * FROM Sales WHERE Region='West'",
    "SELECT * FROM Sales WHERE Amount > 1000",
    "SELECT * FROM Sales",
    "SELECT COUNT(*) FROM Sales"
]

# =========================================
# BENCHMARK
# =========================================

results = []

print("\n====================================")
print(" BROADCAST VS LOCALIZATION TEST ")
print("====================================")

for query in queries:

    print("\n------------------------------------")
    print(query)
    print("------------------------------------")

    # =====================================
    # BROADCAST QUERY
    # =====================================

    start = time.time()

    broadcast_result = execute_global_query(query)

    end = time.time()

    broadcast_time = end - start

    broadcast_nodes = 3

    # =====================================
    # LOCALIZED QUERY
    # =====================================

    start = time.time()

    localized_result = execute_localized_query(query)

    end = time.time()

    localized_time = end - start

    localized_nodes = len(
        detect_target_site(query)
    )

    # =====================================
    # SPEEDUP
    # =====================================

    if localized_time > 0:
        speedup = broadcast_time / localized_time
    else:
        speedup = 0

    # =====================================
    # SAVE RESULT
    # =====================================

    results.append({

        "Query": query,

        "Broadcast Nodes": broadcast_nodes,

        "Localized Nodes": localized_nodes,

        "Broadcast Time (sec)": round(
            broadcast_time,
            6
        ),

        "Localized Time (sec)": round(
            localized_time,
            6
        ),

        "Speedup": round(
            speedup,
            2
        ),

        "Broadcast Rows": len(
            broadcast_result
        ),

        "Localized Rows": len(
            localized_result
        )

    })

# =========================================
# RESULTS TABLE
# =========================================

df = pd.DataFrame(results)

print("\n====================================")
print(" FINAL COMPARISON ")
print("====================================")

print(df)

# =========================================
# SAVE CSV
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

logs_dir = os.path.join(
    BASE_DIR,
    "../logs"
)

os.makedirs(
    logs_dir,
    exist_ok=True
)

output_file = os.path.join(
    logs_dir,
    "comparison_benchmark.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("\n====================================")
print(" BENCHMARK SAVED ")
print("====================================")
print(output_file)