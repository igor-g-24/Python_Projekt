from .models import Base, engine, SessionLocal, Category, Word


def setup_database():
    """Tworzy tabele i wypełnia je początkowymi danymi, jeśli nie istnieją."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Sprawdź, czy kategorie już istnieją
    if db.query(Category).count() == 0:
        print("Wypełnianie bazy danych początkowymi danymi...")

        # Kategorie
        cat_zwierzeta = Category(name="Zwierzęta")
        cat_owoce = Category(name="Owoce")
        cat_panstwa = Category(name="Państwa")

        db.add_all([cat_zwierzeta, cat_owoce, cat_panstwa])
        db.commit()  # Commit, aby uzyskać ID dla kategorii

        # Hasła
        words_data = [
            ("KROKODYL", cat_zwierzeta), ("SŁOŃ", cat_zwierzeta), ("ŻYRAFA", cat_zwierzeta),
            ("JABŁKO", cat_owoce), ("BANAN", cat_owoce), ("TRUSKAWKA", cat_owoce),
            ("POLSKA", cat_panstwa), ("NIEMCY", cat_panstwa), ("HISZPANIA", cat_panstwa)
        ]

        for text, category in words_data:
            word = Word(text=text, category=category)
            db.add(word)

        db.commit()
        print("Baza danych została pomyślnie zainicjowana.")
    else:
        print("Baza danych już istnieje.")

    db.close()


if __name__ == '__main__':
    setup_database()