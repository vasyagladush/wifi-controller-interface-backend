# WiFi Controller Interface Backend

## Requirements:

- python >= 3.10.\* and pip

## Setting up

1. Create a virtual environment:

```console
$ python3 -m venv venv
```

2. Activate the created venv:

- Linux/Mac command: `source venv/bin/activate`
- Windows Command: `.\venv\Scripts\activate`

3. Install dependencies:

```console
(venv)$ pip install -r requirements.txt
```

4. Create a database.sqlite file (if using SQLite file)

```console
touch database.sqlite
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

## Migrations

- add new models' imports to the end of the [models module file](./src/models/__init__.py) so that Alembic detects that new tables have to be created, like:

```python
from models.user import User
```

- Generate a migration: `invoke migrationsGenerate --message=your_message_here`
- Run migrations: `invoke migrationsRun`
- Revert the last migration: `invoke migrationsRevert`

## Sources

- https://fastapi.tiangolo.com/tutorial/sql-databases/
- https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308#:~:text=Improvements%20to%20the%20async%20experience,over%20a%20synchronous%20database%20setup.
- https://github.com/Youngestdev/fastapi-mongo
