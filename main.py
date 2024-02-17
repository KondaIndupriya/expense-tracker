import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font

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
    update_tables()

def show_summary():
    try:
        df = pd.read_csv('expenses.csv')
        messagebox.showinfo("Expense Summary", f"Total Expenses: ${df['Amount'].sum()}\n\n{df.groupby('Category').sum()}")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No expenses recorded yet.")

def update_tables():
    try:
        df = pd.read_csv('expenses.csv')

       
        for i in tree_amount.get_children():
            tree_amount.delete(i)
        for index, row in df.iterrows():
            tree_amount.insert("", "end", values=(row['Amount'],))

        
        for i in tree_category.get_children():
            tree_category.delete(i)
        for index, row in df.iterrows():
            tree_category.insert("", "end", values=(row['Category'],))

        
        for i in tree_description.get_children():
            tree_description.delete(i)
        for index, row in df.iterrows():
            tree_description.insert("", "end", values=(row['Description'],))

    except FileNotFoundError:
        pass

root = tk.Tk()
root.title("Expense Tracker")

custom_font = font.Font(size=10)

tk.Label(root, text="Category:", font=custom_font).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Amount:", font=custom_font).grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Description:", font=custom_font).grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

categories = ["Food", "Movies", "Vacation", "Travelling", "Snacks", "Groceries", "Bill Payments", "School or College Fees", "Others"]
category_var = tk.StringVar(root)
category_var.set("")  
category_dropdown = tk.OptionMenu(root, category_var, *categories)
category_dropdown.config(font=custom_font)
category_dropdown.grid(row=0, column=1, padx=10, pady=5)

amount_entry = tk.Entry(root, font=custom_font)
amount_entry.grid(row=1, column=1, padx=10, pady=5)

description_entry = tk.Entry(root, font=custom_font)
description_entry.grid(row=2, column=1, padx=10, pady=5)

record_button = tk.Button(root, text="Record Expense", command=record_expense, font=custom_font)
record_button.grid(row=3, column=0, columnspan=2, pady=10)

summary_button = tk.Button(root, text="Show Summary", command=show_summary, font=custom_font)
summary_button.grid(row=4, column=0, columnspan=2, pady=10)

tree_category = ttk.Treeview(root, columns=('Category',), show='headings')
tree_category.heading('Category', text='Category')
tree_category.grid(row=5, column=0, pady=10)


tree_amount = ttk.Treeview(root, columns=('Amount',), show='headings')
tree_amount.heading('Amount', text='Amount')
tree_amount.grid(row=5, column=1, pady=10)


tree_description = ttk.Treeview(root, columns=('Description',), show='headings')
tree_description.heading('Description', text='Description')
tree_description.grid(row=5, column=2, pady=10)

update_tables()  

root.mainloop()
