from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Network(Base):
    __tablename__: str = "network"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    ssid: Mapped[str] = mapped_column(nullable=True)
    country_code: Mapped[str] = mapped_column(nullable=False)
    # TODO: "This list is incomplete. You can help by expanding it."
