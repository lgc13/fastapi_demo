from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import SQLModel, create_engine, Session

# Database setup
DATABASE_URL = "sqlite:///database.db"
connect_args = {"check_same_thread": False}  # use the same db in different threads
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def get_session():
    """
    Session will store the objects in memory.
    Engine will communicate with the db.
    yield wil provide a new Session for each request
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# To create the table models
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print(f">>> in lifespan: {_app}")
    create_db_and_tables()
    yield


print(">>>> IN database.py")
