import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import datetime
from matplotlib import pyplot as plt


# File to store expenses
DATA_FILE = "expenses.json"

# Initialize data file if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"expenses": []}, f)

# Load data from the file
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save data to the file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Add an expense
def add_expense():
    date = entry_date.get()
    amount = entry_amount.get()
    category = category_var.get()
    description = entry_description.get()

    if not amount.isdigit() or not date or not category or not description:
        messagebox.showerror("Invalid Input", "Please provide valid inputs!")
        return

    expense = {
        "date": date,
        "amount": float(amount),
        "category": category,
        "description": description,
    }

    data = load_data()
    data["expenses"].append(expense)
    save_data(data)

    messagebox.showinfo("Success", "Expense added successfully!")
    clear_inputs()

# Clear input fields
def clear_inputs():
    entry_date.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    category_var.set(categories[0])

# Show summary (category-wise)
def show_summary():
    data = load_data()
    category_expenses = {}
    for expense in data["expenses"]:
        category = expense["category"]
        category_expenses[category] = category_expenses.get(category, 0) + expense["amount"]

    if not category_expenses:
        messagebox.showinfo("No Data", "No expenses to analyze.")
        return

    # Plotting category-wise expenses
    plt.bar(category_expenses.keys(), category_expenses.values(), color='skyblue')
    plt.title("Category-wise Expenses")
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")
    plt.show()

# UI Setup
app = tk.Tk()
app.title("Expense Tracker")
app.geometry("400x400")

# Inputs
tk.Label(app, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=10, pady=5)
entry_date = tk.Entry(app)
entry_date.grid(row=0, column=1, padx=10, pady=5)
entry_date.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

tk.Label(app, text="Amount").grid(row=1, column=0, padx=10, pady=5)
entry_amount = tk.Entry(app)
entry_amount.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="Category").grid(row=2, column=0, padx=10, pady=5)
category_var = tk.StringVar(app)
categories = ["Food", "Transport", "Entertainment", "Other"]
category_var.set(categories[0])
ttk.OptionMenu(app, category_var, *categories).grid(row=2, column=1, padx=10, pady=5)

tk.Label(app, text="Description").grid(row=3, column=0, padx=10, pady=5)
entry_description = tk.Entry(app)
entry_description.grid(row=3, column=1, padx=10, pady=5)

# Buttons
tk.Button(app, text="Add Expense", command=add_expense, bg="green", fg="white").grid(row=4, column=0, padx=10, pady=10)
tk.Button(app, text="View Summary", command=show_summary, bg="blue", fg="white").grid(row=4, column=1, padx=10, pady=10)
tk.Button(app, text="Clear", command=clear_inputs, bg="orange", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

# Run the app
app.mainloop()
