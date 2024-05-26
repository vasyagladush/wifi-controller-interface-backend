from uuid import uuid4

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from models.user import User
