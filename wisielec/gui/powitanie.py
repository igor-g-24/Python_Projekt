import tkinter as tk


def show_welcome_screen(root):
    from gui.background import set_background
    from gui.logowanie import show_login_screen
    from gui.rejestrowanie import show_register_screen
    for widget in root.winfo_children():
        widget.destroy()

    set_background(root)

    login_btn = tk.Button(root, text="Zaloguj się", command=lambda: show_login_screen(root))
    register_btn = tk.Button(root, text="Zarejestruj się", command=lambda: show_register_screen(root))

    login_btn.place(relx=0.3, rely=0.6, anchor="center", width=150, height=40)
    register_btn.place(relx=0.7, rely=0.6, anchor="center", width=150, height=40)