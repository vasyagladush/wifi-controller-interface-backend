from unicodedata import name

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class AP(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=True)
