import random
from .models import SessionLocal, Word, Category, User


def get_random_word():
    """Pobiera losowe słowo i jego kategorię z bazy danych."""
    db = SessionLocal()
    count = db.query(Word).count()
    if count == 0:
        db.close()
        return None, None

    random_id = random.randint(1, count)
    word_obj = db.query(Word).filter(Word.id == random_id).first()
    category_name = word_obj.category.name
    word_text = word_obj.text
    db.close()
    return word_text, category_name


def update_user_stats(user_id, won=False):
    """Aktualizuje statystyki użytkownika po grze."""
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.games_played += 1
        if won:
            user.games_won += 1
        db.commit()
    db.close()


def get_all_users_stats():
    """Pobiera statystyki wszystkich użytkowników."""
    db = SessionLocal()
    users = db.query(User).order_by(User.games_won.desc()).all()
    db.close()
    return users