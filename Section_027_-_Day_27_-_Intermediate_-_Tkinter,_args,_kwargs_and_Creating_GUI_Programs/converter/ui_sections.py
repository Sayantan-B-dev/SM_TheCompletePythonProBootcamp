# ui_sections.py
import tkinter as tk
from styles import *
from utils import safe_float
import converters


def make_converter_frame(
    parent,
    title: str,
    left_unit: str,
    right_unit: str,
    convert_func
):
    frame = tk.Frame(parent, bg=BG_FRAME, padx=15, pady=15)

    tk.Label(
        frame, text=title,
        font=LABEL_FONT, fg=FG_MAIN, bg=BG_FRAME
    ).grid(row=0, column=0, columnspan=3, pady=(0, 10))

    entry = tk.Entry(frame, width=10, font=ENTRY_FONT)
    entry.grid(row=1, column=0)

    tk.Label(
        frame, text="→",
        font=LABEL_FONT, fg=FG_MAIN, bg=BG_FRAME
    ).grid(row=1, column=1)

    result = tk.Label(
        frame, text=f"0.00 {right_unit}",
        font=LABEL_FONT, fg=OK_FG, bg=BG_FRAME
    )
    result.grid(row=1, column=2)

    def convert():
        try:
            value = safe_float(entry.get())
            output = convert_func(value)
            result.config(text=f"{output:.2f} {right_unit}", fg=OK_FG)
        except ValueError:
            result.config(text="Invalid input", fg=ERR_FG)

    tk.Button(
        frame, text="Convert",
        font=BTN_FONT, bg=BTN_BG, fg=BTN_FG,
        command=convert
    ).grid(row=2, column=0, columnspan=3, pady=8)

    return frame
