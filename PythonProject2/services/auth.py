import bcrypt
from database.models import SessionLocal, User


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def register_user(username, password):
    db = SessionLocal()
    if db.query(User).filter(User.username == username).first():
        db.close()
        return False, "Użytkownik o tej nazwie już istnieje."

    hashed = hash_password(password)
    new_user = User(username=username, password_hash=hashed.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.close()
    return True, "Rejestracja pomyślna."


def login_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if user and check_password(password, user.password_hash.encode('utf-8')):
        return user
    return None