# main.py
import tkinter as tk
from styles import *
from ui_sections import make_converter_frame
import converters

window = tk.Tk()
window.title("Funky Unit Converter")
window.minsize(width=600, height=450)
window.config(bg=BG_MAIN, padx=20, pady=20)

tk.Label(
    window, text="UNIT CONVERTER",
    font=TITLE_FONT, fg="#8be9fd", bg=BG_MAIN
).grid(row=0, column=0, columnspan=2, pady=(0, 20))

# ---- Converters ----
make_converter_frame(
    window,
    "Miles → Kilometers",
    "Miles",
    "Km",
    converters.miles_to_km
).grid(row=1, column=0, padx=10, pady=10)

make_converter_frame(
    window,
    "Kilometers → Miles",
    "Km",
    "Miles",
    converters.km_to_miles
).grid(row=1, column=1, padx=10, pady=10)

make_converter_frame(
    window,
    "Kilograms → Pounds",
    "Kg",
    "Lb",
    converters.kg_to_pound
).grid(row=2, column=0, padx=10, pady=10)

make_converter_frame(
    window,
    "Pounds → Kilograms",
    "Lb",
    "Kg",
    converters.pound_to_kg
).grid(row=2, column=1, padx=10, pady=10)


make_converter_frame(
    window,
    "Celsius → Fahrenheit",
    "°C",
    "°F",
    converters.celsius_to_fahrenheit
).grid(row=3, column=0)

make_converter_frame(
    window,
    "Fahrenheit → Celsius",
    "°F",
    "°C",
    converters.fahrenheit_to_celsius
).grid(row=3, column=1)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()
