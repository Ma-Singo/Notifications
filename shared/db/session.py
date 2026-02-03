from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    with SessionLocal() as session:
        yield session
