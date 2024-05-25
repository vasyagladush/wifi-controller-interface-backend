import uuid
from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    password_hash: Mapped[str]
    # TODO: roles: admin, user, etc.
