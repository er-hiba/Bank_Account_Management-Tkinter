from tkinter import *
from tkinter import ttk
from account_classes import Account, CurrentAccount, SavingsAccount
from datetime import datetime
import json


# Initializing the Tkinter root window
root = Tk()
root.title("Bank Management System")  # Setting title for the window
# Change the background color of the window
root.configure(bg='#D9C0C9')

# Function to clear all entry fields in the GUI
def clear_entry_fields():
    entry_owner.delete(0, 'end')
    entry_balance.delete(0, 'end')
    entry_interest.delete(0, 'end')
    entry_overdraft.delete(0, 'end')

# Function to update entry states based on account type selection
def update_entry_state():
    if account_type.get() == 'Savings':
        entry_interest.config(state='normal')
        entry_overdraft.config(state='disabled')
    else:
        entry_interest.config(state='disabled')
        entry_overdraft.config(state='normal')

# Attempt to load existing data from file (if it exists)
try:
    with open('account_data.json', 'r') as file:
        account_data_list = json.load(file)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    # If the file doesn't exist or is empty, initialize an empty list
    account_data_list = []

# Function to create a new account
def create_account():

    # Retrieving data entered in the GUI for the new account creation
    number = Account.get_counter()
    owner = entry_owner.get()
    balance = float(entry_balance.get()) if entry_balance.get() else 0.0
    interest = float(entry_interest.get()) if entry_interest.get() else 0.0
    overdraft = float(entry_overdraft.get()) if entry_overdraft.get() else 0.0

    # Current date as the account opening date
    opening_date = datetime.now().strftime("%Y-%m-%d")

    # Creating a new account object based on the selected account type
    if account_type.get() == 'Current':
        new_account = CurrentAccount(number, owner, balance, opening_date, overdraft)
    else:
        new_account = SavingsAccount(number, owner, balance, opening_date, interest)

    # Inserting account details into the TreeView
    tree.insert('', 'end', values=(new_account.get_number, new_account.get_owner, new_account.get_balance, 
                                   'Current' if isinstance(new_account, CurrentAccount) else 'Savings',
                                   new_account.get_interest if isinstance(new_account, SavingsAccount) else '',
                                   new_account.get_overdraft if isinstance(new_account, CurrentAccount) else ''))

    # Centering data in the table columns
    for col in range(6):
        tree.column(col, anchor='center')

    # Collecting account data in a dictionary
    account_data = {
        "Number": new_account.get_number,
        "Owner": new_account.get_owner,
        "Initial Balance": new_account.get_balance,
        "Type": 'Current' if isinstance(new_account, CurrentAccount) else 'Savings',
        "Interest Rate": new_account.get_interest if isinstance(new_account, SavingsAccount) else '',
        "Overdraft Amount": new_account.get_overdraft if isinstance(new_account, CurrentAccount) else ''
    }
    
    account_data_list.append(account_data)  # Appending account data dictionary to the list

    # Write the entire updated list back to the file
    with open('account_data.json', 'w') as file:
        json.dump(account_data_list, file, indent=2)

    label_num.config(text= Account.get_counter())

    # Clearing entry fields to reset input fields after creating an account
    clear_entry_fields()

# Function to load account data from the 'account_data.json' file and inserts it into the table (Treeview).
def load_data_from_file():
    with open('account_data.json', 'r') as file:
        data = json.load(file)
        for account in data:
            tree.insert('', 'end', values=(
                account["Number"], account["Owner"], account["Initial Balance"],
                account["Type"], account["Interest Rate"], account["Overdraft Amount"]))

    max_account_number = max(account['Number'] for account in data)
    Account.set_counter(max_account_number + 1)
    label_num.config(text= Account.get_counter())

    # Centering data in the table columns
    for col in range(6):
        tree.column(col, anchor='center')

# Initializing account type variable
account_type = StringVar()
account_type.set('')

# Labels and Entries for account details
label_number = Label(root, text="Number:", bg='#D9C0C9', fg='#333333', font=('Consolas',12))
label_num = Label(root, text=Account.get_counter(), bg='#D9C0C9', font=('Consolas',12))
label_owner = Label(root, text="Owner:", bg='#D9C0C9', fg='#333333', font=('Consolas',12))
entry_owner = Entry(root, bg='#F2E5E9', font=('Consolas',12))
label_balance = Label(root, text="Initial Balance:", bg='#D9C0C9', fg='#333333', font=('Consolas',12))
entry_balance= Entry(root, bg='#F2E5E9', font=('Consolas',12))
label_currency = Label(root, text="MAD", bg='#D9C0C9', font=('Consolas',12))
label_account_type = Label(root, text="Account Type:", bg='#D9C0C9', fg='#333333', font=('Consolas',12))
# Radio buttons for selecting account type
label_current = Radiobutton(root, bg='#D9C0C9', font=('Consolas',12), text="Current", variable=account_type, value='Current', command=update_entry_state)
label_savings = Radiobutton(root, bg='#D9C0C9', font=('Consolas',12), text="Savings", variable=account_type, value='Savings', command=update_entry_state)
# Labels and Entries for interest rate and overdraft amount
label_interest = Label(root, text="Interest Rate:", bg='#D9C0C9', fg='#333333', font=('Consolas',12))
entry_interest = Entry(root, state='disabled', bg='#F2E5E9', font=('Consolas',12))
label_percentage = Label(root, bg='#D9C0C9', text="%", font=('Consolas',12))
label_overdraft = Label(root, text="Overdraft Amount:", bg='#D9C0C9', fg='#333333', font=('Consolas',12))
entry_overdraft = Entry(root, state='normal',bg='#F2E5E9', font=('Consolas',12))
# Button for creating accounts
button_create = Button(root, text="Create Account", command=create_account, bg='#F3A281', font=('Consolas',11))

# Widget placement and layout in the GUI
label_number.place(x=10, y=10)
label_num.place(x=190, y=10)
label_owner.place(x=10, y=40)
entry_owner.place(x=190, y=40)
label_balance.place(x=10, y=70)
entry_balance.place(x=190, y=70)
label_currency.place(x=380, y=70)
label_account_type.place(x=10, y=100)
label_current.place(x=190, y=100)
label_savings.place(x=290, y=100)
label_interest.place(x=10, y=130)
entry_interest.place(x=190, y=130)
label_percentage.place(x=380, y=130)
label_overdraft.place(x=10, y=170)
entry_overdraft.place(x=190, y=170)
button_create.place(x=120, y=210)

# Treeview for displaying account details
tree = ttk.Treeview(root, columns=('Number', 'Owner', 'Initial Balance', 'Type', 'Interest Rate', 'Overdraft Amount'), show='headings')
# Columns for different account details in Treeview
tree.heading('Number', text='Number')
tree.heading('Owner', text='Owner')
tree.heading('Initial Balance', text='Initial Balance')
tree.heading('Type', text='Type')
tree.heading('Interest Rate', text='Interest Rate')
tree.heading('Overdraft Amount', text='Overdraft Amount')
tree.place(x=10, y=270) # Positioning table (Treeview) displaying account data
# Load existing account data from the 'account_data.json' file when the GUI is initialized
load_data_from_file()

# Starting the main event loop
root.mainloop()
