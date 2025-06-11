import os
from gui.main_app import HangmanApp
from database.database_setup import setup_database

if __name__ == "__main__":
    # Sprawdź, czy baza danych istnieje, jeśli nie, stwórz ją
    if not os.path.exists("hangman.db"):
        print("Tworzenie nowej bazy danych...")
        setup_database()

    app = HangmanApp()
    app.mainloop()