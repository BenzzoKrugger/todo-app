from sqlmodel import create_engine, Session, SQLModel
from .models.todo import Todo

engine = create_engine("sqlite:///database.db", connect_args={'check_same_thread': False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session