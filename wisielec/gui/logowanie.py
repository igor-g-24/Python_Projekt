import tkinter as tk
from tkinter import messagebox


def show_login_screen(root):
    from Logic.autoryzacja import login_user
    from gui.powitanie import show_welcome_screen
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Login").pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Hasło").pack(pady=10)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if login_user(username, password):
            messagebox.showinfo("Sukces", "Zalogowano!")
            # TODO: przejście do gry
        else:
            messagebox.showerror("Błąd", "Nieprawidłowe dane")

    tk.Button(root, text="Zaloguj", command=handle_login).pack(pady=10)
    tk.Button(root, text="Wróć", command=lambda: show_welcome_screen(root)).pack()