from sqlmodel import create_engine, SQLModel, Session
from config import settings

DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}/{settings.database_name}"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
