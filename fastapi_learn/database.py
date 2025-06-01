from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLACHEMY_DB_URL = "sqlite:///./articles.db"

engine = create_engine(SQLACHEMY_DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# DB setup
engine_summary = create_engine("sqlite:///summaries.db", echo=False)
SessionLocal_summary = sessionmaker(bind=engine_summary)

Base_summary = declarative_base()


# Create tables
def init_db():
    Base_summary.metadata.create_all(bind=engine_summary)
