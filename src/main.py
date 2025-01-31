from fastapi import FastAPI, Response, HTTPException
import logging
from pydantic import BaseModel

app = FastAPI()
logger = logging.getLogger('uvicorn.error')


class Item(BaseModel):
    id: int
    text: str
    is_complete: bool


class ItemRequest(BaseModel):
    text: str


items: list[Item] = []


@app.get("/")
def main():
    logger.info("Hello from fastapi-demo!")
    return Response("This is the main page!")


@app.get("/items", response_model=list[Item])
def get_items(page: int = 1, size: int = 10) -> list[Item]:
    logger.info(f">>> Getting items in the list with page {page} and size {size}")

    page_start = (page - 1) * size
    page_end = page_start + size

    return items[page_start:page_end]


@app.post("/items")
def create_item(item_request: ItemRequest) -> list[Item]:
    logger.info(f"Creating item with item_request: {item_request}")

    last_id = items[-1].id if items else 0
    new_id = last_id + 1

    new_item = Item(
        id=new_id,
        text=item_request.text,
        is_complete=False
    )
    items.append(new_item)

    return items


@app.get("/items/{item_id}")
def get_item_by_id(item_id: int) -> Item:
    logger.info("Getting item by id:", item_id)

    found_item = next(
        (item for item in items if item.id == item_id),
        None,
    )

    if found_item is None:
        raise HTTPException(status_code=404, detail="Item not found :(")

    return found_item


@app.delete("/items")
def delete_items():
    logger.info("Deleting all items!")
    items.clear()
    return items


if __name__ == "__main__":
    main()
