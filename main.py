from tkinter import *
from tkinter import messagebox, simpledialog
from random import choice, randint, shuffle
import pyperclip
import os

# Fixed username and password
USERNAME = "test"
PASSWORD = "test"

# File to save username and password
LOGIN_FILE = "up.txt"


# ---------------------------- LOGIN FUNCTION ------------------------------- #
def login():
    # Check if the login file exists; if not, create it with default credentials
    if not os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE, "w") as file:
            file.write(f"{USERNAME}\n{PASSWORD}")

    # Set up the login window
    login_window = Toplevel()
    login_window.title("Login")
    login_window.geometry("300x200")

    # Username entry
    Label(login_window, text="Enter Username:").pack(pady=5)
    entered_username = Entry(login_window, width=50)
    entered_username.pack(pady=5)

    # Password entry
    Label(login_window, text="Enter Password:").pack(pady=5)
    entered_password = Entry(login_window, width=50, show="*")
    entered_password.pack(pady=5)

    def submit_login():
        if entered_username.get() == USERNAME and entered_password.get() == PASSWORD:
            messagebox.showinfo("Login Success", "Welcome to the Password Manager!")
            login_window.destroy()  # Close login window
            window.deiconify()      # Show the main window
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            login_window.quit()

    # Login button
    login_button = Button(login_window, text="Login", command=submit_login)
    login_button.pack(pady=10)

    login_window.mainloop()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = [chr(i) for i in range(97, 123)] + [chr(i).upper() for i in range(97, 123)]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

    strength = evaluate_password_strength(password)
    strength_label.config(text=f"Password Strength: {strength}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Details entered: \nEmail: {email} \nPassword: {password} \nSave?")
        if is_ok:
            with open("data.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)
            messagebox.showinfo(title="Success", message="Password saved successfully!")


# ---------------------------- VIEW SAVED PASSWORDS ------------------------------- #
def view_passwords():
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as data_file:
            content = data_file.read()
        messagebox.showinfo(title="Saved Passwords", message=content if content else "No passwords saved yet.")
    else:
        messagebox.showinfo(title="No Data", message="No passwords saved yet.")


# ---------------------------- DELETE PASSWORD ------------------------------- #

def delete_password():
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as data_file:
            lines = data_file.readlines()

        if lines:
            website_to_delete = simpledialog.askstring("Delete Password", "Enter the website name to delete:")

            if website_to_delete:
                new_lines = [line for line in lines if not line.startswith(website_to_delete)]

                if len(new_lines) == len(lines):
                    messagebox.showinfo(title="Not Found", message=f"No entry found for '{website_to_delete}'")
                else:
                    with open("data.txt", "w") as data_file:
                        data_file.writelines(new_lines)

                    messagebox.showinfo(title="Success", message=f"Password for '{website_to_delete}' deleted successfully!")
            else:
                messagebox.showinfo(title="Error", message="Please enter a valid website name.")
        else:
            messagebox.showinfo(title="No Data", message="No passwords saved yet.")
    else:
        messagebox.showinfo(title="No Data", message="No passwords saved yet.")


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as data_file:
            lines = data_file.readlines()

        if lines:
            website_to_search = simpledialog.askstring("Search Password", "Enter the website name to search:")

            if website_to_search:
                for line in lines:
                    if line.startswith(website_to_search):
                        messagebox.showinfo(title="Password Found", message=line)
                        return

                messagebox.showinfo(title="Not Found", message=f"No password found for '{website_to_search}'")
            else:
                messagebox.showinfo(title="Error", message="Please enter a valid website name.")
        else:
            messagebox.showinfo(title="No Data", message="No passwords saved yet.")
    else:
        messagebox.showinfo(title="No Data", message="No passwords saved yet.")


# ---------------------------- TOGGLE PASSWORD VISIBILITY ------------------------------- #
def toggle_password_visibility():
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


# ---------------------------- STRENGTH EVALUATION ------------------------------- #
def evaluate_password_strength(password):
    if len(password) < 8:
        return "Weak"

    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special_char = any(not c.isalnum() for c in password)

    if all([has_uppercase, has_lowercase, has_digit, has_special_char]):
        return "Strong"
    return "Medium" if has_uppercase or has_lowercase or has_digit or has_special_char else "Weak"


def evaluate_and_update_strength():
    password = password_entry.get()
    strength = evaluate_password_strength(password)
    strength_label.config(text=f"Password Strength: {strength}")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Hide the main window until login is successful
window.withdraw()

# Login before showing the main application
window.after(0, login)

canvas = Canvas(height=217, width=217)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, columnspan=3)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

strength_label = Label(text="Password Strength:")
strength_label.grid(row=4, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=25, show="*")
password_entry.grid(row=3, column=2)
password_entry.bind('<KeyRelease>', lambda event: evaluate_and_update_strength())

# Checkbox to show/hide password
show_password_var = BooleanVar()
show_password_checkbox = Checkbutton(text="Show Password", variable=show_password_var, command=toggle_password_visibility)
show_password_checkbox.grid(row=4, column=1)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=4, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=5, column=1, columnspan=2)
view_passwords_button = Button(text="View Saved Passwords", width=36, command=view_passwords)
view_passwords_button.grid(row=6, column=1, columnspan=2)
delete_password_button = Button(text="Delete Password", width=36, command=delete_password)
delete_password_button.grid(row=7, column=1, columnspan=2)
search_password_button = Button(text="Search Password", width=36, command=search_password)
search_password_button.grid(row=8, column=1, columnspan=2)
exit_button = Button(text="Exit", width=36, command=window.quit)
exit_button.grid(row=9, column=1, columnspan=2)

window.mainloop()

