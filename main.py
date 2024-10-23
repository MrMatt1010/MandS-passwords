from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = list('0123456789')
    symbols = list('!#$%&()*+')

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)  # Clear existing password
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
            try:
                with open("data.txt", "a") as data_file:
                    data_file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showinfo(title="Success", message="Password saved successfully!")
            except Exception as e:
                messagebox.showerror(title="Error", message=f"An error occurred while saving the password: {e}")

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
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
try:
    logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)
except TclError:
    # If logo.png is not found, skip displaying the image
    pass
canvas.grid(row=0, column=1)

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
email_entry.insert(0, "")  # You can set a default email here if desired
password_entry = Entry(width=21, show="*")
password_entry.grid(row=3, column=1)

# Bind the function to the password entry's '<KeyRelease>' event
password_entry.bind('<KeyRelease>', lambda event: evaluate_and_update_strength())

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

# Exit button
exit_button = Button(text="Exit", width=36, command=window.quit)
exit_button.grid(row=5, column=1, columnspan=2)

window.mainloop()
