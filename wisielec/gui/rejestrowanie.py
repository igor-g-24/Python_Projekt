import tkinter as tk


def show_register_screen(root):
    from gui.background import set_background
    from gui.powitanie import show_welcome_screen
    for widget in root.winfo_children():
        widget.destroy()

    set_background(root)

    username_label = tk.Label(root, text="Nazwa użytkownika:")
    username_label.place(relx=0.4, rely=0.45, anchor="center")

    username_entry = tk.Entry(root)
    username_entry.place(relx=0.6, rely=0.45, anchor="center")

    password_label = tk.Label(root, text="Hasło:")
    password_label.place(relx=0.4, rely=0.55, anchor="center")

    password_entry = tk.Entry(root, show="*")
    password_entry.place(relx=0.6, rely=0.55, anchor="center")

    def register():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            print("Uzupełnij wszystkie pola.")
        else:
            print(f"Zarejestrowano: {username}")
            show_welcome_screen(root)

    register_btn = tk.Button(root, text="Zarejestruj", command=register)
    register_btn.place(relx=0.5, rely=0.7, anchor="center")

    back_btn = tk.Button(root, text="Powrót", command=lambda: show_welcome_screen(root))
    back_btn.place(relx=0.5, rely=0.8, anchor="center")