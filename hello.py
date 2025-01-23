from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def main():
    print("Hello from fastapi-demo!")
    return "hello world!"


if __name__ == "__main__":
    main()
