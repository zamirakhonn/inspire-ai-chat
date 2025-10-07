# services/history.py
from services.db import SessionLocal, get_or_create_user, Message, User
from datetime import datetime

def add_to_history(user_identifier: str, role: str, content: str):
    """
    Save a message to DB (role can be 'user' or 'assistant').
    """
    session = SessionLocal()
    try:
        user = get_or_create_user(session, user_identifier)
        msg = Message(
            user_id=user.id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        session.add(msg)
        session.commit()
    finally:
        session.close()

def get_chat_history(user_identifier: str, limit: int = 50):
    """
    Retrieve the most recent messages for a user.
    Returns them in OpenAI API format: [{"role": ..., "content": ...}, ...]
    """
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(user_id=user_identifier).first()
        if not user:
            return []
        messages = (
            session.query(Message)
            .filter_by(user_id=user.id)
            .order_by(Message.created_at.asc())
            .limit(limit)
            .all()
        )
        return [{"role": m.role, "content": m.content} for m in messages]
    finally:
        session.close()
