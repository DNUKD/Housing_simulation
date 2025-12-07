from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite DB file location
DATABASE_URL = "sqlite:///./cost_of_living.db"

# DB engine used for con and exec statements
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory for creating DB sessions (query, insert, update, delete)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()
