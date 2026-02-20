import tkinter as tk
from tkinter import messagebox
import time

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Extended long-form sample text for typing practice (no repetition operators)

        self.long_text = (
            "The quick brown fox jumps over the lazy dog. This sentence is often used to display all letters of the alphabet, "
            "but in a typing practice environment it serves as a simple warm-up line that helps users adjust their posture and rhythm. "
            "Typing is not merely about speed; it is about accuracy, consistency, and endurance. Developing strong typing skills "
            "requires focus and deliberate repetition over time. Many beginners rush to increase their words per minute, but true "
            "improvement begins with minimizing errors and building proper finger placement habits.\n\n"

            "Python is an interpreted, high-level, general-purpose programming language known for its readability and versatility. "
            "Developers across industries use Python for web development, data analysis, machine learning, automation, and scripting. "
            "Because Python emphasizes clean and expressive syntax, it is often recommended as a first language for beginners. "
            "However, mastering Python also requires understanding advanced concepts such as asynchronous programming, memory management, "
            "and architectural design principles. The more code you read and write, the more naturally structured thinking becomes.\n\n"

            "Typing speed is measured in words per minute, commonly abbreviated as WPM. This metric calculates how many standard-length "
            "words a person can type in sixty seconds. A strong typist balances speed with precision, ensuring that the error rate remains low. "
            "Professional developers, writers, and analysts rely on efficient typing to translate ideas into executable instructions quickly. "
            "When typing becomes second nature, cognitive energy can be directed toward problem-solving rather than mechanical input.\n\n"

            "Practice makes perfect when it comes to improving your typing skills. Consistent daily sessions produce better results than "
            "sporadic, intense bursts of effort. Maintaining proper posture, keeping wrists relaxed, and positioning fingers correctly "
            "on the home row are fundamental habits. Over time, muscle memory forms naturally, reducing the need to look at the keyboard. "
            "Confidence builds gradually as the mind and fingers synchronize into a smooth, uninterrupted workflow.\n\n"

            "Tkinter is the standard graphical user interface library that comes bundled with Python. It allows developers to create "
            "desktop applications with windows, buttons, labels, text boxes, and interactive components. Although it is relatively simple "
            "compared to modern GUI frameworks, Tkinter remains valuable for learning interface fundamentals and building lightweight tools. "
            "Understanding event-driven programming within GUI environments reinforces core software development principles.\n\n"

            "A journey of a thousand miles begins with a single step. This proverb emphasizes the importance of starting, even when the goal "
            "seems distant or intimidating. In both programming and typing, incremental progress accumulates into meaningful mastery. "
            "Small improvements compound over weeks and months, transforming novice skills into professional competence. Discipline, patience, "
            "and curiosity form the foundation of sustainable growth in any technical field.\n\n"

            "Software engineering is not simply about writing code that works. It involves designing systems that remain maintainable, scalable, "
            "and secure over time. Clean architecture, modular structure, and thoughtful documentation reduce long-term complexity. Version control "
            "systems such as Git enable collaborative development, allowing teams to manage changes safely and efficiently. Understanding commit "
            "history and branch structures is essential for professional-level workflow.\n\n"

            "Continuous learning defines the technology industry. Tools evolve, frameworks shift, and best practices adapt as new discoveries emerge. "
            "Engineers who cultivate adaptability and critical thinking remain resilient in dynamic environments. Reading technical documentation, "
            "analyzing open-source projects, and experimenting with new ideas strengthen long-term competence. The pursuit of mastery is not a sprint "
            "but a steady progression built upon curiosity and structured effort."
        )

        self.target_text = self.long_text
        self.duration = 60          # default 60 seconds
        self.start_time = None
        self.timer_running = False
        self.after_id = None
        self.end_after_id = None

        self.create_widgets()
        self.reset_test()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Typing Speed Test", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Duration selection
        duration_frame = tk.Frame(self.root)
        duration_frame.pack(pady=5)

        tk.Label(duration_frame, text="Test duration:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        self.duration_var = tk.IntVar(value=60)
        rb30 = tk.Radiobutton(duration_frame, text="30 seconds", variable=self.duration_var,
                              value=30, command=self.set_duration, font=("Arial", 10))
        rb30.pack(side=tk.LEFT, padx=5)
        rb60 = tk.Radiobutton(duration_frame, text="1 minute", variable=self.duration_var,
                              value=60, command=self.set_duration, font=("Arial", 10))
        rb60.pack(side=tk.LEFT, padx=5)

        # Frame for target text (scrollable)
        target_frame = tk.Frame(self.root, bg="#f0f0f0", relief=tk.GROOVE, bd=2)
        target_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(target_frame, text="Type this text:", font=("Arial", 12)).pack(anchor="w", padx=5, pady=5)
        self.target_text_display = tk.Text(target_frame, height=8, wrap=tk.WORD, font=("Courier", 11),
                                           bg="#e8e8e8", state=tk.DISABLED)
        self.target_text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar for target text
        scroll_target = tk.Scrollbar(target_frame, command=self.target_text_display.yview)
        scroll_target.pack(side=tk.RIGHT, fill=tk.Y)
        self.target_text_display.config(yscrollcommand=scroll_target.set)

        # Frame for user input (scrollable)
        input_frame = tk.Frame(self.root, bg="#f0f0f0", relief=tk.GROOVE, bd=2)
        input_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(input_frame, text="Your typing:", font=("Arial", 12)).pack(anchor="w", padx=5, pady=5)
        self.input_text = tk.Text(input_frame, height=8, wrap=tk.WORD, font=("Courier", 11),
                                  state=tk.DISABLED)
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar for input text
        scroll_input = tk.Scrollbar(input_frame, command=self.input_text.yview)
        scroll_input.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=scroll_input.set)

        # Bind key release to check typing progress
        self.input_text.bind("<KeyRelease>", self.on_key_release)

        # Frame for timer and stats
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=10)

        self.time_label = tk.Label(stats_frame, text="Time left: 60 s", font=("Arial", 12))
        self.time_label.grid(row=0, column=0, padx=10)

        self.wpm_label = tk.Label(stats_frame, text="WPM: 0", font=("Arial", 12))
        self.wpm_label.grid(row=0, column=1, padx=10)

        self.accuracy_label = tk.Label(stats_frame, text="Accuracy: 100%", font=("Arial", 12))
        self.accuracy_label.grid(row=0, column=2, padx=10)

        self.correct_chars_label = tk.Label(stats_frame, text="Correct: 0", font=("Arial", 10))
        self.correct_chars_label.grid(row=1, column=0, padx=10, pady=2)

        self.total_chars_label = tk.Label(stats_frame, text="Total typed: 0", font=("Arial", 10))
        self.total_chars_label.grid(row=1, column=1, padx=10, pady=2)

        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_test, width=10)
        self.start_button.grid(row=0, column=0, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_test, width=10)
        self.reset_button.grid(row=0, column=1, padx=5)

    def set_duration(self):
        """Update the duration based on radio button selection."""
        self.duration = self.duration_var.get()
        if not self.timer_running:
            self.time_label.config(text=f"Time left: {self.duration} s")

    def reset_test(self):
        """Reset the test: clear input, reset timer and stats."""
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        if self.end_after_id:
            self.root.after_cancel(self.end_after_id)
            self.end_after_id = None

        # Display target text (long, read-only)
        self.target_text_display.config(state=tk.NORMAL)
        self.target_text_display.delete(1.0, tk.END)
        self.target_text_display.insert(1.0, self.target_text)
        self.target_text_display.config(state=tk.DISABLED)

        # Clear and disable input
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete(1.0, tk.END)
        self.input_text.config(state=tk.DISABLED)

        self.start_time = None
        self.timer_running = False
        self.time_label.config(text=f"Time left: {self.duration} s")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 100%")
        self.correct_chars_label.config(text="Correct: 0")
        self.total_chars_label.config(text="Total typed: 0")

        self.start_button.config(state=tk.NORMAL)

    def start_test(self):
        """Enable input, start countdown timer, and schedule test end."""
        self.input_text.config(state=tk.NORMAL)
        self.input_text.focus_set()
        self.input_text.delete(1.0, tk.END)   # ensure clean start
        self.start_time = time.time()
        self.timer_running = True

        # Disable duration radio buttons and start button
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                for sub in child.winfo_children():
                    if isinstance(sub, tk.Radiobutton):
                        sub.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)

        # Start countdown updates
        self.update_countdown()
        # Schedule test end after duration seconds
        self.end_after_id = self.root.after(self.duration * 1000, self.finish_test)

    def update_countdown(self):
        """Update the countdown timer every 100 ms."""
        if self.timer_running:
            elapsed = time.time() - self.start_time
            remaining = max(0, self.duration - elapsed)
            self.time_label.config(text=f"Time left: {remaining:.1f} s")
            if remaining > 0:
                self.after_id = self.root.after(100, self.update_countdown)
            else:
                self.time_label.config(text="Time left: 0.0 s")

    def calculate_stats(self):
        """Compute current WPM, accuracy, correct and total characters."""
        target = self.target_text
        user_input = self.input_text.get(1.0, tk.END).rstrip("\n")  # remove trailing newline

        total_typed = len(user_input)
        if total_typed == 0:
            return 0, 100.0, 0, 0

        # Count correct characters up to the length of the shorter string
        correct = 0
        for i in range(min(len(target), len(user_input))):
            if target[i] == user_input[i]:
                correct += 1

        accuracy = (correct / total_typed) * 100

        # WPM = (correct characters / 5) / time in minutes
        if self.start_time and self.timer_running:
            elapsed = time.time() - self.start_time
            elapsed_minutes = elapsed / 60.0
            if elapsed_minutes > 0:
                wpm = (correct / 5) / elapsed_minutes
            else:
                wpm = 0
        else:
            # For final stats after timer stops, use total duration
            elapsed_minutes = self.duration / 60.0
            wpm = (correct / 5) / elapsed_minutes if elapsed_minutes > 0 else 0

        return round(wpm), round(accuracy, 1), correct, total_typed

    def on_key_release(self, event):
        """Called whenever a key is released in the input widget."""
        if not self.timer_running:
            return

        wpm, accuracy, correct, total = self.calculate_stats()
        self.wpm_label.config(text=f"WPM: {wpm}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy}%")
        self.correct_chars_label.config(text=f"Correct: {correct}")
        self.total_chars_label.config(text=f"Total typed: {total}")

    def finish_test(self):
        """Stop the test, compute final stats, and show results."""
        self.timer_running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        if self.end_after_id:
            self.root.after_cancel(self.end_after_id)
            self.end_after_id = None

        # Disable input
        self.input_text.config(state=tk.DISABLED)

        # Re-enable radio buttons
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                for sub in child.winfo_children():
                    if isinstance(sub, tk.Radiobutton):
                        sub.config(state=tk.NORMAL)

        # Calculate final stats using full duration
        wpm, accuracy, correct, total = self.calculate_stats()
        # Ensure WPM is based on total duration, not current time (timer stopped)
        # We already handle that in calculate_stats when timer_running is False

        self.time_label.config(text=f"Time left: 0.0 s")
        self.wpm_label.config(text=f"WPM: {wpm}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy}%")
        self.correct_chars_label.config(text=f"Correct: {correct}")
        self.total_chars_label.config(text=f"Total typed: {total}")

        messagebox.showinfo("Test Complete",
                            f"Time: {self.duration} seconds\n"
                            f"Correct characters: {correct}\n"
                            f"Total typed: {total}\n"
                            f"Accuracy: {accuracy}%\n"
                            f"WPM: {wpm}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()