from fastapi import FastAPI

app = FastAPI()

items = []


@app.get("/")
def main():
    print("Hello from fastapi-demo!")
    return "This is the main page!"


@app.get("/hello")
def hello():
    print("Hello World from the /hello endpoint!")
    return "Hello World!"


@app.post("/items")
def create_item():
    print("Creating item")
    items.append("Item Inserted")
    return items


@app.get("/items")
def get_items():
    print("Items in the list:", items)
    return items


@app.delete("/items")
def delete_items():
    print("Deleting all items!")
    items.clear()
    return items


if __name__ == "__main__":
    main()
