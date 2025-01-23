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
   
   uv add ruff --dev # dev dependency
    
    # if needed, install python like so:
    uv python install
    ```
   
4. (Possibly) change PyCharm's Interpreter settings
   - Make sure its pointing to the same Python version as you have installed or in the .venv
   - Settings > Project: Your_Project_Name_Here > Add Interpreter > Add Local Interpreter > Select Existing > Python path dropdown:
   - Choose the one for: `~/YourProjectPath/.venv/bin/python`
   - Alternatively, the IDE might just pop up telling you to use the one for your project:
   - Settings > Project: Your_Project_Name_Here > Python Interpreter > Some pop up here saying to add the `.venv`
   
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
    uv run hello.py # runs just the app
    uv run uvicorn hello:app --reload # runs this in a server. reload will auto run if updates are made
    
    # steps for venv: https://docs.astral.sh/uv/pip/environments/
    uv venv 
    source my-env-name-here/bin/activate # 'activating' env making its pakages available
    ```
