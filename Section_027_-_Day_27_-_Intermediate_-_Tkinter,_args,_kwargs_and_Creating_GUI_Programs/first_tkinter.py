import tkinter as tk

# =============== Window ==================
window = tk.Tk()
window.title("My First GUI")
window.minsize(width=500, height=800)
window.config(padx=20, pady=20)
# =============== Top Label ==================
label = tk.Label(text="Hello World", font=("Arial", 24, "bold"))
label.pack(pady=20)

# =============== Button (Counter) ==================
i = 0

def button_clicked():
    global i
    i += 1
    label.config(text=f"Button Got Clicked {i} times")

button_counter = tk.Button(text="I AM A BUTTON", command=button_clicked)
button_counter.pack(pady=10)

# =============== Input Section ==================
def get_input():
    label2.config(text=f"You entered: {entry.get()}")

entry = tk.Entry(width=20)
entry.pack(pady=5)

submit_button = tk.Button(text="Submit", command=get_input)
submit_button.pack(pady=5)

label2 = tk.Label(text="", font=("Arial", 16))
label2.pack(pady=10)

# =============== Practicing place ===============
x_cor = 20
y_cor = 224
label3 = tk.Label(text=f"I am at the ({x_cor}, {y_cor}) coordinate", font=("Arial", 16))
label3.place(x=x_cor, y=y_cor)

# =============== Practicing Grid ===============

grid_frame = tk.Frame(window)
grid_frame.pack(pady=30)

grid_style = {
    "font": ("Arial", 16),
    "borderwidth": 2,
    "relief": "solid",
    "padx": 10,
    "pady": 5
}

def grid_cell_style(row, column):
    return {"row":row, "column":column, "sticky":"ew", "padx":10, "pady":10}

tk.Label(grid_frame, text="TopLeft", **grid_style).grid(**grid_cell_style(0, 0))
tk.Label(grid_frame, text="TopRight", **grid_style).grid(**grid_cell_style(0, 1))
tk.Label(grid_frame, text="BottomLeft", **grid_style).grid(**grid_cell_style(1, 0))
tk.Label(grid_frame, text="BottomRight", **grid_style).grid(**grid_cell_style(1, 1))


# =============== Main Loop ==================
window.mainloop()
