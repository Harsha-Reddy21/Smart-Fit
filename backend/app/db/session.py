from typing import Generator
import os
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError, ProgrammingError
from app.db.base import Base


def _ensure_database(url_str: str) -> None:
    try:
        test_engine = sa_create_engine(url_str)
        with test_engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        return
    except OperationalError:
        url = make_url(url_str)
        admin_url = url.set(database="postgres")
        try:
            admin_engine = sa_create_engine(str(admin_url), isolation_level="AUTOCOMMIT")
            with admin_engine.connect() as conn:
                conn.exec_driver_sql(f'CREATE DATABASE "{url.database}"')
        except ProgrammingError:
            # Database likely exists or insufficient privileges; ignore and proceed
            pass


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:12345678@localhost:5432/smart-fit",
)

_ensure_database(DATABASE_URL)
engine = sa_create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def create_db_and_tables() -> None:
    from app.models import user, exercise, workout, nutrition, progress, chat  # noqa: F401
    Base.metadata.create_all(engine)


def get_session() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



