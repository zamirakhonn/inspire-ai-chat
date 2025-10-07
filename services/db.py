# services/db.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
import os

# -----------------------------
# Database setup
# -----------------------------
DB_URL = os.getenv("DATABASE_URL", "sqlite:///inspire.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# -----------------------------
# Models
# -----------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="user")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(50))  # "user" or "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")


# -----------------------------
# Utility functions
# -----------------------------
def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_or_create_user(session, user_identifier: str):
    """Find user by identifier or create if not exists."""
    user = session.query(User).filter_by(user_id=user_identifier).first()
    if not user:
        user = User(user_id=user_identifier, name=user_identifier)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user
