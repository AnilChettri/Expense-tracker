# report_export.py

import pandas as pd
from jinja2 import Template
from weasyprint import HTML
from database import get_transactions
from analytics.visualizations import plot_category_summary, plot_time_series, plot_category_pie
from logger import logger
import os

def generate_report_html(df):
    bar = plot_category_summary(df).to_html(full_html=False, include_plotlyjs='cdn')
    line = plot_time_series(df).to_html(full_html=False, include_plotlyjs='cdn')
    pie = plot_category_pie(df).to_html(full_html=False, include_plotlyjs='cdn')

    template = Template("""
    <html>
    <head><title>Expense Report</title></head>
    <body>
        <h1>📊 Expense Report</h1>
        <h2>Summary Table</h2>
        {{ table | safe }}
        <h2>Category Breakdown</h2>
        {{ bar | safe }}
        <h2>Time Series</h2>
        {{ line | safe }}
        <h2>Spending Distribution</h2>
        {{ pie | safe }}
    </body>
    </html>
    """)

    return template.render(table=df.to_html(index=False), bar=bar, line=line, pie=pie)

def export_pdf(output_file="reports/expense_report.pdf"):
    df = pd.DataFrame(get_transactions(), columns=["id", "amount", "description", "category", "type", "payment_method", "date"])
    html = generate_report_html(df)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    HTML(string=html).write_pdf(output_file)
    logger.info(f"✅ PDF report saved to {output_file}")

if __name__ == "__main__":
    export_pdf()
