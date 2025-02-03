from typing import Optional

from fastapi import FastAPI, Response, HTTPException
import logging
from pydantic import BaseModel

app = FastAPI()
logger = logging.getLogger("uvicorn.error")


class Item(BaseModel):
    id: int
    text: str
    is_complete: bool


class ItemRequest(BaseModel):
    text: str


class ItemPatchRequest(BaseModel):
    is_complete: bool


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


@app.post("/items", response_model=Item)
def create_item(item_request: ItemRequest) -> Item:
    logger.info(f"Creating item with item_request: {item_request}")

    all_ids: list[int] = list(map(lambda it: it.id, items))
    biggest_id = max(all_ids, default=None)

    new_id = biggest_id + 1 if biggest_id is not None else 1

    new_item = Item(id=new_id, text=item_request.text, is_complete=False)
    items.append(new_item)

    return new_item


@app.get("/items/{item_id}")
def get_item_by_id(item_id: int) -> Item:
    logger.info(f"Getting item by id: {item_id}")

    found_item: Optional[Item] = next((it for it in items if it.id == item_id), None)
    # ALTERNATIVELY, here's a lambda:
    #  next(filter(lambda it: it.id == item_id, items), None)

    if found_item is None:
        raise HTTPException(status_code=404, detail="Item not found :(")

    return found_item

@app.patch("/items/{item_id}")
def update_item(item_id: int, item_patch_request: ItemPatchRequest) -> Item:
    logger.info(f"Updating item with item_id: {item_id} and request: {item_patch_request}")

    item = get_item_by_id(item_id)
    updated_item = item.model_copy(update={"is_complete": item_patch_request.is_complete})

    updated_items = list(
        map(
            lambda x: updated_item if x.id == item.id else x,
            items,
        )
    )

    items.clear()
    items.extend(updated_items)

    return updated_item


@app.delete("/items")
def delete_items():
    logger.info("Deleting all items!")
    items.clear()
    return items


@app.delete("/items/{item_id}")
def delete_item_by_id(item_id: int) -> None:
    logger.info(f"Deleting item by id: {item_id}")

    found_item = get_item_by_id(item_id)
    items.remove(found_item)


if __name__ == "__main__":
    main()
