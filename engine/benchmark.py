import time
import pandas as pd
import os

from localizer import execute_localized_query

# =========================================
# BENCHMARK CONFIGURATION
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

benchmark_results = []

print("\n====================================")
print(" DISTRIBUTED QUERY BENCHMARK ")
print("====================================")

for query in queries:

    print("\n------------------------------------")
    print(f"Running Query:")
    print(query)
    print("------------------------------------")

    start_time = time.time()

    result = execute_localized_query(query)

    end_time = time.time()

    execution_time = end_time - start_time

    benchmark_results.append({
        "Query": query,
        "Rows Returned": len(result),
        "Execution Time (sec)": round(execution_time, 6)
    })

# =========================================
# RESULT TABLE
# =========================================

df = pd.DataFrame(benchmark_results)

print("\n====================================")
print(" BENCHMARK RESULTS ")
print("====================================")

print(df)

# =========================================
# SAVE CSV
# =========================================

logs_dir = os.path.join(BASE_DIR, "../logs")

os.makedirs(logs_dir, exist_ok=True)

csv_path = os.path.join(logs_dir, "benchmark.csv")

df.to_csv(csv_path, index=False)

print("\n====================================")
print(f"Benchmark saved to:")
print(csv_path)
print("====================================")