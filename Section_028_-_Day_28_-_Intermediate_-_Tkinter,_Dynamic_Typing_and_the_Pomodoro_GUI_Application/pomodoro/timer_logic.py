import tkinter as tk
from constants import *
import state

def reset_timer(window, canvas, timer_text, title_label, check_marks):
    if state.timer:
        window.after_cancel(state.timer)

    state.reps = 0
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)

    check_marks.config(state="normal")
    check_marks.delete("1.0", tk.END)
    check_marks.config(state="disabled")
    check_marks.xview_moveto(0.0)


def start_timer(window, canvas, timer_text, title_label, check_marks):
    state.reps += 1

    work = WORK_MIN * SECONDS_PER_MIN
    short = SHORT_BREAK_MIN * SECONDS_PER_MIN
    long = LONG_BREAK_MIN * SECONDS_PER_MIN

    if state.reps % 8 == 0:
        title_label.config(text="Long Break", fg=GREEN)
        countdown(window, long, canvas, timer_text, title_label, check_marks)
    elif state.reps % 2 == 0:
        title_label.config(text="Short Break", fg=PINK)
        countdown(window, short, canvas, timer_text, title_label, check_marks)
    else:
        title_label.config(text="Work", fg=RED)
        countdown(window, work, canvas, timer_text, title_label, check_marks)


def countdown(window, count, canvas, timer_text, title_label, check_marks):
    minutes = count // 60
    seconds = count % 60

    canvas.itemconfig(timer_text, text=f"{minutes:02d}:{seconds:02d}")

    if count > 0:
        state.timer = window.after(
            1000,
            countdown,
            window,
            count - 1,
            canvas,
            timer_text,
            title_label,
            check_marks
        )
    else:
        start_timer(window, canvas, timer_text, title_label, check_marks)

        marks = ""
        for i in range(1, state.reps // 2 + 1):
            marks += "✓"
            if i % 4 == 0:
                marks += ","

        check_marks.config(state="normal")
        check_marks.delete("1.0", tk.END)
        check_marks.insert(tk.END, marks)
        check_marks.config(state="disabled")
        check_marks.xview_moveto(1.0)
