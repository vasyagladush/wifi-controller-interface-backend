from invoke import task # type: ignore
from os import path

@task
def start(c):
    c.run("python src/main.py")

@task
def migrationsGenerate(c, message):
    """Generate a new migration."""
    # Ensure we're using the virtual environment's alembic
    venv_alembic = path.join('venv', 'bin', 'alembic')

    # Run the Alembic command
    # c.run(f"PYTHONPATH=./src {venv_alembic} revision --autogenerate -m \"{message}\"", pty=True)
    c.run(f"{venv_alembic} revision --autogenerate -m \"{message}\"", pty=True)

@task
def migrationsRun(c):
    """Apply migrations."""
    # Ensure we're using the virtual environment's alembic
    venv_alembic = path.join('venv', 'bin', 'alembic')
    c.run(f"{venv_alembic} upgrade head", pty=True)

@task
def migrationsRevert(c):
    """Revert last migration."""
    # Ensure we're using the virtual environment's alembic
    venv_alembic = path.join('venv', 'bin', 'alembic')
    c.run(f"{venv_alembic} downgrade -1", pty=True)
