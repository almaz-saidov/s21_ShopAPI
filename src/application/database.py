from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(settings.DB_URL)

SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db_session():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
