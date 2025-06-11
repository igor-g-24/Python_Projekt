from .models import Base, engine, SessionLocal, Word


def setup_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    if db.query(Word).count() == 0:
        print("Wypełnianie bazy danych hasłami z pliku hasla.txt...")

        try:
            with open('hasla.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    word_text = line.strip().upper()
                    if word_text:
                        word = Word(text=word_text)
                        db.add(word)

            db.commit()
            print(f"Baza danych została pomyślnie wypełniona.")
        except FileNotFoundError:
            print(
                "BŁĄD: Nie znaleziono pliku 'hasla.txt'. Upewnij się, że znajduje się on w głównym folderze projektu.")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd podczas ładowania haseł: {e}")
            db.rollback()
    else:
        print("Baza danych z hasłami już istnieje.")

    db.close()


if __name__ == '__main__':
    setup_database()