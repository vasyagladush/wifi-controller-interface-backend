# WiFi Controller Interface Backend

## Requirements:

- python >= 3.10.\* and pip

## Setting up

1. Create a virtual environment:

```console
python3 -m venv venv
```

2. Activate the created venv:

- Linux/Mac command: `source venv/bin/activate`
- Windows Command: `.\venv\Scripts\activate`

3. Install dependencies (inside the venv from now on):

```console
pip install -r requirements.txt
```

4. Create a database.sqlite file (if using SQLite file)

Linux/Mac:
```console
touch database.sqlite
```
Windows:
```console
type NUL > database.sqlite
```

5. Create a .env file

```console
cp .env.sample .env
```

6. Install pre-commit hooks:

```console
pre-commit install
```

7. Start the application:

```console
invoke start
```

## Next app starts

### Traditional way:

1. Activate venv

- Linux/Mac command: `source venv/bin/activate`
- Windows Command: `.\venv\Scripts\activate`

2. Start the application:
   
```console
invoke start
```

### Alternative way:
Windows (requires PowerShell):
```console
.\run
```
Note regarding alternative Windows start: App may not close with the terminal - make sure to terminate the app (`CTRL` + `C`) before closing terminal.
## Migrations

- add new models' imports to the end of the [models module file](./src/models/__init__.py) so that Alembic detects that new tables have to be created, like:

```python
from models.user import User
```

- Generate a migration:
```console
invoke migrationsGenerate --message=your_message_here
```
- Run migrations:
```console
invoke migrationsRun
```
- Revert the last migration:
```console
invoke migrationsRevert
```

## Sources

- https://fastapi.tiangolo.com/tutorial/sql-databases/
- https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308#:~:text=Improvements%20to%20the%20async%20experience,over%20a%20synchronous%20database%20setup.
- https://github.com/Youngestdev/fastapi-mongo
- https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file#4-chain-dependencies
