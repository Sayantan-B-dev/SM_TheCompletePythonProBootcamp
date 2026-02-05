# ui.py

import tkinter as tk

from password_generator import generate_strong_password
from dialogs import custom_popup
from storage import save_credentials

def build_ui(window):
    """
    Builds the entire user interface.

    This function:
    - Creates widgets
    - Places them using grid
    - Binds buttons to callbacks
    """

    # Window configuration
    window.title("Password Manager")
    window.config(padx=40, pady=40)

    # Grid weights for responsive layout
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=3)
    window.columnconfigure(2, weight=1)

    # -------- LOGO --------
    canvas = tk.Canvas(window, width=200, height=200, highlightthickness=0)
    logo_img = tk.PhotoImage(file="assets/logo.png")
    canvas.create_image(100, 100, image=logo_img)
    canvas.image = logo_img   # Prevent garbage collection
    canvas.grid(row=0, column=1, pady=(0, 20))
    # ----------------------

    # Labels
    tk.Label(window, text="Website:").grid(row=1, column=0, sticky="w")
    tk.Label(window, text="Username / Email:").grid(row=2, column=0, sticky="w")
    tk.Label(window, text="Password:").grid(row=3, column=0, sticky="w")

    # Entry fields
    website_entry = tk.Entry(window)
    website_entry.grid(row=1, column=1, columnspan=2, sticky="ew")
    website_entry.focus()

    username_entry = tk.Entry(window)
    username_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
    username_entry.insert(0, "example@email.com")

    password_entry = tk.Entry(window)
    password_entry.grid(row=3, column=1, sticky="ew")

    # -------- CALLBACKS --------
    def on_generate():
        """
        Generates password and inserts it into password entry.
        """
        password_entry.delete(0, tk.END)
        password_entry.insert(0, generate_strong_password())

    def on_save():
        """
        Validates input, shows confirmation popup,
        and saves credentials if confirmed.
        """

        website = website_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        # Validation popup
        if not website or not username or not password:
            custom_popup(window, "Error", "Please fill in all fields")
            return

        # Confirmation popup
        confirm = custom_popup(
            window,
            website,
            f"""These are the details entered:

Website : {website}
Email   : {username}
Password: {password}

Is it ok to save?"""
        )

        # Save only if confirmed
        if confirm:
            save_credentials(website, username, password)

            # Clear fields after save
            website_entry.delete(0, tk.END)
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
    # ---------------------------

    # Buttons
    tk.Button(
        window,
        text="Generate Password",
        command=on_generate
    ).grid(row=3, column=2, padx=5, sticky="ew")

    tk.Button(
        window,
        text="Add to Vault",
        command=on_save
    ).grid(row=4, column=0, columnspan=3, pady=5, sticky="ew")
