## Learning FastApi, UV, Ruff and more!

- Creating app steps:

1. Create repo
2. Add [UV - package manager](https://github.com/astral-sh/uv)

    ```shell
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    uv init # this will also create the pyproject.toml
    ```

3. Add dependencies

    ```shell
    # adding dependencies
    uv add depedency_name_here
    uv add fastapi sqlalchemy alembic uvicorn
    
    : '
    examples:
    
    fastapi - web framework
    sqlalchemy - DB
    alembic - DB migration tool
    uvicorn - web server
    pydantic - data validation
    '
   
   uv add some_dependency --dev # dev dependency
    
    # if needed, install python like so:
    uv python install
    ```
   
4. (Possibly) change PyCharm's Interpreter settings
   - Make sure its pointing to the same Python version as you have installed or in the .venv
   - Settings > Project: Your_Project_Name_Here > Add Interpreter > Add Local Interpreter > Select Existing > Python path dropdown:
   - Choose the one for: `~/YourProjectPath/.venv/bin/python`
   - Alternatively, the IDE might just pop up telling you to use the one for your project:
   - Settings > Project: Your_Project_Name_Here > Python Interpreter > Some pop up here saying to add the `.venv`
   - ...
   - If getting this error: warning: `VIRTUAL_ENV=/app/.venv` does not match the project environment path `.venv` and will be ignored
     - [fix with this!](https://github.com/astral-sh/uv/issues/7073#issuecomment-2581842745)
   
5. Create first api:

   ```python
   from fastapi import FastAPI
   
   app = FastAPI()
   
   @app.get("/hello")
   def main():
    print("Hello from fastapi-demo!")
     return "hello world!"
   
   
   if __name__ == "__main__":
     main()
   ```
      
6. Run server

    ```zsh
    uv run main.py # runs just the app
    uv run uvicorn src.main:app --reload # runs this in a server. reload will auto run if updates are made
    
    # steps for venv: https://docs.astral.sh/uv/pip/environments/
    uv venv 
    source my-env-name-here/bin/activate # 'activating' env making its pakages available
    ```
   
7. (Optional) Add Docker

   1. Add a `Dockerfile`
   2. You can use the code found [here](https://docs.astral.sh/uv/guides/integration/fastapi/#deployment) as a basis:
   
      ```dockerfile
      FROM python:3.12-slim
      
      # Install uv.
      COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
      
      # Copy the application into the container.
      COPY . /app
      
      # Install the application dependencies.
      WORKDIR /app
      RUN uv sync --frozen --no-cache
      
      # Run the application.
      CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]
      ```
   
      ###### Change some of the variables to run with `uvicorn` instead of `fastapi`

      ```dockerfile
      # possibly a newer version
      FROM python:3.13-slim 
      
      # use uvicorn: look at file `src/main` then app object in that file
      CMD ["/app/.venv/bin/uvicorn", "src.main:app", "--port", "80", "--host", "0.0.0.0"]
      ```
   3. Run Docker

      ```shell
      # build Docker image
      docker build -t fastapi_my_image .
      
      # run it, mapping port 8000 on the host to the 80 on the container
      docker run -p 8000:80 fastapi_my_image
      ```
      
   4. (Alternatively) Using docker-compose:

      ```yaml
      # docker-compose.yaml
      services:
        backend:
          build: .
          image: fastapi_my_image:latest
          container_name: fastapi_my_container
          command: uv run uvicorn src.main:app --host 0.0.0.0 --port 80 --reload # important
          ports:
            - "8000:80"
          volumes: # important
            - .:/app
      ```
      
      ```shell
      # builds the container, the image, then runs it
      docker compose up 
      
      # possible to prevent uneeded containers:
      docker compose up --no-recreate
      ```

8. [Ruff Dependency](https://docs.astral.sh/ruff/tutorial/#getting-started) - Python linter and code formatter

   ```shell
   uv add ruff --dev # dev dependency
   uv run ruff check # running ruff check on the app
   uv run ruff check --fix # fixes errors linter found
   uv run ruff format # formats the file in accordance to pep conventions
   ``` 
   
   ```toml
   # pyproject.toml
   # add the following
   
   [tool.ruff.lint]
   extend-select = ["E", "W"]
   ```
   
9. [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

   - FastAPI uses Starlette

   ```shell
   uv add pytest --dev
   uv add httpx --dev
   
   uv run pytest test.py
   ```
   
   - Add pytest configuration so it finds the tests for you. [See guide here](https://docs.pytest.org/en/stable/reference/customize.html)

   ```toml
   # pyproject.tolm
   [tool.pytest.ini_options]
   minversion = "6.0"
   addopts = "-ra -q"
   testpaths = [
       "test.py", # example here
       "tests",
       "integration",
   ]
   ```
   
   - Test example:

```python
# test.py
from fastapi.testclient import TestClient
from src.hello import app

client = TestClient(app)


def test_root():
   response = client.get("/")
   assert response.status_code == 200
   assert response.text == "This is the main page!"


def test_items():
   response = client.get("/items")
   assert response.status_code == 200
   assert response.json() == []

```
      