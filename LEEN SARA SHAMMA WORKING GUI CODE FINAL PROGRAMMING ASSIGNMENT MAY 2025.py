# we are first going to import the necessary libraries so that we are able to create the GUI, for example, we use the messagebox, pickle, enum, and datetime
import pickle
import tkinter as tk
from tkinter import messagebox, ttk
from enum import Enum
import datetime


# defining our classes for the enums (for any types and status) that represent options for each of our appropriate classes
class TicketType(Enum):
    SINGLERACE = "Single-Race"
    WEEKENDPACKAGE = "Weekend Package"
    SEASONMEMBERSHIP = "Season Membership"
    GROUPDISCOUNT = "Group Discount"


class PaymentMethod(Enum):
    CARDDEBITCARD = "Credit or debit card"
    DIGITALWALLET = "Digital wallet"


class OrderStatus(Enum):
    ORDERCONFIRMED = "Your ticket has been booked!"
    ORDERCANCELLED = "Your ticket has been cancelled."


# defining the user class to keep track of name, email, password etc.
class User:
    def __init__(self, user_id, full_name, email, password):
        self.__user_id = user_id
        self.__name = full_name
        self.__email = email
        self.__password = password

    # defining the get methods for each of the appropriate attributes for the User class
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    # defining the set methods for each of the appropriate attributes for the User class
    def set_name(self, full_name):
        self.__name = full_name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password


# defining a class named "TicketOrder" that represents the orders in the system
class TicketOrder:
    def __init__(self, order_id, user_id, ticket_choice, total_paid, status, order_date, quantity):
        self.__order_id = order_id
        self.__user_id = user_id
        self.__type_of_ticket = ticket_choice
        self.__total_price = total_paid
        self.__status = status
        self.__purchase_date = order_date
        self.__number_of_tickets = quantity

    def get_total_price(self):
        return self.__total_price

    def get_type_of_ticket(self):
        return self.__type_of_ticket

    def get_number_of_tickets(self):
        return self.__number_of_tickets

    def get_purchase_date(self):
        return self.__purchase_date


# creating binary files to keep users and orders stored by using the '.pkl'

users_file = 'users.pkl'

orders_file = 'orders.pkl'


# we will now be saving the item(s) to the file and we will be creating the file if it already does not exist using the 'with open' function as a 'read binary' file
# this means we can read the data as binary
# we do the same when we want to update the file using the 'with open' function as a 'write binary'


def save_to_file(item, filename):
    try:
        with open(filename, 'rb') as file:
            existing_data = pickle.load(file)
    except:
        existing_data = []
    existing_data.append(item)
    with open(filename, 'wb') as file:
        pickle.dump(existing_data, file)


