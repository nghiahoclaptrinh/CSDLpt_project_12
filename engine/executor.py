import sqlite3
import pandas as pd
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    "North": os.path.join(BASE_DIR, "../databases/sales_north.db"),
    "South": os.path.join(BASE_DIR, "../databases/sales_south.db"),
    "West": os.path.join(BASE_DIR, "../databases/sales_west.db")
}


# =========================================
# EXECUTE QUERY ON SINGLE SITE
# =========================================
def execute_query_on_site(site_name, db_path, query):

    print("\n====================================")
    print(f"[SITE] {site_name}")
    print(f"[DATABASE] {db_path}")
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

        execution_time = end_time - start_time

        print(f"[SUCCESS] Query executed on {site_name}")
        print(f"[TIME] {execution_time:.6f} seconds")
        print(f"[ROWS RETURNED] {len(result)}")

        return result

    except Exception as e:

        print(f"[ERROR] Failed to execute query on {site_name}")
        print(f"[DETAILS] {e}")
        print("[WARNING] Continuing with remaining sites...")

        return pd.DataFrame()


# =========================================
# EXECUTE GLOBAL QUERY
# =========================================
def execute_global_query(query):

    print("\n")
    print("########################################")
    print("GLOBAL QUERY EXECUTION STARTED")
    print("########################################")

    final_result = pd.DataFrame()

    for site_name, db_path in DATABASES.items():

        site_result = execute_query_on_site(
            site_name,
            db_path,
            query
        )

        final_result = pd.concat(
            [final_result, site_result],
            ignore_index=True
        )

    print("\n########################################")
    print("GLOBAL QUERY EXECUTION FINISHED")
    print("########################################")

    return final_result


# =========================================
# MAIN PROGRAM
# =========================================
if __name__ == "__main__":

    print("\n====================================")
    print(" DISTRIBUTED QUERY EXECUTION ENGINE ")
    print("====================================")

    print("\nType 'exit' to quit program.")

    while True:

        print("\n------------------------------------")
        print("Available Example Queries:")
        print("1. SELECT * FROM Sales")
        print("2. SELECT * FROM Sales WHERE Amount > 1000")
        print("3. SELECT * FROM Sales WHERE Region='North'")
        print("4. SELECT COUNT(*) FROM Sales")
        print("------------------------------------")

        query = input("\nEnter SQL Query:\n> ")

        # Exit condition
        if query.lower() == "exit":
            print("\nExiting program...")
            break

        # Execute query
        final_output = execute_global_query(query)

        # Display result
        print("\n")
        print("====================================")
        print(" FINAL AGGREGATED RESULT ")
        print("====================================")

        if final_output.empty:
            print("\nNo results returned.")
        else:
            print(final_output)

        print("\n====================================")
        print(" READY FOR NEXT QUERY ")
        print("====================================")