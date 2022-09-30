import tkinter as tk

from initial_screen import AppSelectorScreen

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hello there")
    root.maxsize(900, 600)
    app = AppSelectorScreen(root)
    root.mainloop()