# also we will do the same for loading data from the files specifically here they will be 'read binary'
def load_from_file(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except:
        return []


# now we will set up the window and title for the window screen with specific dimensions
root = tk.Tk()
root.title("Ticketing System")
root.geometry("600x400")


# next we will define the show_main_menu that shows the first screen (which is the main menu with options using Button that the user can see and click)
def show_main_menu():
    clear_window()
    tk.Label(root, text="Welcome to the Ticket Booking App", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Login", command=login_screen).pack(pady=5)
    tk.Button(root, text="Create Account", command=create_account_screen).pack(pady=5)
    tk.Button(root, text="Admin Dashboard", command=admin_dashboard).pack(pady=5)


# we create a function that when we change the screens it removes the existing widgets from the screen/window (such as when the user clicks a button and gets directed to another screen)
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# we create a function for the screen for creating a new user account
def create_account_screen():
    clear_window()
    tk.Label(root, text="Create Your Account").pack()
    name_box = tk.Entry(root)
    email_box = tk.Entry(root)
    pass_box = tk.Entry(root, show="*")
    for label_text, entry_box in zip(["Name", "Email", "Password"], [name_box, email_box, pass_box]):
        tk.Label(root, text=label_text).pack()
        entry_box.pack()

    def submit():
        new_id = len(load_from_file(users_file)) + 1
        new_user = User(new_id, name_box.get(), email_box.get(), pass_box.get())
        save_to_file(new_user, users_file)
        messagebox.showinfo("Success", "Your account was created!")
        show_main_menu()

    tk.Button(root, text="Submit", command=submit).pack(pady=5)


# we create a function to show the login screen which includes the form for logging in such as name, email, password, etc

def login_screen():
    clear_window()
    tk.Label(root, text="Login to Continue").pack()
    email_input = tk.Entry(root)
    password_input = tk.Entry(root, show="*")
    for label_text, entry_box in zip(["Email", "Password"], [email_input, password_input]):
        tk.Label(root, text=label_text).pack()
        entry_box.pack()

    def check():
        all_users = load_from_file(users_file)
        for existing_user in all_users:
            if existing_user.get_email() == email_input.get() and existing_user.get_password() == password_input.get():
                show_user_dashboard(existing_user)
                return
        messagebox.showerror("Error", "Incorrect login details. Try again.")

    tk.Button(root, text="Login", command=check).pack(pady=5)


# we create a function after logging into the account and show the ticket options and prices and the user can buy tickets with the specific quantity they want
# for example we have the single race ticket that costs 20 AED and they can select this through the dropdown
# also inside this function we create another function for the purchasing process and it determines the price based on the ticket type and it creates and save the new order that has been made

def ticket_purchase_interface(current_user):
    clear_window()
    tk.Label(root, text="Choose Ticket Type").pack()
    ticket_options = {
        TicketType.SINGLERACE.value: "20 AED (1 day access)",
        TicketType.WEEKENDPACKAGE.value: "50 AED (3 days access)",
        TicketType.SEASONMEMBERSHIP.value: "200 AED (full season access)",
        TicketType.GROUPDISCOUNT.value: "15 AED per person (min 5 people)"
    }
    tk.Label(root, text="Select from these:").pack()
    ticket_choice = ttk.Combobox(root, values=[f"{key} - {value}" for key, value in ticket_options.items()])
    ticket_choice.pack()

    tk.Label(root, text="Number of Tickets").pack()
    quantity_box = tk.Entry(root)
    quantity_box.pack()

    tk.Label(root, text="Payment Method").pack()
    pay_choice = ttk.Combobox(root, values=[option.value for option in PaymentMethod])
    pay_choice.pack()

    def purchase():
        try:
            ticket_count = int(quantity_box.get())
            selected_ticket = ticket_choice.get().split(" - ")[0]
            price = 20 if "Single" in selected_ticket else 50 if "Weekend" in selected_ticket else 200 if "Season" in selected_ticket else 15
            total_amount = ticket_count * price
            new_order = TicketOrder(order_id=len(load_from_file(orders_file)) + 1,
                                    user_id=current_user.get_user_id(),
                                    ticket_choice=selected_ticket,
                                    total_paid=total_amount,
                                    status=OrderStatus.ORDERCONFIRMED,
                                    order_date=str(datetime.date.today()),
                                    quantity=ticket_count)
            save_to_file(new_order, orders_file)
            messagebox.showinfo("Success", f"You paid {total_amount} AED")
            show_user_dashboard(current_user)
        except:
            messagebox.showerror("Error", "Something was wrong. Please check your inputs.")

    tk.Button(root, text="Confirm Purchase", command=purchase).pack(pady=5)
    tk.Button(root, text="Back", command=lambda: show_user_dashboard(current_user)).pack()


# we create a function for the admin dashboard to view all of the ticket sales/orders that have been made in the system

def admin_dashboard():
    clear_window()
    tk.Label(root, text="Admin Dashboard", font=("Arial", 14)).pack(pady=10)

    def apply_discount():
        clear_window()
        tk.Label(root, text="Modify Discounts", font=("Arial", 14)).pack(pady=10)
        ticket_pick = ttk.Combobox(root, values=[ticket.value for ticket in TicketType])
        ticket_pick.pack()
        tk.Label(root, text="New Price (AED)").pack()
        new_price = tk.Entry(root)
        new_price.pack()
        tk.Button(root, text="Save Discount", command=lambda: save_discount(ticket_pick.get(), new_price.get())).pack(
            pady=5)
        tk.Button(root, text="Back", command=admin_dashboard).pack(pady=5)

    all_orders = load_from_file(orders_file)
    ticket_sales_by_date = {}
    for order_instance in all_orders:
        order_day = order_instance.get_purchase_date()
        ticket_sales_by_date[order_day] = ticket_sales_by_date.get(order_day,
                                                                   0) + order_instance.get_number_of_tickets()

    for sale_date, total in ticket_sales_by_date.items():
        tk.Label(root, text=f"{sale_date}: {total} tickets sold").pack()

    tk.Button(root, text="Modify Discounts", command=apply_discount).pack(pady=5)
    tk.Button(root, text="Back", command=show_main_menu).pack(pady=5)


# we create a function that allows the admin to change the price(s) of the different tickets one at a time based on the instructions which will display that the discounts have been updated/modifying availability

def save_discount(ticket_name, price_input):
    try:
        new_price = float(price_input)
        if ticket_name == TicketType.SINGLERACE.value:
            label = "20 AED (1 day access)"
            new_text = f"{ticket_name} - {new_price:.0f} AED (1 day access)"
        elif ticket_name == TicketType.WEEKENDPACKAGE.value:
            label = "50 AED (3 days access)"
            new_text = f"{ticket_name} - {new_price:.0f} AED (3 days access)"
        elif ticket_name == TicketType.SEASONMEMBERSHIP.value:
            label = "200 AED (full season access)"
            new_text = f"{ticket_name} - {new_price:.0f} AED (full season access)"
        elif ticket_name == TicketType.GROUPDISCOUNT.value:
            label = "15 AED per person (min 5 people)"
            new_text = f"{ticket_name} - {new_price:.0f} AED per person (min 5 people)"
        else:
            raise ValueError("Unknown ticket type")

        messagebox.showinfo("Updated", f"Price for {ticket_name} updated to {new_price:.0f} AED")
        admin_dashboard()
    except:
        messagebox.showerror("Error", "Please type a valid number")


# we create a function so that this is what the user sees after they logged in which includes the labels and the buttons

def show_user_dashboard(current_user):
    clear_window()
    tk.Label(root, text=f"Welcome, {current_user.get_name()}!", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Buy Ticket", command=lambda: ticket_purchase_interface(current_user)).pack(pady=5)
    tk.Button(root, text="View My Orders", command=lambda: view_my_orders(current_user)).pack(pady=5)
    tk.Button(root, text="Edit Account", command=lambda: edit_account(current_user)).pack(pady=5)
    tk.Button(root, text="Back to Main Menu", command=show_main_menu).pack(pady=10)


# we create a function for the user to be able to view their orders and the user

def view_my_orders(current_user):
    clear_window()
    tk.Label(root, text="My Orders", font=("Arial", 14)).pack(pady=10)
    orders = load_from_file(orders_file)
    user_related_orders = [order for order in orders if order._TicketOrder__user_id == current_user.get_user_id()]
    for each_order in user_related_orders:
        order_row = tk.Frame(root)
        order_row.pack(pady=2)
        tk.Label(order_row,
                 text=f"{each_order.get_type_of_ticket()} | {each_order.get_total_price()} AED on {each_order.get_purchase_date()}").pack(
            side=tk.LEFT)
        tk.Button(order_row, text="Delete",
                  command=lambda order_to_delete=each_order: delete_order(order_to_delete, current_user)).pack(
            side=tk.RIGHT)
    tk.Button(root, text="Back", command=lambda: show_user_dashboard(current_user)).pack(pady=5)


# we create a function here to specifically delete an order

def delete_order(order_to_remove, current_user):
    orders = load_from_file(orders_file)
    orders = [order for order in orders if order._TicketOrder__order_id != order_to_remove._TicketOrder__order_id]
    with open(orders_file, 'wb') as file:
        pickle.dump(orders, file)
    messagebox.showinfo("Deleted", "Your ticket order has been removed.")
    view_my_orders(current_user)


# we create a function to update account details for the user which includes the name, email, and password

def edit_account(current_user):
    clear_window()
    tk.Label(root, text="Edit Your Info", font=("Arial", 14)).pack(pady=10)
    name_box = tk.Entry(root)
    name_box.insert(0, current_user.get_name())
    email_box = tk.Entry(root)
    email_box.insert(0, current_user.get_email())
    pass_box = tk.Entry(root, show="*")
    pass_box.insert(0, current_user.get_password())
    for label_text, entry_box in zip(["Name", "Email", "Password"], [name_box, email_box, pass_box]):
        tk.Label(root, text=label_text).pack()
        entry_box.pack()

    def update():
        current_user.set_name(name_box.get())
        current_user.set_email(email_box.get())
        current_user.set_password(pass_box.get())
        all_users = load_from_file(users_file)
        for index, existing_user in enumerate(all_users):
            if existing_user.get_user_id() == current_user.get_user_id():
                all_users[index] = current_user
                break
        with open(users_file, 'wb') as file:
            pickle.dump(all_users, file)
        messagebox.showinfo("Updated", "Your account info is now saved.")
        show_user_dashboard(current_user)

    tk.Button(root, text="Save Changes", command=update).pack(pady=5)
    tk.Button(root, text="Back", command=lambda: show_user_dashboard(current_user)).pack(pady=5)


# we will now have the window loop forever until the user exits or clicks 'x'
# basically we will start the GUI window and it will be waiting for the user to "trigger" an event such as by clicking one of the buttons they see on the window
show_main_menu()
root.mainloop()