# dialogs.py

import tkinter as tk

def custom_popup(parent, title, message):
    """
    Displays a modal confirmation dialog.

    Why custom instead of messagebox:
    - Full layout control
    - Multi-line previews
    - Custom styling
    - Predictable return value

    Returns:
        True  → OK clicked
        False → Cancel / close
    """

    # Mutable container to allow modification from nested functions
    result = {"value": False}

    # Create a new dialog window
    popup = tk.Toplevel(parent)

    # Set window properties
    popup.title(title)
    popup.transient(parent)   # Keep above parent
    popup.grab_set()          # Block parent interaction
    popup.resizable(False, False)

    # Message label (supports multi-line text)
    tk.Label(
        popup,
        text=message,
        justify="left",
        padx=20,
        pady=20
    ).pack()

    # Button container
    button_frame = tk.Frame(popup)
    button_frame.pack(pady=10)

    # OK callback
    def on_ok():
        result["value"] = True
        popup.destroy()

    # Cancel callback
    def on_cancel():
        popup.destroy()

    # Buttons
    tk.Button(button_frame, text="OK", width=10, command=on_ok)\
        .pack(side="left", padx=5)
    tk.Button(button_frame, text="Cancel", width=10, command=on_cancel)\
        .pack(side="left", padx=5)

    # ---- CENTER POPUP OVER PARENT ----
    popup.update_idletasks()

    px, py = parent.winfo_x(), parent.winfo_y()
    pw, ph = parent.winfo_width(), parent.winfo_height()
    w, h = popup.winfo_width(), popup.winfo_height()

    popup.geometry(
        f"{w}x{h}+{px + pw//2 - w//2}+{py + ph//2 - h//2}"
    )
    # ---------------------------------

    # Pause execution until popup closes
    parent.wait_window(popup)

    # Return user decision
    return result["value"]
