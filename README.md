# M and S Passwords


This is a Tkinter-based Password Manager application that allows users to save, view, search, delete, and generate strong passwords. The application includes a login screen, a session timeout feature, and a scrollable view for saved passwords. Passwords can also be copied to the clipboard directly.

## Features

* **Login Authentication** : Users must log in with the username `test` and password `test` to access the password manager.
* **Session Timeout** : The application automatically logs out after five minutes of inactivity.
* **Password Management** :
* Save passwords for different websites.
* View saved passwords with a scrollable interface.
* Copy passwords to the clipboard with a single click.
* Delete specific saved passwords.
* Search for a password by website name.
* **Password Generator** : Generates strong passwords with a mix of letters, numbers, and symbols.
* **Password Strength Indicator** : Evaluates the strength of the generated or entered password in real-time.

## Technologies

* **Python** (Tkinter for GUI)
* **Pyperclip** for clipboard functionality

## Installation

1. **Clone or download the repository** .
2. **Install dependencies** :

* Ensure Python is installed.
* Install `pyperclip` by running:
* pip install pyperclip

1. **Save the Application Files** :

* Place all files (including `logo.png` for the app logo) in the same directory.

## Usage

### Running the Application

1. Run the `password_manager.py` script:
   python password_manager.py
2. On startup, log in using the credentials:
   * Username: `test`
   * Password: `test`
3. After successful login, the main password manager interface will open.

### Main Features

1. **Generate Password** : Click "Generate Password" to create a strong password and automatically display its strength.
2. **Save Password** : Enter the website, email, and password, then click "Add" to save it to `data.txt`.
3. **View Saved Passwords** :

* Click "View Saved Passwords" to open a scrollable window showing all saved entries.
* Each entry has a "Copy Password" button to copy the password directly to the clipboard.

1. **Search Password** : Click "Search Password" to search for a saved password by website name.
2. **Delete Password** : Click "Delete Password" to remove a password entry by website name.
3. **Session Timeout** : The app automatically exits after 5 minutes of inactivity.

### File Structure

* **password_manager.py** : Main application code.
* **data.txt** : Stores saved password entries in a "Website | Email | Password" format.
* **up.txt** : Stores login credentials (for simplicity, fixed as `test:test` in this example).
* **logo.png** : Application logo displayed on the main screen.

### Notes

* **Security Disclaimer** : This application saves credentials in plain text (`data.txt` and `up.txt`) and is intended for educational purposes. For a secure implementation, consider using encrypted storage and hashed passwords.
* **Clipboard Access** : The `pyperclip` library is used to copy passwords to the clipboard. Ensure this library is installed for full functionality.

## License

This project is open-source and can be modified and used as per your requirements.

of course if you could mentioned that my code helped you, that would be great :)
