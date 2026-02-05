import tkinter as tk
from constants import *
from timer_logic import start_timer, reset_timer

def build_ui(window):
    main_frame = tk.Frame(window, bg=YELLOW)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(
        main_frame,
        text="Timer",
        font=(FONT_NAME, 40, "bold"),
        fg=GREEN,
        bg=YELLOW,
        width=12
    )
    title_label.pack(pady=(0, 20))

    canvas = tk.Canvas(
        main_frame,
        width=220,
        height=240,
        bg=YELLOW,
        highlightthickness=0
    )
    tomato = tk.PhotoImage(file="tomato.png")
    canvas.create_image(110, 120, image=tomato)
    timer_text = canvas.create_text(
        110, 135,
        text="00:00",
        fill="white",
        font=(FONT_NAME, 36, "bold")
    )
    canvas.image = tomato
    canvas.pack(pady=10)

    controls = tk.Frame(main_frame, bg=YELLOW)
    controls.pack(pady=20)

    start_btn = tk.Button(
        controls,
        text="Start",
        font=(FONT_NAME, 14, "bold"),
        width=8,
        bg=GREEN,
        fg=DARK,
        command=lambda: start_timer(
            window, canvas, timer_text, title_label, check_marks
        )
    )
    start_btn.grid(row=0, column=0, padx=10)

    reset_btn = tk.Button(
        controls,
        text="Reset",
        font=(FONT_NAME, 14, "bold"),
        width=8,
        bg=PINK,
        fg=DARK,
        command=lambda: reset_timer(
            window, canvas, timer_text, title_label, check_marks
        )
    )
    reset_btn.grid(row=0, column=1, padx=10)

    progress_frame = tk.Frame(main_frame, bg=YELLOW)
    progress_frame.pack(pady=(10, 0))

    scrollbar = tk.Scrollbar(
        progress_frame,
        orient="horizontal",
        bg=DARK,
        troughcolor="#dcdacb",
        activebackground=GREEN,
        highlightthickness=0,
        bd=0
    )
    scrollbar.pack(side="bottom", fill="x", pady=(4, 8))

    check_marks = tk.Text(
        progress_frame,
        height=1,
        width=20,
        font=(FONT_NAME, 20, "bold"),
        fg=GREEN,
        bg=YELLOW,
        wrap="none",
        xscrollcommand=scrollbar.set,
        highlightthickness=2,
        highlightbackground=GREEN,
        bd=0
    )
    check_marks.pack(side="top")
    check_marks.config(state="disabled")

    scrollbar.config(command=check_marks.xview)

    return window
