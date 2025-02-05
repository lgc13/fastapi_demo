from typing import Optional, cast, Any

from fastapi import FastAPI, Response, HTTPException
import logging
from sqlmodel import select, delete

from src.database import lifespan, SessionDep
from src.models import ItemPatchRequest, ItemRequest, Item

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

    logger.info(f">>> Item {item_id} was deleted!")


if __name__ == "__main__":
    main()
