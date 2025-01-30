from fastapi import FastAPI, Response, HTTPException
import logging

app = FastAPI()
logger = logging.getLogger('uvicorn.error')

items: list[str] = []


@app.get("/")
def main():
    logger.info("Hello from fastapi-demo!")
    return Response("This is the main page!")


@app.get("/items")
def get_items(page: int = 1, size: int = 10):
    logger.info(f">>> Getting items in the list with page {page} and size {size}" )

    page_start = (page - 1) * size
    page_end = page_start + size

    return items[page_start:page_end]


@app.post("/items")
def create_item():
    logger.info("Creating item")

    items.append("NEW ITEM!")
    return items

@app.get("/items/{item_id}")
def get_item_by_id(item_id: int) -> str:
    logger.info("Getting item by id:", item_id)

    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found :(")

    item = items[item_id]

    return item


@app.delete("/items")
def delete_items():
    logger.info("Deleting all items!")
    items.clear()
    return items


if __name__ == "__main__":
    main()
