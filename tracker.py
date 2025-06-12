import streamlit as st
import pandas as pd
from database import (
    add_transaction,
    get_transactions,
    edit_transaction,
    delete_transaction,
    set_budget,
    get_budgets,
    reset_data,
    create_tables
)
from datetime import datetime
from logger import logger
from eda_model import fetch_data, generate_report
from visualizations import (
    plot_category_summary,
    plot_time_series,
    plot_category_pie
)

import threading

# Initialize Database Tables
create_tables()
logger.info("Database tables ensured.")

st.title("💰 Expense Tracker")
logger.info("Streamlit app launched.")

menu = ["Add Transaction", "View Summary", "Set Budget", "Manage Transactions", "Reset Data"]
choice = st.sidebar.selectbox("Menu", menu)

def background_eda():
    """Run analytics in the background to avoid slowing down Streamlit."""
    try:
        df = fetch_data("transactions")
        generate_report(df, output_path="reports/expense_report.html")
    except Exception as e:
        logger.error(f"Failed to generate background EDA: {e}")

if choice == "Add Transaction":
    st.header("Add a New Transaction")
    txn_date = st.date_input("Date", datetime.now()).strftime('%Y-%m-%d')
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    description = st.text_input("Description", "Enter a short note...")
    category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Travel", "Entertainment", "Other"])
    txn_type = st.radio("Transaction Type", ["expense", "income"])
    payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "Other"])

    if st.button("Add Transaction"):
        if amount > 0:
            add_transaction(amount, description, category, txn_type, payment_method, txn_date)
            st.success(f"{txn_type.capitalize()} added successfully!")
            logger.info(f"Transaction added: {amount} - {category} - {txn_type} on {txn_date}")
            threading.Thread(target=background_eda).start()  # Run EDA after new transaction
        else:
            st.error("Amount must be greater than 0.")
            logger.warning("Attempted to add transaction with zero amount.")

elif choice == "View Summary":
    st.header("Summary & Analytics")
    transactions = get_transactions()
    if not transactions:
        st.info("No transactions found.")
        logger.info("User viewed summary but no transactions exist.")
    else:
        df = pd.DataFrame(transactions, columns=['id', 'amount', 'description', 'category', 'type', 'payment_method', 'date'])
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)
        df['net_amount'] = df.apply(lambda row: row['amount'] if row['type'] == 'income' else -row['amount'], axis=1)

        st.subheader("📋 All Transactions")
        st.dataframe(df[['date', 'type', 'amount', 'category', 'description', 'payment_method']])
        logger.info("Displayed transaction summary.")

        # Real-Time Visualizations
        st.subheader("📊 Visual Analytics")
        st.plotly_chart(plot_category_summary(df), use_container_width=True)
        st.plotly_chart(plot_time_series(df), use_container_width=True)
        st.plotly_chart(plot_category_pie(df), use_container_width=True)

elif choice == "Manage Transactions":
    st.header("Edit or Delete Transactions")
    transactions = get_transactions()
    if not transactions:
        st.info("No transactions to manage.")
        logger.info("User accessed Manage Transactions with no data.")
    else:
        df = pd.DataFrame(transactions, columns=['id', 'amount', 'description', 'category', 'type', 'payment_method', 'date'])
        selected_id = st.selectbox("Select Transaction ID", df["id"].tolist())

        if selected_id:
            txn = df[df['id'] == selected_id].iloc[0]
            amount = st.number_input("Amount", value=txn['amount'])
            description = st.text_input("Description", txn['description'])
            category = st.text_input("Category", txn['category'])
            txn_type = st.radio("Transaction Type", ["expense", "income"], index=0 if txn['type'] == "expense" else 1)
            payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "Other"], index=0)

            if st.button("Update Transaction"):
                edit_transaction(selected_id, amount, description, category, txn_type, payment_method, txn['date'])
                st.success("Transaction updated successfully!")
                logger.info(f"Transaction {selected_id} updated.")

            if st.button("Delete Transaction"):
                delete_transaction(selected_id)
                st.warning("Transaction deleted!")
                logger.warning(f"Transaction {selected_id} deleted.")

elif choice == "Set Budget":
    st.header("Set or Update Budget")
    category = st.text_input("Category")
    budget_amount = st.number_input("Budget Amount", min_value=0.0, step=0.01)
    if st.button("Set Budget"):
        set_budget(category, budget_amount)
        st.success(f"Budget for '{category}' set to ${budget_amount:.2f}")
        logger.info(f"Budget set: {category} = {budget_amount}")

elif choice == "Reset Data":
    st.warning("⚠️ This will delete all transactions and budgets!")
    if st.button("Reset All Data"):
        reset_data()
        st.success("All data has been reset.")
        logger.warning("All data was reset by user.")
