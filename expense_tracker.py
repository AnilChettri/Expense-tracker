import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# File to store expenses
DATA_FILE = 'data.json'

# Load expenses from file
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Save expenses to file
def save_expenses(expenses):
    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

# Add a new expense
def add_expense(amount, description, category):
    expenses = load_expenses()
    expense = {
        'amount': amount,
        'description': description,
        'category': category,
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    expenses.append(expense)
    save_expenses(expenses)
    messagebox.showinfo("Success", "Expense added successfully.")
    update_summary()

# Print expense summary
def update_summary():
    expenses = load_expenses()
    categories = {}
    monthly_expenses = {}

    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        date = datetime.strptime(expense['date'], '%Y-%m-%d')
        month_year = date.strftime('%Y-%m')

        if category not in categories:
            categories[category] = 0
        categories[category] += amount

        if month_year not in monthly_expenses:
            monthly_expenses[month_year] = 0
        monthly_expenses[month_year] += amount

    # Clear the text area and update it with new data
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, "Category-wise Expenditure:\n")
    for category, total in categories.items():
        summary_text.insert(tk.END, f"{category}: ${total:.2f}\n")

    summary_text.insert(tk.END, "\nMonthly Summary:\n")
    for month_year, total in monthly_expenses.items():
        summary_text.insert(tk.END, f"{month_year}: ${total:.2f}\n")

# Add expense form
def add_expense_form():
    try:
        amount = float(amount_entry.get())
        description = description_entry.get()
        category = category_entry.get()
        add_expense(amount, description, category)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount.")

# Create main application window
root = tk.Tk()
root.title("Expense Tracker")

# Create and place widgets
tk.Label(root, text="Amount").grid(row=0, column=0, padx=10, pady=10)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Description").grid(row=1, column=0, padx=10, pady=10)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Category").grid(row=2, column=0, padx=10, pady=10)
category_entry = tk.Entry(root)
category_entry.grid(row=2, column=1, padx=10, pady=10)

add_button = tk.Button(root, text="Add Expense", command=add_expense_form)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

summary_text = tk.Text(root, width=50, height=15)
summary_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

update_summary()

root.mainloop()
