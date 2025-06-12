# export.py

import pandas as pd
from database import get_transactions
from eda_model import fetch_data, generate_report
from logger import logger

# Define column names based on database schema
COLUMNS = ["id", "amount", "description", "category", "type", "payment_method", "date"]

def export_to_csv():
    try:
        data = get_transactions()
        df = pd.DataFrame(data, columns=COLUMNS)
        df.to_csv("export.csv", index=False)
        logger.info("Transactions exported to export.csv")
    except Exception as e:
        logger.error(f"Failed to export to CSV: {e}")

def export_to_excel():
    try:
        data = get_transactions()
        df = pd.DataFrame(data, columns=COLUMNS)
        df.to_excel("export.xlsx", index=False)
        logger.info("Transactions exported to export.xlsx")
    except Exception as e:
        logger.error(f"Failed to export to Excel: {e}")

def export_eda():
    """Generate and save a data profiling report."""
    try:
        df = fetch_data("transactions")
        generate_report(df, output_path="reports/expense_report.html")
    except Exception as e:
        logger.error(f"Failed to generate EDA report: {e}")

if __name__ == "__main__":
    export_to_csv()
    export_to_excel()
    export_eda()
