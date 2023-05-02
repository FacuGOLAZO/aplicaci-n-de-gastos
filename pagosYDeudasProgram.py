import tkinter as tk
from tkinter import simpledialog
import json
import os

root = tk.Tk()

# Set the size of the window 
root.geometry("400x800")

# Set title
root.title("Gastos")

# Create a label to prompt the user to select a user
user_label = tk.Label(root, text="Select a user:")
user_label.pack()


# Create a list of users with their initial balance

if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    with open("users.json", "w") as f:
        users = [[simpledialog.askstring("New user", "Enter the name of the new user:"), 0]]
        json.dump(users, f)
# Create a list to store the variables associated with each user's balance
balances = [tk.DoubleVar(root, value=balance) for _, balance in users]

# Create an OptionMenu widget for the user to select a user
selected_user = tk.StringVar(root)
selected_user.set(users[0][0])  # Set the initial value of the OptionMenu to the first user
user_menu = tk.OptionMenu(root, selected_user, *tuple(name for name, _ in users))
user_menu.pack()

# Create a label to display the balance of the selected user
balance_label = tk.Label(root)
balance_label.pack()

# create function to uptade balance
def uptade_balance():
    balance_text = "\n".join([f"{name}: {balance.get()}" for (name, _), balance in zip(users, balances)])
    balance_label.config(text=balance_text)

# show balance
uptade_balance()

# Create a button to add a new user
def add_user():
    # Get the name of the new user from the user
    new_user_name = simpledialog.askstring("New user", "Enter the name of the new user:")
    if new_user_name:
        # Check if the user already exists
        if any(user_name.lower() == new_user_name.lower() for user_name, _ in users):
            result_label.config(text=f"{new_user_name} already exists!")
        else:
            # Add the new user to the list of users with a balance of zero
            users.append([new_user_name, 0])
            # Add a new variable to store the balance for the new user
            balances.append(tk.DoubleVar(root, value=0))
            # Update the OptionMenu with the new user
            user_menu["menu"].add_command(label=new_user_name, command=tk._setit(selected_user, new_user_name))
            # Update the OptionMenu with the new user
            pay_user_menu["menu"].add_command(label=new_user_name, command=tk._setit(selected_pay_user, new_user_name))
            # Uptade balance
            uptade_balance()
            # Save the user
            save_to_json()

        
# funtion to delete a user

def delete_user(user_name):
    # Find the index of the user to delete
    user_index = [name for name, _ in users].index(user_name)

    # add an user if user want to delete last user
    while len(users)==1:
        new_user_name = None
        while new_user_name==None and new_user_name!="":
            new_user_name = simpledialog.askstring("New user", "Enter the name of the new user:")
            if new_user_name != None and new_user_name!="":
                users.append([new_user_name, 0])
                balances.append(tk.DoubleVar(root, value=0))
                user_menu["menu"].add_command(label=new_user_name, command=tk._setit(selected_user, new_user_name))
                pay_user_menu["menu"].add_command(label=new_user_name, command=tk._setit(selected_pay_user, new_user_name))

    # Declares the amount the delete user has from his balance
    amount = balances[user_index].get()

    # Calculate the amount to be paid to each user
    num_users = len(users)
    amount_per_user = (amount / (num_users - 1 ))
        
    # Update the balances for all users except the current user
    for i in range(num_users):
        if i != user_index:
            balances[i].set(balances[i].get() + amount_per_user)
            # uptade the balance
            users[i][1]=balances[i].get()

    
    # Delete the user from the list of users
    del users[user_index]
    
    # Delete the variable associated with the user's balance
    del balances[user_index]
    
    # Update the OptionMenu widget to remove the deleted user
    user_menu["menu"].delete(user_index)
    pay_user_menu["menu"].delete(user_index)

    # Update the selected user
    selected_user.set(users[0][0])

    # Uptade balance
    uptade_balance()
    
    # Save the user
    save_to_json()

# Create a button to add a new user
add_user_button = tk.Button(root, text="Add user", command=add_user)
add_user_button.pack()

# Create a button to delete a user
delete_user_button = tk.Button(root, text="Delete user", command=lambda: delete_user(selected_user.get()))
delete_user_button.pack()

# Create a label to display the result of the operation
result_label = tk.Label(root)
result_label.pack()

# Function to save to json
def save_to_json():
    with open("users.json", "w") as f:
        json.dump(users, f)
        

# Create a label to prompt the user to enter a value
pay_label = tk.Label(root, text="Enter the amount to be paid:")
pay_label.pack()

# Create an entry widget for the user to input a value
pay_entry = tk.Entry(root)
pay_entry.pack()

