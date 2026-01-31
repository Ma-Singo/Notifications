from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import Settings

engine = create_engine(
    Settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    with SessionLocal() as session:
        yield session
