import requests
import tkinter as tk

FONT_NAME = "Comic Sans MS"
# -----------------------------
# WINDOW SETUP
# -----------------------------
window = tk.Tk()
window.title("Kanye Quotes")
window.geometry("500x500")
window.config(padx=20, pady=20)

# Configure grid to allow centering
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=3)
window.grid_rowconfigure(2, weight=1)

window.grid_columnconfigure(0, weight=1)

# -----------------------------
# TITLE LABEL
# -----------------------------
label = tk.Label(
    window,
    text="Kanye Says : ",
    font=(FONT_NAME, 25, "bold")
)
label.grid(row=0, column=0, pady=10)

# -----------------------------
# CANVAS (QUOTE DISPLAY)
# -----------------------------
canvas = tk.Canvas(
    window,
    width=400,
    height=250,
    highlightthickness=0,
    bg="pink"
)
canvas.grid(row=1, column=0)

quote_text = canvas.create_text(
    200, 125,                # Center of canvas
    text="Click the button to get a quote",
    width=350,
    font=(FONT_NAME, 16, "bold"),
    justify="center"
)

# -----------------------------
# BUTTON
# -----------------------------
def get_quote():
    response = requests.get("https://api.kanye.rest", timeout=5)
    response.raise_for_status()

    data = response.json()
    canvas.itemconfig(quote_text, text=data["quote"])

button = tk.Button(
    window,
    text="Get Quote",
    command=get_quote,
    font=(FONT_NAME, 14)
)
button.grid(row=2, column=0, pady=20)

# -----------------------------
# START LOOP
# -----------------------------
window.mainloop()
