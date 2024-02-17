import pandas as pd
import tkinter as tk
from tkinter import messagebox


def record_expense():
    amount = amount_entry.get()
    description = description_entry.get()
    category = category_var.get()

    if not amount or not description or not category:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        float(amount)  
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number.")
        return

   
    new_expense = {'Amount': [amount], 'Description': [description], 'Category': [category]}
    df = pd.DataFrame(new_expense)

    try:
        existing_data = pd.read_csv('expenses.csv')
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass  

    df.to_csv('expenses.csv', index=False)

    messagebox.showinfo("Success", "Expense recorded successfully.")

    
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_var.set("")


def show_summary():
    try:
        df = pd.read_csv('expenses.csv')
        messagebox.showinfo("Expense Summary", f"Total Expenses: ${df['Amount'].sum()}\n\n{df.groupby('Category').sum()}")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No expenses recorded yet.")


root = tk.Tk()
root.title("Expense Tracker")

tk.Label(root, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Amount:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

categories = ["Food", "Movies", "Vacation","Travelling", "Snacks" ,"Grosaries","Bill Payments","School or clg Fees" ,"others"]
category_var = tk.StringVar(root)
category_var.set("")  
category_dropdown = tk.OptionMenu(root, category_var, *categories)
category_dropdown.grid(row=0, column=1, padx=10, pady=5)

amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=10, pady=5)

description_entry = tk.Entry(root)
description_entry.grid(row=2, column=1, padx=10, pady=5)

record_button = tk.Button(root, text="Record Expense", command=record_expense)
record_button.grid(row=3, column=0, columnspan=2, pady=10)
summary_button = tk.Button(root, text="Show Summary", command=show_summary)
summary_button.grid(row=4, column=0, columnspan=2, pady=10)


root.mainloop()
