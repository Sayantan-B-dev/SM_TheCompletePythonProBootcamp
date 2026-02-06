import tkinter as tk
import datetime as dt
from age_logic import calculate_detailed_age
from validators import parse_dob
from storage import load_dobs, save_dob


class AgeCounterUI:
    def __init__(self, root):
        self.root = root
        self.dob = None
        self.last_second = None

        tk.Label(root, text="DOB (YYYY-MM-DD HH:MM:SS)").pack(pady=5)

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        # -----------------------------
        # DROPDOWN (SAFE INIT)
        # -----------------------------
        self.saved_dobs = load_dobs()
        self.dropdown_var = tk.StringVar()

        if self.saved_dobs:
            default_value = self.saved_dobs[0]
            self.dropdown_var.set(default_value)
        else:
            default_value = "No saved DOBs"
            self.dropdown_var.set(default_value)

        self.dropdown = tk.OptionMenu(
            root,
            self.dropdown_var,
            default_value,
            *self.saved_dobs,
            command=self.select_saved_dob
        )
        self.dropdown.pack(pady=5)

        # -----------------------------
        # START BUTTON
        # -----------------------------
        self.start_btn = tk.Button(
            root,
            text="Start Count",
            command=self.start_counter
        )
        self.start_btn.pack(pady=10)

        # -----------------------------
        # DISPLAY
        # -----------------------------
        self.label = tk.Label(
            root,
            text="",
            font=("Consolas", 18),
            fg="black",
            justify="center"
        )
        self.label.pack(pady=15)

        self.error = tk.Label(root, fg="red")
        self.error.pack()

    # -----------------------------
    # DROPDOWN SELECTION
    # -----------------------------
    def select_saved_dob(self, value):
        if value == "No saved DOBs":
            return
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

    # -----------------------------
    # START COUNTER
    # -----------------------------
    def start_counter(self):
        try:
            dob_text = self.entry.get()
            self.dob = parse_dob(dob_text)

            if self.dob > dt.datetime.now():
                raise ValueError("DOB cannot be in the future")

            save_dob(dob_text)
            self.refresh_dropdown()

            self.error.config(text="")
            self.update_ui()

        except Exception as e:
            self.error.config(text=str(e))

    # -----------------------------
    # FLASH EFFECT
    # -----------------------------
    def flash_red(self):
        self.label.config(fg="red")
        self.root.after(150, lambda: self.label.config(fg="black"))

    # -----------------------------
    # UPDATE AGE
    # -----------------------------
    def update_ui(self):
        if not self.dob:
            return

        now = dt.datetime.now()
        age = calculate_detailed_age(now, self.dob)

        text = (
            "LIVE AGE COUNTER\n"
            "----------------------\n"
            f"{age['years']} years\n"
            f"{age['months']} months\n"
            f"{age['days']} days\n"
            f"{age['hours']} hours\n"
            f"{age['minutes']} minutes\n"
            f"{age['seconds']} seconds"
        )

        self.label.config(text=text)

        if self.last_second != age["seconds"]:
            self.flash_red()
            self.last_second = age["seconds"]

        self.root.after(1000, self.update_ui)

    # -----------------------------
    # REFRESH DROPDOWN AFTER SAVE
    # -----------------------------
    def refresh_dropdown(self):
        self.saved_dobs = load_dobs()

        menu = self.dropdown["menu"]
        menu.delete(0, "end")

        for dob in self.saved_dobs:
            menu.add_command(
                label=dob,
                command=lambda v=dob: self.dropdown_var.set(v)
            )

        if self.saved_dobs:
            self.dropdown_var.set(self.saved_dobs[-1])
