# expense_tracker.py
class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self):
        amount = float(input("Enter the amount spent: "))
        description = input("Enter a brief description: ")
        category = input("Enter the category (e.g., food, transportation, entertainment): ")
        self.expenses.append({'amount': amount, 'description': description, 'category': category})

    def view_expenses(self):
        for expense in self.expenses:
            print(f"Amount: {expense['amount']}, Description: {expense['description']}, Category: {expense['category']}")

    def categorize_expenses(self):
        categories = {}
        for expense in self.expenses:
            category = expense['category']
            if category in categories:
                categories[category] += expense['amount']
            else:
                categories[category] = expense['amount']
        return categories

    def monthly_summary(self):
        total_amount = sum(expense['amount'] for expense in self.expenses)
        print(f"Total monthly expenses: {total_amount}")

    def category_wise_expenditure(self):
        categories = self.categorize_expenses()
        for category, amount in categories.items():
            print(f"Category: {category}, Expenditure: {amount}")

    def run(self):
        while True:
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Monthly Summary")
            print("4. Category-wise Expenditure")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.monthly_summary()
            elif choice == "4":
                self.category_wise_expenditure()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()