import tkinter as tk
from ui import AgeCounterUI

def main():
    root = tk.Tk()
    root.title("Live Age Counter")
    root.geometry("450x500")
    root.resizable(False, False)

    AgeCounterUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
