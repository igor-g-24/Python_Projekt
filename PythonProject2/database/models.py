from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///hangman.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    words = relationship("Word", back_populates="category")

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="words")