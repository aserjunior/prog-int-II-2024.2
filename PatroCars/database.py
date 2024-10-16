from sqlmodel import create_engine, Session


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)


def initialize_db():
    from models import SQLModel
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
