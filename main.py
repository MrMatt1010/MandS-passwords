from tkinter import *
from tkinter import messagebox, simpledialog
from random import choice, randint, shuffle
import pyperclip
import os

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

    # Evaluate password strength and provide feedback
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
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                      f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            with open("data.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)

            # Show a popup confirming successful save
            messagebox.showinfo(title="Success", message="Password saved successfully!")

# ---------------------------- VIEW SAVED PASSWORDS ------------------------------- #
def view_passwords():
    """Reads and displays the saved passwords from the data.txt file."""
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as data_file:
            content = data_file.read()

        if content:
            # Show saved passwords in a messagebox
            messagebox.showinfo(title="Saved Passwords", message=content)
        else:
            messagebox.showinfo(title="No Data", message="No passwords saved yet.")
    else:
        messagebox.showinfo(title="No Data", message="No passwords saved yet.")

# ---------------------------- DELETE PASSWORD ------------------------------- #
def delete_password():
    """Allows user to delete a specific password from the saved passwords."""
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as data_file:
            lines = data_file.readlines()

        if lines:
            # Ask the user which website's password they want to delete
            website_to_delete = simpledialog.askstring("Delete Password", "Enter the website name to delete:")

            if website_to_delete:
                # Check if the website exists in the file
                new_lines = [line for line in lines if not line.startswith(website_to_delete)]

                if len(new_lines) == len(lines):
                    messagebox.showinfo(title="Not Found", message=f"No entry found for '{website_to_delete}'")
                else:
                    # Overwrite the file without the deleted password
                    with open("data.txt", "w") as data_file:
                        data_file.writelines(new_lines)

                    messagebox.showinfo(title="Success", message=f"Password for '{website_to_delete}' deleted successfully!")
            else:
                messagebox.showinfo(title="Error", message="Please enter a valid website name.")
        else:
            messagebox.showinfo(title="No Data", message="No passwords saved yet.")
    else:
        messagebox.showinfo(title="No Data", message="No passwords saved yet.")

# ---------------------------- TOGGLE PASSWORD VISIBILITY ------------------------------- #
def toggle_password_visibility():
    """Toggles the password between hidden and visible states."""
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


# ---------------------------- STRENGTH EVALUATION ------------------------------- #
def evaluate_password_strength(password):
    """Evaluates password strength based on length, character variety, and complexity."""

    if len(password) < 8:
        return "Weak"

    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special_char = any(not c.isalnum() for c in password)

    if not (has_uppercase or has_lowercase or has_digit or has_special_char):
        return "Weak"

    if all([has_uppercase, has_lowercase, has_digit, has_special_char]):
        return "Strong"

    return "Medium"

def evaluate_and_update_strength():
    """Evaluates the password strength and updates the strength label."""
    password = password_entry.get()
    strength = evaluate_password_strength(password)
    strength_label.config(text=f"Password Strength: {strength}")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("M and S Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=217, width=217)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

strength_label = Label(text="Password Strength:")
strength_label.grid(row=4, column=0)

#Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "")
password_entry = Entry(width=21, show="*")
password_entry.grid(row=3, column=1)

# Bind the function to the password entry's '<KeyRelease>' event
password_entry.bind('<KeyRelease>', lambda event: evaluate_and_update_strength())

# Checkbox to show/hide password
show_password_var = BooleanVar()
show_password_checkbox = Checkbutton(text="Show Password", variable=show_password_var, command=toggle_password_visibility)
show_password_checkbox.grid(row=3, column=2)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2,)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

# View passwords button
view_passwords_button = Button(text="View Saved Passwords", width=36, command=view_passwords)
view_passwords_button.grid(row=5, column=1, columnspan=2)

# Delete password button
delete_password_button = Button(text="Delete Password", width=36, command=delete_password)
delete_password_button.grid(row=6, column=1, columnspan=2)

# Exit button
exit_button = Button(text="Exit", width=36, command=window.quit)
exit_button.grid(row=7, column=1, columnspan=2)

window.mainloop()

