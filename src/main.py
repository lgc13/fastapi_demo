from contextlib import asynccontextmanager
from typing import Annotated, Optional, cast, Any

from fastapi import FastAPI, Response, HTTPException, Depends
import logging
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select, delete


class Item(SQLModel, table=True):
    id: int = Field(primary_key=True)
    text: str
    is_complete: bool


class ItemRequest(BaseModel):
    text: str


class ItemPatchRequest(BaseModel):
    is_complete: bool


# Database setup
DATABASE_URL = "sqlite:///database.db"
connect_args = {"check_same_thread": False} # use the same db in different threads
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

app = FastAPI(lifespan=lifespan)
logger = logging.getLogger("uvicorn.error")
items: list[Item] = []

@app.get("/")
def main():
    logger.info("Hello from fastapi-demo!")
    return Response("This is the main page!")


@app.post("/items", response_model=Item)
def create_item(item_request: ItemRequest, session: SessionDep) -> Item:
    logger.info(f">>> Creating item with item_request: {item_request}")

    new_item = Item(text=item_request.text, is_complete=False)

    session.add(new_item)
    session.commit()
    session.refresh(new_item)

    return new_item

@app.get("/items", response_model=list[Item])
def get_items(session: SessionDep, page: int = 0, size: int = 10) -> list[Item]:
    logger.info(f">>> Getting items in the list with page {page} and size {size}")

    return list(session.exec(select(Item).offset(page).limit(size)).all())

@app.get("/items/{item_id}")
def get_item_by_id(item_id: int, session: SessionDep) -> Item:
    logger.info(f">>> Getting item by id: {item_id}")

    item: Optional[Item] = session.get(Item, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found :(")

    return item


@app.patch("/items/{item_id}")
def update_item(item_id: int, item_patch_request: ItemPatchRequest, session: SessionDep) -> Item:
    logger.info(f"Updating item with item_id: {item_id} and request: {item_patch_request}")

    item = get_item_by_id(item_id, session)
    item.is_complete = item_patch_request.is_complete

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


@app.delete("/items")
def delete_items(session: SessionDep):
    logger.info(">>> Deleting all items!")

    statement = cast(Any, delete(Item))
    session.exec(statement)
    session.commit()


@app.delete("/items/{item_id}")
def delete_item_by_id(item_id: int, session: SessionDep) -> None:
    logger.info(f">>> Deleting item by id: {item_id}")

    item = get_item_by_id(item_id, session)
    session.delete(item)
    session.commit()


if __name__ == "__main__":
    main()
