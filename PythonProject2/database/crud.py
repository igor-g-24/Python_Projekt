import random
from .models import SessionLocal, Word, User


def get_random_word():
    db = SessionLocal()
    count = db.query(Word).count()
    if count == 0:
        db.close()
        return None

    random_offset = random.randint(0, count - 1)
    word_obj = db.query(Word).offset(random_offset).first()

    word_text = word_obj.text if word_obj else None
    db.close()
    return word_text


def update_user_stats(user_id, won=False):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.games_played += 1
        if won:
            user.games_won += 1
        db.commit()
    db.close()


def get_all_users_stats():
    db = SessionLocal()
    users = db.query(User).order_by(User.games_won.desc()).all()
    db.close()
    return users