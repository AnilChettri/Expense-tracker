# eda_model.py

import sqlite3
import pandas as pd
from ydata_profiling import ProfileReport
import os
from logger import logger  # Ensure logger.py exists and is correctly configured

DB_PATH = "expense_tracker.db"  # Make sure this path is correct

def fetch_data(table_name="transactions"):
    """Fetch data from the given table in the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        logger.info(f"Fetched {len(df)} rows from table '{table_name}'.")
        return df
    except Exception as e:
        logger.error(f"Error fetching data from {table_name}: {e}")
        return pd.DataFrame()

def generate_report(df, output_path="reports/expense_report.html"):
    """Generate an HTML report using ydata-profiling."""
    if df.empty:
        logger.warning("No data to analyze. Report not generated.")
        return

    profile = ProfileReport(df, title="Expense Tracker Report", explorative=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    profile.to_file(output_path)
    logger.info(f"EDA report saved to {output_path}")

if __name__ == "__main__":
    df = fetch_data("transactions")
    generate_report(df)
