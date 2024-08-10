import tkinter as tk
from tkinter import messagebox

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Tracker")

        self.expenses = []

        self.amount_label = tk.Label(self.master, text="Amount:")
        self.amount_label.grid(row=0, column=0)

        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.grid(row=0, column=1)

        self.description_label = tk.Label(self.master, text="Description:")
        self.description_label.grid(row=1, column=0)

        self.description_entry = tk.Entry(self.master)
        self.description_entry.grid(row=1, column=1)

        self.category_label = tk.Label(self.master, text="Category:")
        self.category_label.grid(row=2, column=0)

        self.category_entry = tk.Entry(self.master)
        self.category_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.master, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.view_button = tk.Button(self.master, text="View Expenses", command=self.view_expenses)
        self.view_button.grid(row=4, column=0, columnspan=2)

        self.monthly_summary_button = tk.Button(self.master, text="Monthly Summary", command=self.monthly_summary)
        self.monthly_summary_button.grid(row=5, column=0, columnspan=2)

        self.category_wise_expenditure_button = tk.Button(self.master, text="Category-wise Expenditure", command=self.category_wise_expenditure)
        self.category_wise_expenditure_button.grid(row=6, column=0, columnspan=2)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit)
        self.exit_button.grid(row=7, column=0, columnspan=2)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            category = self.category_entry.get()
            self.expenses.append({'amount': amount, 'description': description, 'category': category})
            messagebox.showinfo("Success", "Expense added successfully.")
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")

    def view_expenses(self):
        expense_list = ""
        for expense in self.expenses:
            expense_list += f"Amount: {expense['amount']}, Description: {expense['description']}, Category: {expense['category']}\n"
        messagebox.showinfo("Expenses", expense_list)

    def monthly_summary(self):
        total_amount = sum(expense['amount'] for expense in self.expenses)
        messagebox.showinfo("Monthly Summary", f"Total monthly expenses: {total_amount}")

    def category_wise_expenditure(self):
        categories = {}
        for expense in self.expenses:
            category = expense['category']
            if category in categories:
                categories[category] += expense['amount']
            else:
                categories[category] = expense['amount']
        expenditure_list = ""
        for category, amount in categories.items():
            expenditure_list += f"Category: {category}, Expenditure: {amount}\n"
        messagebox.showinfo("Category-wise Expenditure", expenditure_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
