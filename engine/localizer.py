import sqlite3
import pandas as pd
from datetime import datetime
import time
import os

# =========================================
# DATABASE CONFIGURATION
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    "North": os.path.join(BASE_DIR, "../databases/sales_north.db"),
    "South": os.path.join(BASE_DIR, "../databases/sales_south.db"),
    "West": os.path.join(BASE_DIR, "../databases/sales_west.db")
}

# =========================================
# GLOBAL STATISTICS
# =========================================

query_count = 0
query_history = []

# =========================================
# DETECT TARGET SITE
# =========================================

def detect_target_site(query):

    query_lower = query.lower()

    if "region='north'" in query_lower:
        return ["North"]

    elif "region='south'" in query_lower:
        return ["South"]

    elif "region='west'" in query_lower:
        return ["West"]

    else:
        return list(DATABASES.keys())

# =========================================
# LOGGING SYSTEM
# =========================================

def write_log(query, target_sites, rows, execution_time):

    log_dir = os.path.join(BASE_DIR, "../logs")

    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "query.log")

    with open(log_file, "a", encoding="utf-8") as f:

        f.write("\n============================\n")
        f.write(f"TIME: {datetime.now()}\n")
        f.write(f"QUERY: {query}\n")
        f.write(f"TARGET SITES: {target_sites}\n")
        f.write(f"ROWS RETURNED: {rows}\n")
        f.write(f"EXECUTION TIME: {execution_time:.6f}\n")

# =========================================
# EXECUTE QUERY ON SINGLE SITE
# =========================================

def execute_query_on_site(site_name, db_path, query):

    print("\n====================================")
    print(f"[SITE] {site_name}")
    print(f"[QUERY] {query}")
    print("====================================")

    try:

        start_time = time.time()

        if not os.path.exists(db_path):
            print(f"[ERROR] Database not found: {db_path}")
            return pd.DataFrame()

        conn = sqlite3.connect(db_path)

        result = pd.read_sql_query(query, conn)

        conn.close()

        end_time = time.time()

        print(f"[SUCCESS] Query executed on {site_name}")
        print(f"[TIME] {end_time - start_time:.6f} seconds")
        print(f"[ROWS] {len(result)}")

        return result

    except Exception as e:

        print(f"[ERROR] {site_name}: {e}")

        return pd.DataFrame()

# =========================================
# LOCALIZED QUERY EXECUTION
# =========================================

def execute_localized_query(query):

    print("\n########################################")
    print(" QUERY LOCALIZATION ENGINE ")
    print("########################################")

    global_start = time.time()

    # Detect target fragments
    target_sites = detect_target_site(query)

    nodes_contacted = len(target_sites)

    print(f"\n[LOCALIZER] Target Sites: {target_sites}")

    final_result = pd.DataFrame()

    for site_name in target_sites:

        db_path = DATABASES[site_name]

        result = execute_query_on_site(
            site_name,
            db_path,
            query
        )

        final_result = pd.concat(
            [final_result, result],
            ignore_index=True
        )

    global_end = time.time()

    total_time = global_end - global_start

    write_log(
        query,
        target_sites,
        len(final_result),
        total_time
    )

    print("\n========== STATISTICS ==========")
    print(f"[STAT] Nodes Contacted: {nodes_contacted}")
    print(f"[STAT] Rows Returned : {len(final_result)}")
    print(f"[STAT] Total Time    : {total_time:.6f} sec")
    print("================================")

    return final_result

# =========================================
# SHOW QUERY HISTORY
# =========================================

def show_history():

    print("\n========== QUERY HISTORY ==========")

    if len(query_history) == 0:
        print("No query history.")
        return

    for i, q in enumerate(query_history, start=1):
        print(f"{i}. {q}")

# =========================================
# MAIN PROGRAM
# =========================================

if __name__ == "__main__":

    print("\n====================================")
    print(" DISTRIBUTED QUERY LOCALIZATION ")
    print("====================================")

    print("\nCommands:")
    print("exit    -> Quit")
    print("history -> Show query history")

    while True:

        print("\n------------------------------------")
        print("Example Queries:")
        print("1. SELECT * FROM Sales")
        print("2. SELECT * FROM Sales WHERE Region='North'")
        print("3. SELECT * FROM Sales WHERE Region='South'")
        print("4. SELECT * FROM Sales WHERE Region='West'")
        print("5. SELECT * FROM Sales WHERE Amount > 1000")
        print("\nType 'exit' to quit program.")
        print("------------------------------------")

        query = input("\nEnter SQL Query:\n> ")

        if query.lower() == "exit":
            print("\nExiting...")
            break

        if query.lower() == "history":
            show_history()
            continue

        query_count += 1
        query_history.append(query)

        print(f"\n[QUERY #{query_count}]")

        output = execute_localized_query(query)

        print("\n====================================")
        print(" FINAL RESULT ")
        print("====================================")

        if output.empty:
            print("No results.")
        else:
            print(output)

        print("\n====================================")
        print(" READY FOR NEXT QUERY ")
        print("====================================")