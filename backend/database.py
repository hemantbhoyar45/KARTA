from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import config

import logging

logger = logging.getLogger(__name__)

# Default to local SQLite if no external postgres is defined
SQLALCHEMY_DATABASE_URL = config.DATABASE_URL or "sqlite:///./creditiq.db"

def _init_engine(url: str):
    connect_args = {"check_same_thread": False} if "sqlite" in url else {}
    eng = create_engine(url, connect_args=connect_args)
    if "sqlite" not in url:
        with eng.connect() as conn:
            pass
    return eng

try:
    engine = _init_engine(SQLALCHEMY_DATABASE_URL)
except Exception as e:
    logger.warning(f"Database connection to '{SQLALCHEMY_DATABASE_URL}' failed ({e}). Falling back to local SQLite.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./creditiq.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
