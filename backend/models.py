from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    leetcode_username = Column(String)
    timezone = Column(String)
    last_reminder_sent = Column(DateTime, nullable=True)
