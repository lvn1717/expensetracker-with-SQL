import mysql.connector


# Define the Expense class
class Expense:
    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

# Define the ExpenseTracker class
class ExpenseTracker:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="", #server host from MySQL
            user="",  #MySQL username
            password="",  #MySQL password
            database="expense_tracker"
        )
        self.cursor = self.conn.cursor()

    def add_expense(self, expense):
        sql = "INSERT INTO expenses (date, description, amount, category) VALUES (%s, %s, %s, %s)"
        val = (expense.date, expense.description, expense.amount, expense.category)
        self.cursor.execute(sql, val)
        self.conn.commit()
        print("Expense added successfully.")

    def remove_expense(self, index):
        sql = "SELECT id FROM expenses ORDER BY id LIMIT %s, 1"
        self.cursor.execute(sql, (index,))
        result = self.cursor.fetchone()

        if result:
            expense_id = result[0]
            sql = "DELETE FROM expenses WHERE id = %s"
            self.cursor.execute(sql, (expense_id,))
            self.conn.commit()
            print("Expense removed successfully.")
        else:
            print("Invalid expense index.")
        
    def view_expenses(self):
        self.cursor.execute("SELECT id, date, description, amount, category FROM expenses")
        expenses = self.cursor.fetchall()
        if not expenses:
            print("No expenses found.")
        else:
            print("Expense list:")
            for i, expense in enumerate(expenses, start=1):
                print(f"{i}. Date: {expense[1]}, Description: {expense[2]}, Category: {expense[4]}, Amount: ${expense[3]:.2f}")
    
    def total_expenses(self):
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        total = self.cursor.fetchone()[0]
        total = total if total else 0
        print(f"Total Expenses: ${total:.2f}")

    def close(self):
        self.cursor.close()
        self.conn.close()

# Define the main function
def main():
    tracker = ExpenseTracker()

    try:
        while True:
            print("**************************")
            print("     Expense Tracker      ")
            print("**************************")
            print("1. Add Expense")
            print("2. Remove Expense")
            print("3. View Expenses")
            print("4. Total Expenses")
            print("5. Exit")
        
            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                date = input("Enter the date (YYYY-MM-DD): ")
                description = input("Enter the description: ")
                amount = float(input("Enter the amount: "))
                category = input("Enter the category: ")
                
                # Create an instance of the Expense class
                expense = Expense(date, description, amount, category)
                
                # Add the expense to the tracker
                tracker.add_expense(expense)
            elif choice == "2":
                index = int(input("Enter the expense index to remove: ")) - 1
                tracker.remove_expense(index)
            elif choice == "3":
                tracker.view_expenses()
            elif choice == "4":
                tracker.total_expenses()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        tracker.close()

if __name__ == "__main__":
    main()
