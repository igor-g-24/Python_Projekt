import tkinter as tk


def show_login_screen(root):
    from gui.background import set_background
    from gui.powitanie import show_welcome_screen
    for widget in root.winfo_children():
        widget.destroy()

    set_background(root)

    login_label = tk.Label(root, text="Nazwa użytkownika:")
    login_label.place(relx=0.4, rely=0.4, anchor="center")

    login_entry = tk.Entry(root)
    login_entry.place(relx=0.6, rely=0.4, anchor="center")

    password_label = tk.Label(root, text="Hasło:")
    password_label.place(relx=0.4, rely=0.5, anchor="center")

    password_entry = tk.Entry(root, show="*")
    password_entry.place(relx=0.6, rely=0.5, anchor="center")

    back_btn = tk.Button(root, text="Powrót", command=lambda: show_welcome_screen(root))
    back_btn.place(relx=0.5, rely=0.7, anchor="center")