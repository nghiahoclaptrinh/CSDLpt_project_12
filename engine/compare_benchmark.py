import time
import pandas as pd
import os

from executor import execute_global_query
from localizer import execute_localized_query

# =========================================
# TEST QUERIES
# =========================================

queries = [
    "SELECT * FROM Sales WHERE Region='North'",
    "SELECT * FROM Sales WHERE Region='South'",
    "SELECT * FROM Sales WHERE Region='West'",
    "SELECT * FROM Sales WHERE Amount > 1000",
    "SELECT * FROM Sales"
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

    # Broadcast
    start = time.time()

    broadcast_result = execute_global_query(query)

    end = time.time()

    broadcast_time = end - start

    # Localization
    start = time.time()

    localized_result = execute_localized_query(query)

    end = time.time()

    localized_time = end - start

    speedup = 0

    if localized_time > 0:
        speedup = broadcast_time / localized_time

    results.append({
        "Query": query,
        "Broadcast Time": round(broadcast_time, 6),
        "Localized Time": round(localized_time, 6),
        "Speedup": round(speedup, 2),
        "Broadcast Rows": len(broadcast_result),
        "Localized Rows": len(localized_result)
    })

# =========================================
# RESULTS
# =========================================

df = pd.DataFrame(results)

print("\n====================================")
print(" FINAL BENCHMARK ")
print("====================================")

print(df)

# =========================================
# SAVE CSV
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logs_dir = os.path.join(BASE_DIR, "../logs")

os.makedirs(logs_dir, exist_ok=True)

output_file = os.path.join(
    logs_dir,
    "comparison_benchmark.csv"
)

df.to_csv(output_file, index=False)

print("\nBenchmark saved:")
print(output_file)