# create a function to handle button pay
def on_pay():
    # Get the amount to be paid from the user
    amount = pay_entry.get()
    
    try:
        # Convert the amount to an integer
        amount = float(amount)
        if amount < 0:
            raise 
        
        # Find the index of the current user in the list of users
        current_user_index = [name for name, _ in users].index(selected_user.get())
        
        # Calculate the amount to be paid to each user
        num_users = len(users)
        amount_per_user = -(amount / (num_users ))
        
        # Update the balances for all users except the current user
        for i in range(num_users):
            if i != current_user_index:
                balances[i].set(balances[i].get() + amount_per_user)
                # uptade the balance

                users[i][1]=balances[i].get()

        # Update the balance for the current user
        balances[current_user_index].set(balances[current_user_index].get() + amount + amount_per_user)
        # Uptade the balance
        users[current_user_index][1]=balances[current_user_index].get()
        # Display the updated balances of all users
        uptade_balance()
        
        # Display a message to the user indicating the amount was paid to all users
        message = f"Amount {amount} paid to all users except {selected_user.get()}"
        save_to_json()
    except:
        # If the user entered a non-integer value, display an error message
        message = "Invalid input. Please enter a positive value."

    
    # Replace the current result label with a new label containing the updated message
    global result_label
    result_label.destroy()
    result_label = tk.Label(root, text=message)
    result_label.pack()

# create a button to trigger the on_pay function
pay_button = tk.Button(root, text="Pay", command=on_pay)
pay_button.pack()

# Create a label to prompt the user to enter a value
pay_label_to_user = tk.Label(root, text="Enter the amount to be paid the other user:")
pay_label_to_user.pack()

# Create an entry widget for the user to input a value
pay_entry_to_user = tk.Entry(root)
pay_entry_to_user.pack()

# Create a label to prompt the user to enter a value
select_user_to_pay = tk.Label(root, text="Select the user to be paid:")
select_user_to_pay.pack()

# Create an OptionMenu widget to select a user to be paid

selected_pay_user = tk.StringVar(root)
pay_user_menu = tk.OptionMenu(root, selected_pay_user, *tuple(name for name, _ in users))
pay_user_menu.pack()

# create a function to handle button pay to user

def pay_to_user():
    # Get the amount to be paid from the user
    amount = pay_entry_to_user.get()
    
    try:
        # Convert the amount to an integer
        amount = float(amount)
        
        # Find the index of the current user in the list of users
        current_user_index = [name for name, _ in users].index(selected_user.get())
        
        # Find the index of the selected user in the list of users
        selected_user_index = [name for name, _ in users].index(selected_pay_user.get())
        
        # Update the balances for the current user and the selected user
        balances[current_user_index].set(balances[current_user_index].get() + amount)
        balances[selected_user_index].set(balances[selected_user_index].get() - amount)

        # Uptade the balance in users
        users[current_user_index][1]=balances[current_user_index].get()
        users[selected_user_index][1]=balances[selected_user_index].get()
        
        # Display the updated balances of all users
        uptade_balance()

        #save the uptaded balance
        save_to_json()

        message = f"Amount {amount} paid to user {selected_user.get()} from user {selected_pay_user.get()}"
    except ValueError:
        # If the user entered a non-integer value, display an error message
        message = "Invalid input. Please enter an valid value."
    # Replace the current result label with a new label containing the updated message
    global result_label
    result_label.destroy()
    result_label = tk.Label(root, text=message)
    result_label.pack()
# Create a button to trigger the pay_to_user function

pay_to_user_button = tk.Button(root, text="Pay to user", command=pay_to_user)
pay_to_user_button.pack()

#function that inputs an even value in pay_entry_to_user
def update_entry_value():
    # Find the index of the current user in the list of users
    current_user_index = [name for name, _ in users].index(selected_user.get())
        
    # Find the index of the selected user in the list of users
    selected_user_index = [name for name, _ in users].index(selected_pay_user.get())
    
    current_user_balance = balances[current_user_index].get()
    selected_user_balance = balances[selected_user_index].get()
    
    if current_user_balance<0 and selected_user_balance>0:
        comparativeValue=-current_user_balance
        if comparativeValue>selected_user_balance:
            difference = selected_user_balance
        else:
            difference = comparativeValue
    else:
        difference = 0

    pay_entry_to_user.delete(0, tk.END)  # Clear the current value in the widget
    pay_entry_to_user.insert(0, str(difference))  # Insert the new value into the widget

# Create a button that will even
even_button = tk.Button(root, text="Even", command=update_entry_value)
even_button.pack()


# Center all the widgets
for widget in root.winfo_children():
    widget.pack_configure(pady=10)
root.update_idletasks()
root.geometry(f"+{int((root.winfo_screenwidth() - root.winfo_width())/2)}+{int((root.winfo_screenheight() - root.winfo_height())/2)}")

root.mainloop()
