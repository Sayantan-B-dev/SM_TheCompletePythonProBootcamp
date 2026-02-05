import tkinter as tk
from constants import YELLOW
from ui import build_ui

window = tk.Tk()
window.title("Pomodoro Timer")
window.geometry("1280x720")
window.grid_propagate(False)
window.config(bg=YELLOW)

build_ui(window)

window.mainloop()
