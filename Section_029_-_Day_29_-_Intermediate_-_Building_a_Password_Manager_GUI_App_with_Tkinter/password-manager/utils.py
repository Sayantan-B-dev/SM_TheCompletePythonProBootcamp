# utils.py

def center_window(win):
    """
    Centers a Tkinter window on the screen.

    Why needed:
    - Tkinter does not auto-center windows
    - Improves UX consistency
    """

    # Ensure geometry is calculated
    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Calculate centered position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    win.geometry(f"{width}x{height}+{x}+{y}")
