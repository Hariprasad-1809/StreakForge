from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

try:
    from .database import Base
except ImportError:
    from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    leetcode_username = Column(String)
    timezone = Column(String)
    last_reminder_sent = Column(DateTime, nullable=True)


class SupportQuery(Base):
    __tablename__ = "support_queries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    code = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
