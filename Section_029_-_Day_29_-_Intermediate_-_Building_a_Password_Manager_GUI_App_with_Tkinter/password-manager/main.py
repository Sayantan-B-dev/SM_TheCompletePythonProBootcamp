# main.py

import tkinter as tk
from ui import build_ui
from utils import center_window

# Create main application window
window = tk.Tk()

# Hide window until fully built
window.withdraw()

# Build UI components
build_ui(window)

# Center window on screen
center_window(window)

# Show window
window.deiconify()

# Start Tkinter event loop
window.mainloop()
