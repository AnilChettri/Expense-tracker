# visualizations.py

import pandas as pd
import plotly.express as px
import sqlite3
from logger import logger

DB_PATH = "expense_tracker.db"

def fetch_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM transactions", conn)
        conn.close()
        df['date'] = pd.to_datetime(df['date'])
        logger.info("Data loaded for visualization.")
        return df
    except Exception as e:
        logger.error(f"Failed to load data for visualization: {e}")
        return pd.DataFrame()

def plot_dynamic_summary(df):
    """Smart LLM-like visual decision engine"""
    if df.empty:
        return px.bar(title="📉 No Data Available")

    if df['category'].nunique() == 1:
        # Not enough categorical variety — show trend over time
        return plot_time_series(df)
    elif df.shape[0] < 10:
        # Few entries — show pie chart
        return plot_category_pie(df)
    else:
        # General default — show bar chart
        return plot_category_summary(df)

def plot_category_summary(df):
    summary = df.groupby('category')['amount'].sum().reset_index().sort_values(by='amount', ascending=False)
    fig = px.bar(summary, x='category', y='amount', title="🧾 Total Amount by Category",
                 text_auto=True, color='amount')
    fig.update_layout(xaxis_title="Category", yaxis_title="Total Amount")
    return fig

def plot_time_series(df):
    df['net_amount'] = df.apply(lambda row: row['amount'] if row['type'] == 'income' else -row['amount'], axis=1)
    time_series = df.groupby(df['date'].dt.date)['net_amount'].sum().cumsum().reset_index()
    time_series.columns = ['Date', 'Net Spending']
    fig = px.line(time_series, x='Date', y='Net Spending', markers=True,
                  title="📈 Cumulative Net Spending Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="Net Amount")
    return fig

def plot_category_pie(df):
    df_exp = df[df['type'] == 'expense']
    if df_exp.empty or df_exp['category'].nunique() < 2:
        return px.pie(values=[1], names=["No variety"], title="💸 Expense Distribution")
    pie_data = df_exp.groupby('category')['amount'].sum().reset_index()
    fig = px.pie(pie_data, values='amount', names='category', title='💸 Expense Distribution by Category',
                 hole=0.4)
    return fig
