import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class BudgetTracker:
    def __init__(self):
        self.transactions = pd.DataFrame(columns=['date', 'name', 'type', 'amount', 'category', 'balance'])

    def add_transaction(self, name, t_type, date, amount, category):
        balance = self.get_current_balance() + amount
        new_row = pd.Series({'date': date, 'name': name, 'type': t_type, 'amount': amount, 'category': category, 'balance': balance})
        new_df = pd.DataFrame([new_row])
        self.transactions = pd.concat([self.transactions, new_df], ignore_index=True)

    def get_current_balance(self):
        if self.transactions.empty:
            return 0
        return self.transactions.iloc[-1]['balance']

    def save_data(self, filename):
        self.transactions.to_csv(filename, index=False)

    def load_data(self, filename):
        self.transactions = pd.read_csv(filename)

    def save_data_to_excel(self, filename):
        self.transactions.to_excel(filename, index=False, engine='openpyxl')


def on_add_transaction():
    try:
        name = entry_name.get()
        t_type = transaction_type.get()
        month = months.index(months_var.get()) + 1
        day = int(entry_day.get())
        year = datetime.now().year
        date = f"{year}-{month}-{day}"
        amount = float(entry_amount.get())
        category = category_var.get()
        if t_type == "Expense":
            amount = -amount

        tracker.add_transaction(name, t_type, date, amount, category)
        update_balance_display()

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid data")

def update_balance_display():
    balance_label.config(text=f"Current balance: {tracker.get_current_balance()}")

def on_plot_balance():
    # Create a new window
    graph_window = tk.Toplevel()
    graph_window.title("Balance Graph")

    # Create a figure and axis object for the graph
    fig, ax = plt.subplots()

    # Plot the balance data on the axis object
    tracker.transactions.plot(x='date', y='balance', kind='line', ax=ax)

    # Create a canvas to display the graph
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Create a toolbar for the graph
    toolbar = NavigationToolbar2Tk(canvas, graph_window)
    toolbar.update()
    canvas.get_tk_widget().pack()

def on_save_excel():
    excel_file = "budget_data.xlsx"
    tracker.save_data_to_excel(excel_file)
    messagebox.showinfo("Data saved", f"Data saved to {excel_file}")

def main():
    global tracker, entry_name, transaction_type, months_var, months, entry_day, entry_amount, category_var, balance_label

    tracker = BudgetTracker()
    # Load previous data if available
    data_file = 'budget_data.csv'
    try:
        tracker.load_data(data_file)
    except FileNotFoundError:
        pass  # File not found, starting with an empty budget tracker

    # Create the main window
    root = tk.Tk()
    root.title("Budget Tracker")

    # Define the months list
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Create input fields and labels
    input_frame = tk.LabelFrame(root, text="Input")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    entry_name = tk.Entry(input_frame)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5)
    transaction_type = ttk.Combobox(input_frame, values=("Income", "Expense"), state="readonly")
    transaction_type.set("Income")
    transaction_type.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Month:").grid(row=2, column=0, padx=5, pady=5)
    months_var = tk.StringVar()
    months_combobox = ttk.Combobox(input_frame, textvariable=months_var, values=months, state="readonly")
    months_combobox.set(months[datetime.now().month - 1])  # Set the current month
    months_combobox.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Day:").grid(row=3, column=0, padx=5, pady=5)
    entry_day = tk.Entry(input_frame)
    entry_day.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Amount:").grid(row=4, column=0, padx=5, pady=5)
    entry_amount = tk.Entry(input_frame)
    entry_amount.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Category:").grid(row=5, column=0, padx=5, pady=5)
    category_var = tk.StringVar()
    categories = ttk.Combobox(input_frame, textvariable=category_var,
                              values=("Entertainment", "Savings", "Rent", "Utilities", "Food"), state="readonly")
    categories.set("Entertainment")
    categories.grid(row=5, column=1, padx=5, pady=5)

    # Create a button for adding transactions
    tk.Button(input_frame, text="Add Transaction", command=on_add_transaction).grid(row=6, column=0, columnspan=2,
                                                                                    padx=5, pady=5)

    # Create a label to display the current balance
    balance_label = tk.Label(root, text="")
    balance_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    update_balance_display()

    # Create a button to display the balance graph
    tk.Button(root, text="Plot Balance", command=on_plot_balance).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Create a button to save data as an Excel file
    tk.Button(root, text="Save to Excel", command=on_save_excel).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Run the main loop
    root.mainloop()


if __name__ == '__main__':
    main()
