import tkinter as tk
from tkinter import messagebox


def show_register_screen(root):
    from Logic.autoryzacja import register_user
    from gui.powitanie import show_welcome_screen
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Rejestracja").pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Hasło").pack(pady=10)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Sukces", "Zarejestrowano pomyślnie!")
            show_welcome_screen(root)
        else:
            messagebox.showerror("Błąd", "Użytkownik już istnieje!")

    tk.Button(root, text="Zarejestruj", command=handle_register).pack(pady=10)
    tk.Button(root, text="Wróć", command=lambda: show_welcome_screen(root)).pack()