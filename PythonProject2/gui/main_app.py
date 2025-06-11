import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from services import auth, export
from database import crud
from core.game_logic import SinglePlayer, TwoPlayer

NOTEBOOK_BG = "#FEFCEF"
FONT_FAMILY = "Courier New"


class HangmanApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Wisielec")
        self.geometry("800x600")
        self.current_user = None
        self.player2_user = None

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", background=NOTEBOOK_BG, font=(FONT_FAMILY, 12))
        style.configure("TButton", background="#E0E0E0", font=(FONT_FAMILY, 12), padding=5)
        style.map("TButton", background=[("active", "#C0C0C0")])
        style.configure("TEntry", font=(FONT_FAMILY, 12))

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, MainMenuFrame, Player2LoginFrame, GameFrame, StatsFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

    def start_single_player_game(self):
        word = crud.get_random_word()
        if not word:
            messagebox.showerror("Błąd", "Brak haseł w bazie danych! Uruchom ponownie aplikację.")
            return

        game_instance = SinglePlayer(word, self.current_user.id)
        game_frame = self.frames[GameFrame]
        game_frame.setup_game(game_instance, word, 'single')
        self.show_frame(GameFrame)

    def start_two_player_game(self):
        word = crud.get_random_word()
        if not word:
            messagebox.showerror("Błąd", "Brak haseł w bazie danych! Uruchom ponownie aplikację.")
            return

        game_instance = TwoPlayer(word, self.current_user.id, self.player2_user.id)
        game_frame = self.frames[GameFrame]
        game_frame.setup_game(game_instance, word, 'two', self.current_user.username, self.player2_user.username)
        self.show_frame(GameFrame)

    def logout(self):
        self.current_user = None
        self.player2_user = None
        self.show_frame(LoginFrame)


class NotebookFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.canvas = tk.Canvas(self, bg=NOTEBOOK_BG, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Configure>", self.draw_notebook_background)

    def draw_notebook_background(self, event=None):
        self.canvas.delete("background")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        for i in range(0, height, 25):
            self.canvas.create_line(0, i, width, i, fill="#a0c0ff", tags="background")
        self.canvas.create_line(50, 0, 50, height, fill="#ff8080", width=2, tags="background")


class LoginFrame(NotebookFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self.canvas, text="Wisielec", font=(FONT_FAMILY, 32, "bold"), bg=NOTEBOOK_BG).place(relx=0.5, rely=0.2,
                                                                                                     anchor="center")
        tk.Label(self.canvas, text="Nazwa użytkownika:", font=(FONT_FAMILY, 12), bg=NOTEBOOK_BG).place(relx=0.5,
                                                                                                       rely=0.4,
                                                                                                       anchor="center")
        self.username_entry = ttk.Entry(self.canvas, width=30, font=(FONT_FAMILY, 12))
        self.username_entry.place(relx=0.5, rely=0.45, anchor="center")
        tk.Label(self.canvas, text="Hasło:", font=(FONT_FAMILY, 12), bg=NOTEBOOK_BG).place(relx=0.5, rely=0.55,
                                                                                           anchor="center")
        self.password_entry = ttk.Entry(self.canvas, show="*", width=30, font=(FONT_FAMILY, 12))
        self.password_entry.place(relx=0.5, rely=0.6, anchor="center")
        ttk.Button(self.canvas, text="Zaloguj", command=self.login).place(relx=0.4, rely=0.7, anchor="center")
        ttk.Button(self.canvas, text="Zarejestruj", command=self.register).place(relx=0.6, rely=0.7, anchor="center")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = auth.login_user(username, password)
        if user:
            self.controller.current_user = user
            self.controller.show_frame(MainMenuFrame)
            self.password_entry.delete(0, 'end')
        else:
            messagebox.showerror("Błąd", "Nieprawidłowa nazwa użytkownika lub hasło.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = auth.register_user(username, password)
        messagebox.showinfo("Rejestracja", message)


class Player2LoginFrame(NotebookFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self.canvas, text="Logowanie Gracza 2", font=(FONT_FAMILY, 24, "bold"), bg=NOTEBOOK_BG).place(relx=0.5,
                                                                                                               rely=0.2,
                                                                                                               anchor="center")
        tk.Label(self.canvas, text="Nazwa użytkownika:", font=(FONT_FAMILY, 12), bg=NOTEBOOK_BG).place(relx=0.5,
                                                                                                       rely=0.4,
                                                                                                       anchor="center")
        self.username_entry = ttk.Entry(self.canvas, width=30, font=(FONT_FAMILY, 12))
        self.username_entry.place(relx=0.5, rely=0.45, anchor="center")
        tk.Label(self.canvas, text="Hasło:", font=(FONT_FAMILY, 12), bg=NOTEBOOK_BG).place(relx=0.5, rely=0.55,
                                                                                           anchor="center")
        self.password_entry = ttk.Entry(self.canvas, show="*", width=30, font=(FONT_FAMILY, 12))
        self.password_entry.place(relx=0.5, rely=0.6, anchor="center")
        ttk.Button(self.canvas, text="Zaloguj Gracza 2", command=self.login_player2).place(relx=0.5, rely=0.7,
                                                                                           anchor="center")
        ttk.Button(self.canvas, text="Powrót", command=lambda: controller.show_frame(MainMenuFrame)).place(relx=0.5,
                                                                                                           rely=0.8,
                                                                                                           anchor="center")

    def login_player2(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == self.controller.current_user.username:
            messagebox.showerror("Błąd", "Gracz 2 nie może być tą samą osobą co Gracz 1.")
            return
        user = auth.login_user(username, password)
        if user:
            self.controller.player2_user = user
            self.password_entry.delete(0, 'end')
            self.controller.start_two_player_game()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowa nazwa użytkownika lub hasło.")


class MainMenuFrame(NotebookFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.welcome_label = tk.Label(self.canvas, text="", font=(FONT_FAMILY, 16), bg=NOTEBOOK_BG)
        self.welcome_label.place(relx=0.5, rely=0.2, anchor="center")
        ttk.Button(self.canvas, text="Gra Jednoosobowa", command=controller.start_single_player_game).place(relx=0.5,
                                                                                                            rely=0.4,
                                                                                                            anchor="center",
                                                                                                            width=300)
        ttk.Button(self.canvas, text="Gra Dwuosobowa", command=lambda: controller.show_frame(Player2LoginFrame)).place(
            relx=0.5, rely=0.5, anchor="center", width=300)
        ttk.Button(self.canvas, text="Statystyki", command=lambda: controller.show_frame(StatsFrame)).place(relx=0.5,
                                                                                                            rely=0.6,
                                                                                                            anchor="center",
                                                                                                            width=300)
        ttk.Button(self.canvas, text="Eksportuj Statystyki (CSV)", command=self.export_stats).place(relx=0.5, rely=0.7,
                                                                                                    anchor="center",
                                                                                                    width=300)
        ttk.Button(self.canvas, text="Wyloguj", command=controller.logout).place(relx=0.5, rely=0.8, anchor="center",
                                                                                 width=300)

    def on_show(self):
        if self.controller.current_user:
            self.welcome_label.config(text=f"Witaj, {self.controller.current_user.username}!")

    def export_stats(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Pliki CSV", "*.csv")])
        if filepath:
            success, message = export.export_stats_to_csv(filepath)
            if success:
                messagebox.showinfo("Sukces", message)
            else:
                messagebox.showerror("Błąd", message)


class GameFrame(NotebookFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.game = None
        self.keyboard_buttons = {}

    def setup_game(self, game_instance, word, mode, p1_name=None, p2_name=None):
        self.game = game_instance
        self.mode = mode
        self.p1_name = p1_name
        self.p2_name = p2_name
        for widget in self.canvas.winfo_children():
            widget.destroy()
        self.canvas.delete("hangman")

        self.word_label = tk.Label(self.canvas, text=self.game.game.get_display_word(), font=(FONT_FAMILY, 30),
                                   bg=NOTEBOOK_BG)
        self.word_label.place(relx=0.6, rely=0.25, anchor="center")

        self.lives_label = tk.Label(self.canvas, font=(FONT_FAMILY, 14), bg=NOTEBOOK_BG, justify="center")
        self.lives_label.place(relx=0.6, rely=0.35, anchor="center")

        self.keyboard_frame = tk.Frame(self.canvas, bg=NOTEBOOK_BG)
        self.keyboard_frame.place(relx=0.6, rely=0.65, anchor="center")

        self.create_keyboard()
        self.update_lives_label()

    def create_keyboard(self):
        polish_alphabet = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ"
        row = 0
        col = 0
        self.keyboard_buttons = {}
        for letter in polish_alphabet:
            btn = ttk.Button(self.keyboard_frame, text=letter, width=3, command=lambda l=letter: self.handle_guess(l))
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.keyboard_buttons[letter] = btn
            col += 1
            if col > 8:
                col = 0
                row += 1

    def handle_guess(self, letter):
        if not self.game:
            return
        result = self.game.make_guess(letter)
        self.keyboard_buttons[letter]['state'] = 'disabled'
        if result == "incorrect":
            lives_lost = self.game.game.max_lives - self.game.lives if self.mode == 'single' \
                else (self.game.game.max_lives // 2 * 2) - (self.game.players[1]['lives'] +self.game.players[2]['lives'])
            self.draw_hangman_part(lives_lost)
        self.word_label.config(text=self.game.game.get_display_word())
        self.update_lives_label()
        if self.game.is_game_over():
            self.end_game()

    def draw_hangman_part(self, part_number):
        x = 180
        y = 450
        line_color = "black"
        line_width = 3
        parts = [
            lambda: self.canvas.create_line(x - 100, y, x + 100, y, width=line_width, fill=line_color, tags="hangman"),
            lambda: self.canvas.create_line(x, y, x, y - 300, width=line_width, fill=line_color, tags="hangman"),
            lambda: self.canvas.create_line(x, y - 300, x - 150, y - 300, width=line_width, fill=line_color,
                                            tags="hangman"),
            lambda: self.canvas.create_line(x - 150, y - 300, x - 150, y - 250, width=line_width, fill=line_color,
                                            tags="hangman"),
            lambda: self.canvas.create_oval(x - 175, y - 250, x - 125, y - 200, width=line_width, outline=line_color,
                                            tags="hangman"),
            lambda: self.canvas.create_line(x - 150, y - 200, x - 150, y - 100, width=line_width, fill=line_color,
                                            tags="hangman"),
            lambda: self.canvas.create_line(x - 150, y - 175, x - 200, y - 150, width=line_width, fill=line_color,
                                            tags="hangman"),
            lambda: self.canvas.create_line(x - 150, y - 175, x - 100, y - 150, width=line_width, fill=line_color,
                                            tags="hangman"),
            lambda: self.canvas.create_line(x - 150, y - 100, x - 200, y - 50, width=line_width, fill=line_color,
                                            tags="hangman"),
            lambda: self.canvas.create_line(x - 150, y - 100, x - 100, y - 50, width=line_width, fill=line_color,
                                            tags="hangman")
        ]
        if 1 <= part_number <= len(parts):
            parts[part_number - 1]()

    def update_lives_label(self):
        if self.mode == 'single':
            self.lives_label.config(text=f"Życia: {self.game.lives}")
        else:
            p1_lives = self.game.players[1]['lives']
            p2_lives = self.game.players[2]['lives']
            current_player_name = self.p1_name if self.game.current_player == 1 else self.p2_name
            if self.game.players[self.game.current_player]['lives'] <= 0:
                self.lives_label.config(
                    text=f"Tura: {current_player_name} (BRAK ŻYĆ)\n{self.p1_name}: {p1_lives} | {self.p2_name}: {p2_lives}")
            else:
                self.lives_label.config(
                    text=f"Tura: {current_player_name}\n{self.p1_name}: {p1_lives} żyć | {self.p2_name}: {p2_lives} żyć")

    def end_game(self):
        won = self.game.game.is_won()
        message = ""
        if self.mode == 'single':
            crud.update_user_stats(self.game.user_id, won)
            message = "Wygrałeś!" if won else f"Przegrałeś! Hasło to: {self.game.game.word_to_guess}"
        else:
            if won:
                winner_id = self.game.winner
                winner_name = self.p1_name if winner_id == self.controller.current_user.id else self.p2_name
                message = f"Wygrał {winner_name}!"
                crud.update_user_stats(winner_id, won=True)
                loser_id = self.game.players[2]['id'] if winner_id == self.game.players[1]['id'] else \
                self.game.players[1]['id']
                crud.update_user_stats(loser_id, won=False)
            else:
                message = f"Remis! Nikt nie odgadł hasła.\nHasło to: {self.game.game.word_to_guess}"
                crud.update_user_stats(self.game.players[1]['id'], won=False)
                crud.update_user_stats(self.game.players[2]['id'], won=False)
        messagebox.showinfo("Koniec Gry", message)
        self.controller.show_frame(MainMenuFrame)


class StatsFrame(NotebookFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self.canvas, text="Ranking Graczy", font=(FONT_FAMILY, 24, "bold"), bg=NOTEBOOK_BG).place(relx=0.5,
                                                                                                           rely=0.1,
                                                                                                           anchor="center")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(FONT_FAMILY, 12, "bold"))
        style.configure("Treeview", font=(FONT_FAMILY, 11), rowheight=25)
        self.tree = ttk.Treeview(self.canvas, columns=("rank", "username", "played", "won"), show="headings")
        self.tree.heading("rank", text="Miejsce")
        self.tree.heading("username", text="Gracz")
        self.tree.heading("played", text="Rozegrane gry")
        self.tree.heading("won", text="Wygrane gry")
        self.tree.column("rank", width=80, anchor="center")
        self.tree.column("username", width=200, anchor="center")
        self.tree.column("played", width=150, anchor="center")
        self.tree.column("won", width=150, anchor="center")
        self.tree.place(relx=0.5, rely=0.5, anchor="center", relheight=0.7, relwidth=0.9)
        ttk.Button(self.canvas, text="Powrót do menu", command=lambda: controller.show_frame(MainMenuFrame)).place(
            relx=0.5, rely=0.9, anchor="center")

    def on_show(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        users = crud.get_all_users_stats()
        for i, user in enumerate(users, 1):
            self.tree.insert("", "end", values=(i, user.username, user.games_played, user.games_won))