from baza.models import User
from baza.database import SessionLocal

def register_user(username, password):
    session = SessionLocal()
    existing = session.query(User).filter_by(username=username).first()
    if existing:
        session.close()
        return False
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    session.close()
    return True

def login_user(username, password):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username, password=password).first()
    session.close()
    return user is not None