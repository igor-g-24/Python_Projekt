import tkinter as tk
from baza.database import init_db
from gui.powitanie import show_welcome_screen

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    root.title("Wisielec")
    root.geometry("600x400")
    show_welcome_screen(root)
    root.mainloop()