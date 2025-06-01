from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)


class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    file_name = Column(String)
    summary = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
